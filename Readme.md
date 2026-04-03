# Tailscale Tray (GTK + AppIndicator)

A lightweight GTK-based system tray application to control **Tailscale** directly from your Linux desktop.

## ✨ Features

- Toggle Tailscale on/off from tray
- Select exit nodes dynamically (radio menu)
- Detect current Tailscale state on startup
- Runs as a **systemd user service**
- Minimal, no full GUI window required

---

## 📦 Requirements

- Python 3
- GTK 3 (`PyGObject`)
- AppIndicator support
- Tailscale installed

### Install dependencies (Debian/Ubuntu)

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
```
### 🚀 Installation

#### Move the script
```
mkdir -p ~/.local/bin
mv tailscaleTrayVer1.py ~/.local/bin/tailscale-tray
chmod +x ~/.local/bin/tailscale-tray
```
#### Create systemd user service
```
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/tailscale-tray.service
```
##### Paste:
```
[Unit]
Description=Tailscale Tray App
After=network.target

[Service]
ExecStart=/home/YOUR_USERNAME/.local/bin/tailscale-tray
Restart=always
Environment=DISPLAY=:0
Environment=XDG_CURRENT_DESKTOP=GNOME

[Install]
WantedBy=default.target

#### Enable and start
systemctl --user daemon-reexec
systemctl --user enable tailscale-tray.service
systemctl --user start tailscale-tray.service
```
### 🧠 How It Works
#### Toggle
Enable: tailscale up --accept-routes
Disable: tailscale down --accept-routes
#### Exit Node Selection
Fetch nodes: tailscale status --json
Set exit node: tailscale up --exit-node=<IP> --accept-routes
Disable exit node: tailscale up --exit-node= --accept-routes
#### 📊 Menu Structure
Tailscale [✓]
Exit Node →
    None
    Node A
    Node B

Check service status \
systemctl --user status tailscale-tray.service \
View logs \
journalctl --user -u tailscale-tray.service -f \
Run manually \
~/.local/bin/tailscale-tray 

#### 🧩 Design Notes 
Built with GTK3 + AppIndicator \
Uses RadioMenuItem for exit node selection \
Uses tailscale CLI via subprocess \
Designed to be lightweight and minimal 