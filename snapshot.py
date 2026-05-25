import requests
import socket
import json
import os
from datetime import datetime

class GhostSnapshot:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.timestamp = datetime.now().isoformat()
        self.snapshot_data = {
            "target": target_ip,
            "timestamp": self.timestamp,
            "services": {}
        }

    def capture_http(self, port=80):
        """Capture les headers et le titre d'un service web"""
        url = f"http://{self.target_ip}:{port}"
        try:
            response = requests.get(url, timeout=3)
            self.snapshot_data["services"]["http"] = {
                "port": port,
                "headers": dict(response.headers),
                "status_code": response.status_code,
                "content_preview": response.text[:500] # Petit aperçu pour le clone
            }
            print(f"[+] Snapshot HTTP réussi sur le port {port}")
        except Exception as e:
            print(f"[-] Échec capture HTTP : {e}")

    def capture_ssh_banner(self, port=22):
        """Récupère la bannière de version SSH"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((self.target_ip, port))
            banner = s.recv(1024).decode().strip()
            s.close()
            self.snapshot_data["services"]["ssh"] = {
                "port": port,
                "banner": banner
            }
            print(f"[+] Snapshot SSH réussi : {banner}")
        except Exception as e:
            print(f"[-] Échec capture SSH : {e}")

    def save(self, folder="snapshots"):
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = f"snapshot_{self.target_ip.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = os.path.join(folder, filename)
        with open(path, 'w') as f:
            json.dump(self.snapshot_data, f, indent=4)
        print(f"[✅] Snapshot sauvegardé dans : {path}")
        return path

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    snap = GhostSnapshot(target)
    snap.capture_http()
    snap.capture_ssh_banner()
    snap.save()
