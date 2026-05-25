import subprocess
import threading
import json
import time
from datetime import datetime

class HoneyLogger:
    def __init__(self, clone_id, workspace_root):
        self.clone_id = clone_id
        self.log_file = os.path.join(workspace_root, f"activity_{clone_id}.json")
        self.running = False

    def start_logging(self):
        """Surveille les logs Docker en temps réel"""
        print(f"[*] Enregistrement de l'activité pour le clone {self.clone_id}...")
        self.running = True
        
        # Commande pour voir les logs d'accès Nginx par exemple
        cmd = ["docker", "logs", "-f", self.clone_id]
        
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in iter(proc.stdout.readline, ''):
                if not self.running: break
                self._process_line(line)
        except Exception as e:
            print(f"[!] Erreur Logger : {e}")

    def _process_line(self, line):
        # Transformer la ligne de log brute en Mirage Event
        entry = {
            "timestamp": datetime.now().isoformat(),
            "clone_id": self.clone_id,
            "activity": line.strip()
        }
        # En pratique, on enverrait ça à Oracle
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def stop(self):
        self.running = False
