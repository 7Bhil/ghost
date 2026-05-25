import subprocess
import threading
import json
import time
import os
from datetime import datetime

class HoneyLogger:
    def __init__(self, clone_id, workspace_root, cloud_db=None):
        self.clone_id = clone_id
        self.log_file = os.path.join(workspace_root, f"activity_{clone_id}.json")
        self.cloud_db = cloud_db
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
                if line.strip():
                    self._process_line(line)
        except Exception as e:
            print(f"[!] Erreur Logger : {e}")

    def _process_line(self, line):
        # Transformer la ligne de log brute en Mirage Event
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "clone_id": self.clone_id,
            "activity": line.strip()
        }
        
        # Log local
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except: pass

        # Log Cloud
        if self.cloud_db and self.cloud_db.db is not None:
            self.cloud_db.insert_event({
                "component": "ghost",
                "type": "attacker_activity",
                "severity": "medium",
                "message": f"Activité détectée dans le clone {self.clone_id}",
                "data": entry
            })

    def stop(self):
        self.running = False
