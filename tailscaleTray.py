#!/usr/bin/env python3
import gi
import subprocess

gi.require_version('Gtk', '3.0')  # AppIndicator still works with GTK3
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3

APP_ID = "tailscale-tray"

class TailscaleTray:
    def __init__(self):
        print("[INFO] Starting Tailscale tray...")
        self.indicator = AppIndicator3.Indicator.new(
            APP_ID,
            "/home/atk_frostbyte/PersonalApplications/OrnnY/TailscaleTray/tailscale-contrast.svg",  # or replace with your SVG absolute path
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.menu = Gtk.Menu()

        self.exit_menu = Gtk.Menu()
        self.exit_item = Gtk.MenuItem(label="Exit Node")
        self.exit_item.set_submenu(self.exit_menu)
        self.exit_group = []

        # "None" option
        none_item = Gtk.RadioMenuItem.new_with_label(None, "None")
        none_item.connect("toggled", self.on_exit_selected, None)
        self.exit_menu.append(none_item)
        self.exit_group.append(none_item)

        # Dynamic nodes
        for name, ip in self.get_exit_nodes():
            item = Gtk.RadioMenuItem.new_with_label(self.exit_group, name)
            item.connect("toggled", self.on_exit_selected, ip)
            self.exit_menu.append(item)

        self.menu.append(self.exit_item)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", Gtk.main_quit)
        self.menu.append(quit_item)


        self.toggle_item = Gtk.CheckMenuItem(label="Enable Tailscale")
        # self.toggle_item = Gtk.CheckMenuItem(label="Tailscale")
        self.toggle_item.set_active(self.is_tailscale_up())  # initial state
        self.toggle_item.connect("toggled", self.on_toggle)
        self.menu.append(self.toggle_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        print("[INFO] Tray initialized. Waiting for interaction...")

    def get_exit_nodes(self):
        try:
            output = subprocess.check_output(["tailscale", "status", "--json"])
            import json
            data = json.loads(output)

            nodes = []
            for peer in data.get("Peer", {}).values():
                if peer.get("ExitNodeOption"):
                    nodes.append((peer["DNSName"], peer["TailscaleIPs"][0]))

            return nodes
        except Exception as e:
            print(f"[ERROR] Failed to get exit nodes: {e}")
            return []
    
    def on_exit_selected(self, menuitem, exit_ip):
        if menuitem.get_active():
            if exit_ip is None:
                subprocess.Popen(["tailscale", "up", "--exit-node=", "--accept-routes"])
            else:
                subprocess.Popen(["tailscale", "up", f"--exit-node={exit_ip}", "--accept-routes"])

    def is_tailscale_up(self):
        try:
            output = subprocess.check_output(["tailscale", "status"], stderr=subprocess.STDOUT).decode()
            running = "running" in output.lower() or "connected" in output.lower()
            print(f"[DEBUG] tailscale status output:\n{output.strip()}")
            return running
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to check Tailscale status: {e}")
            return False
        
    def on_toggle(self, menuitem):
        if menuitem.get_active():
            subprocess.Popen(["tailscale", "up"])
        else:
            subprocess.Popen(["tailscale", "down"])

if __name__ == "__main__":
    TailscaleTray()
    Gtk.main()

