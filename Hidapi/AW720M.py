#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AW720M 灯光控制（Mac，可不使用虚拟环境）
通过 HID Feature Report 设置 Alienware 鼠标/设备的 RGB 灯光。
依赖：pip3 install --user hidapi  或  brew install hidapi 后 pip 安装 hidapi
"""

from __future__ import print_function

import argparse
import sys
import time

try:
    import hid
except ImportError:
    print("请先安装 hidapi：", file=sys.stderr)
    print("  方式一（推荐，无需改系统）：pipx run --spec hidapi python3 AW720M.py --list", file=sys.stderr)
    print("  方式二（一次安装）：pip3 install --break-system-packages hidapi", file=sys.stderr)
    print("  方式三：python3 -m venv .venv && source .venv/bin/activate && pip install hidapi", file=sys.stderr)
    sys.exit(1)

# 协议常量
# APIv4：34 字节 Feature Report（OpenRGB Alienware 笔记本/台式）
REPORT_SIZE = 33
HIDAPI_REPORT_SIZE = REPORT_SIZE + 1
CMD_SET_COLOR = 0x27
# APIv7：65 字节 USB Interrupt OUT（Alienware 鼠标，如 AW610M/AW720M，见 alienfx-tools）
APIv7_REPORT_SIZE = 65
APIv7_CMD_CONTROL = (0x40, 0x10, 0x0c, 0x00, 0x01)  # COMMV7_control
APIv7_EFFECT_COLOR = 1  # v7OpCodes[AlienFX_A_Color]
# COMMV7_update：设色后发送以“提交”，否则后续设色可能不生效
APIv7_CMD_UPDATE = (0x40, 0x60, 0x07, 0x00, 0xc0, 0x4e, 0x00, 0x01)

# 自动发现时仅按设备名称匹配，VID/PID 完全从枚举结果动态获取，不写死
NAME_KEYWORDS = ("alienware", "aw720", "g series")


def _path_str(d):
    p = d.get("path")
    if p is None:
        return ""
    return p.decode("utf-8", errors="replace") if isinstance(p, bytes) else p


def _str_lower(d, key):
    s = (d.get(key) or "").strip() or ""
    if isinstance(s, bytes):
        s = s.decode("utf-8", errors="replace")
    return s.lower()


def _device_name_matches(d, keywords=NAME_KEYWORDS):
    """设备厂商或产品名包含任一关键词即视为匹配，用于动态发现。"""
    product = _str_lower(d, "product_string")
    manufacturer = _str_lower(d, "manufacturer_string")
    combined = product + " " + manufacturer
    return any(kw in combined for kw in keywords)


def list_hid_devices():
    """枚举所有 HID 设备，便于确认 AW720M 的 VID/PID。"""
    print("HID 设备列表（VID:PID 路径 厂商 产品）：")
    print("-" * 60)
    for d in hid.enumerate():
        print("  {:04x}:{:04x}  {}  {}  {}".format(
            d["vendor_id"],
            d["product_id"],
            _path_str(d),
            (d.get("manufacturer_string") or "").strip() or "-",
            (d.get("product_string") or "").strip() or "-",
        ))
    print("-" * 60)
    print("未指定 --vid/--pid 时会按设备名称自动匹配（名称含 Alienware/AW720 等）；VID:PID 从枚举动态获取。")


def find_target_devices(vid=None, pid=None, name_keywords=None):
    """
    动态查找目标设备，不写死 VID/PID。
    - 若指定了 vid+pid：枚举该 VID:PID 下所有 HID 接口，返回 [(path, vid, pid), ...]。
    - 未指定：枚举全部设备，按厂商/产品名包含关键词匹配，返回匹配项的 path 与枚举得到的 vid/pid。
    返回 [(path, vid, pid), ...]，vid/pid 均来自枚举结果。
    """
    out = []
    for d in hid.enumerate(vid if vid is not None else 0, pid if pid is not None else 0):
        v, p = d["vendor_id"], d["product_id"]
        if vid is not None and pid is not None:
            if v != vid or p != pid:
                continue
        else:
            if not _device_name_matches(d, name_keywords or NAME_KEYWORDS):
                continue
        out.append((d["path"], v, p))
    return out


def send_feature_report(dev, buf):
    """发送 HID Feature Report，并做短暂延时避免设备忙。"""
    dev.send_feature_report(bytes(buf))
    time.sleep(0.06)


def get_feature_report(dev, report_id=0x00, size=HIDAPI_REPORT_SIZE):
    """读取 HID Feature Report。"""
    return dev.get_feature_report(report_id, size)


def set_color_apiv7(dev, r, g, b, zone=0, brightness=0x64, retries=5):
    """
    APIv7：65 字节 USB Interrupt OUT，用于 Alienware 鼠标（AW610M/AW720M 等）。
    先发 control 设色，再发 update 提交；重复 retries 次并加延时，提高“有时有效有时无效”时的成功率。
    """
    # 预建 control 与 update 包，避免重复逻辑
    buf = bytearray(APIv7_REPORT_SIZE)
    buf[0] = 0x00
    for i, byte_val in enumerate(APIv7_CMD_CONTROL):
        buf[1 + i] = byte_val
    buf[5] = APIv7_EFFECT_COLOR
    buf[6] = brightness & 0xFF
    buf[7] = zone & 0xFF
    buf[8] = r & 0xFF
    buf[9] = g & 0xFF
    buf[10] = b & 0xFF
    control_packet = bytes(buf)

    upd = bytearray(APIv7_REPORT_SIZE)
    upd[0] = 0x00
    for i, byte_val in enumerate(APIv7_CMD_UPDATE):
        upd[1 + i] = byte_val
    update_packet = bytes(upd)

    time.sleep(0.05)  # 打开设备后稍等再发，避免首包被丢
    for _ in range(retries):
        dev.write(control_packet)
        time.sleep(0.12)
        dev.write(update_packet)
        time.sleep(0.12)


def set_color_direct(dev, r, g, b, zones=(0,)):
    """
    APIv4：34 字节 HID Feature Report，用于部分 Alienware 笔记本/台式。
    部分设备不回复读取，发送后若读回失败则忽略。
    """
    buf = bytearray(HIDAPI_REPORT_SIZE)
    buf[0] = 0x00
    buf[1] = 0x03
    buf[2] = CMD_SET_COLOR
    buf[3] = r & 0xFF
    buf[4] = g & 0xFF
    buf[5] = b & 0xFF
    n = len(zones)
    buf[6] = (n >> 8) & 0xFF
    buf[7] = n & 0xFF
    for i, z in enumerate(zones):
        if 8 + i < len(buf):
            buf[8 + i] = z & 0xFF
    send_feature_report(dev, buf)
    try:
        get_feature_report(dev)
    except OSError:
        pass


def open_device(vid, pid, path=None):
    """
    打开 HID 设备，兼容 hid.Device（新）与 hid.device()（旧）两种 API。
    path 优先；否则用 vid/pid。
    """
    def open_by_path(p):
        if hasattr(hid, "Device"):
            return hid.Device(path=p)
        dev = hid.device()
        dev.open_path(p)
        return dev

    def open_by_vid_pid(v, p):
        if hasattr(hid, "Device"):
            return hid.Device(vid=v, pid=p)
        dev = hid.device()
        dev.open(v, p)
        return dev

    if path is not None:
        return open_by_path(path)
    return open_by_vid_pid(vid, pid)


def main():
    ap = argparse.ArgumentParser(description="AW720M / Alienware HID 灯光控制（可不使用虚拟环境）")
    ap.add_argument("--list", action="store_true", help="枚举 HID 设备并退出，用于查看 VID/PID")
    ap.add_argument("--vid", type=lambda x: int(x, 0), default=None, help="USB Vendor ID（不指定则按设备名称自动发现）")
    ap.add_argument("--pid", type=lambda x: int(x, 0), default=None, help="USB Product ID（不指定则按设备名称自动发现）")
    ap.add_argument("--no-report-id", action="store_true", help="部分设备不需要 Report ID，当前实现仍带 1 字节")
    ap.add_argument("--r", type=int, default=None, metavar="0-255", help="红色")
    ap.add_argument("--g", type=int, default=None, metavar="0-255", help="绿色")
    ap.add_argument("--b", type=int, default=None, metavar="0-255", help="蓝色")
    ap.add_argument("--zone", type=int, default=0, help="灯区索引，默认 0")
    args = ap.parse_args()

    if args.list:
        list_hid_devices()
        return

    r = args.r if args.r is not None else 255
    g = args.g if args.g is not None else 0
    b = args.b if args.b is not None else 0
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    # 动态查找目标设备：未指定 vid/pid 时按名称匹配，vid/pid 一律从枚举结果取
    candidates = find_target_devices(args.vid, args.pid)
    if not candidates:
        # 仅当用户同时指定了 vid 和 pid 时，再试一次直接按该 ID 打开
        if args.vid is not None and args.pid is not None:
            candidates = [(None, args.vid, args.pid)]
        else:
            print("未找到名称匹配的设备（Alienware/AW720 等）。请运行 python3 AW720M.py --list 查看设备列表，并用 --vid/--pid 指定。", file=sys.stderr)
            sys.exit(2)

    # 对每个候选接口都打开并发送设色命令（不只看第一个能打开的），避免枚举顺序导致有时命中 LED 有时没命中
    last_error = None
    any_open = False
    any_sent = False
    for path, vid_open, pid_open in candidates:
        dev = None
        try:
            dev = open_device(vid_open, pid_open, path=path)
            any_open = True
        except Exception as e:
            last_error = e
            continue
        try:
            try:
                set_color_apiv7(dev, r, g, b, zone=args.zone)
                any_sent = True
            except OSError:
                try:
                    set_color_direct(dev, r, g, b, zones=(args.zone,))
                    any_sent = True
                except OSError:
                    pass
        finally:
            if dev is not None:
                dev.close()

    # 若按 path 一个都没打开，再试一次仅用 vid/pid 打开
    if not any_open and candidates:
        vid_open, pid_open = candidates[0][1], candidates[0][2]
        try:
            dev = open_device(vid_open, pid_open, path=None)
            any_open = True
            try:
                set_color_apiv7(dev, r, g, b, zone=args.zone)
                any_sent = True
            except OSError:
                try:
                    set_color_direct(dev, r, g, b, zones=(args.zone,))
                    any_sent = True
                except OSError:
                    pass
            finally:
                dev.close()
        except Exception as e:
            last_error = e

    if not any_open:
        print("无法打开 Alienware 设备：{}".format(last_error), file=sys.stderr)
        print("", file=sys.stderr)
        print("常见原因与处理：", file=sys.stderr)
        print("  1. macOS 权限：系统设置 → 隐私与安全性 → 输入监控 → 勾选「终端」或你使用的 App。", file=sys.stderr)
        print("  2. 尝试用 sudo 运行：sudo python3 AW720M.py --r 255 --g 0 --b 0", file=sys.stderr)
        print("  3. 关闭 Alienware Command Center、Dell 外设管理等可能占用设备的软件后重试。", file=sys.stderr)
        print("  4. AW720M 请用 USB 线连接（不要仅用蓝牙），再试。", file=sys.stderr)
        print("  5. macOS 可能独占鼠标的 HID 接口，导致无法打开；可尝试在 Windows 或 Linux 下用本脚本。", file=sys.stderr)
        if not candidates or candidates[0][0] is None:
            print("  6. 运行 python3 AW720M.py --list 查看本机 HID 设备，用 --vid/--pid 指定你的设备。", file=sys.stderr)
        sys.exit(2)

    if any_sent:
        print("已设置灯光 R={} G={} B={}".format(r, g, b))
    else:
        print("已向设备各接口发送命令但均写失败；若灯光无变化可尝试关闭 Dell/Alienware 驱动或换 USB 口。", file=sys.stderr)


if __name__ == "__main__":
    main()
