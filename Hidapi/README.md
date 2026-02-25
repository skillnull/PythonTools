# AW720M 灯光控制脚本（Mac）

通过 HID Feature Report 控制 Alienware AW720M 等设备的 RGB 灯光。

## 遇到 externally-managed-environment 时（Homebrew Python）

系统禁止直接 `pip3 install` 时，可用下面任一方式，**无需手动建虚拟环境**。

### 方式一：pipx run（推荐，零安装）

每次用 `pipx run` 自动带好 hidapi，不用激活 venv、不用改系统 Python：

```bash
cd Hidapi
# 首次使用需安装 pipx：brew install pipx && pipx ensurepath
pipx run --spec hidapi python3 AW720M.py --list
pipx run --spec hidapi python3 AW720M.py --r 255 --g 0 --b 0
```

### 方式二：允许 pip 安装到系统（一次安装，之后直接 python3）

接受 PEP 668 的覆盖方式，以后可直接 `python3 AW720M.py`：

```bash
pip3 install --break-system-packages hidapi
cd Hidapi
python3 AW720M.py --list
python3 AW720M.py --r 255 --g 0 --b 0
```

### 方式三：虚拟环境（传统做法）

```bash
cd Hidapi
python3 -m venv .venv
source .venv/bin/activate
pip install hidapi
python3 AW720M.py --list
python3 AW720M.py --r 255 --g 0 --b 0
```

## 使用

```bash
# 枚举本机 HID 设备，确认鼠标的 VID/PID
python3 AW720M.py --list

# 设置灯光颜色（不写死 VID/PID，按设备名称自动发现；或 --list 后用 --vid/--pid 指定）
python3 AW720M.py --r 255 --g 0 --b 0
python3 AW720M.py --r 0 --g 255 --b 0
python3 AW720M.py --r 0 --g 0 --b 255
```

（若用方式一，上述命令前加：`pipx run --spec hidapi`。）

## 提示「无法打开设备 / open failed」时

- 脚本**不写死 VID/PID**，设备 ID 从枚举结果动态获取；名称含 Alienware/AW720 等即会匹配。
1. **macOS 输入监控权限**：系统设置 → 隐私与安全性 → 输入监控 → 勾选「终端」（或你运行脚本的 App）。
2. **用 sudo 试一次**：`sudo python3 AW720M.py --r 255 --g 0 --b 0`（若这样能成功，多半是权限问题）。
3. 关闭 **Alienware Command Center、Dell 外设管理** 等可能占用 HID 的软件后再试。
4. **AW720M 请用 USB 线连接**（不要仅用蓝牙）再运行脚本。
5. **macOS 限制**：系统可能独占鼠标的 HID 接口，导致即使用 sudo 仍「open failed」。此时只能在 Windows 或 Linux 下用本脚本控制灯光。
6. 脚本会遍历所有匹配接口并尝试按 path / 按 vid:pid 打开；若仍失败，可用 `--list` 查看本机 VID:PID 后以 `--vid/--pid` 明确指定。

## 参数说明

| 参数 | 说明 |
|------|------|
| `--list` | 列出所有 HID 设备（用于查看 VID/PID） |
| `--vid 0xXXXX` | USB Vendor ID（不指定则按设备名称自动发现） |
| `--pid 0xXXXX` | USB Product ID（不指定则按设备名称自动发现） |
| `--r`, `--g`, `--b` | 红/绿/蓝 0–255 |
| `--zone N` | 灯区索引，默认 0 |

协议参考 OpenRGB 的 Alienware 控制器实现。
