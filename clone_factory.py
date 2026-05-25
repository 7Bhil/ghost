import json
import os
import subprocess

class GhostCloneFactory:
    def __init__(self, snapshot_path=None):
        self.snapshot = None
        if snapshot_path and os.path.exists(snapshot_path):
            with open(snapshot_path, 'r') as f:
                self.snapshot = json.load(f)
            self.target_ip = self.snapshot['target']
        else:
            self.target_ip = "generic_target"

        self.clone_id = f"ghost_{self.target_ip.replace('.', '_')}"
        self.work_dir = os.path.join("clones", self.clone_id)
        os.makedirs(self.work_dir, exist_ok=True)

    def deploy_cowrie(self):
        """Déploie un honeypot SSH Cowrie (Standard Industriel)"""
        print("[*] Déploiement du honeypot SSH Cowrie...")
        docker_compose = {
            "version": "3",
            "services": {
                "cowrie": {
                    "image": "cowrie/cowrie:latest",
                    "container_name": f"{self.clone_id}_ssh",
                    "ports": ["2222:2222"], # Port interne de cowrie
                    "restart": "always"
                }
            }
        }
        with open(os.path.join(self.work_dir, "docker-compose-ssh.yml"), "w") as f:
            json.dump(docker_compose, f, indent=4)
        
        subprocess.run(["docker", "compose", "-f", "docker-compose-ssh.yml", "up", "-d"], cwd=self.work_dir)
        print("[✅] Cowrie SSH est actif.")

    def deploy_dionaea(self):
        """Déploie un honeypot multi-services Dionaea"""
        print("[*] Déploiement du honeypot multi-services Dionaea...")
        docker_compose = {
            "version": "3",
            "services": {
                "dionaea": {
                    "image": "dinotools/dionaea:latest",
                    "container_name": f"{self.clone_id}_multi",
                    "ports": ["21:21", "445:445", "1433:1433", "3306:3306"],
                    "restart": "always"
                }
            }
        }
        with open(os.path.join(self.work_dir, "docker-compose-multi.yml"), "w") as f:
            json.dump(docker_compose, f, indent=4)
        
        subprocess.run(["docker", "compose", "-f", "docker-compose-multi.yml", "up", "-d"], cwd=self.work_dir)
        print("[✅] Dionaea est actif (FTP, SMB, MSSQL, MySQL).")

    def deploy_custom_web(self):
        """Génère un clone web Nginx basé sur le snapshot (déjà implémenté)"""
        if not self.snapshot or "http" not in self.snapshot['services']:
            return
        # ... (logique Nginx précédente)
        print("[*] Déploiement du clone Web personnalisé...")

    def deploy_pro_suite(self):
        """Lance l'artillerie lourde pour piéger l'attaquant"""
        self.deploy_cowrie()
        self.deploy_dionaea()
        if self.snapshot:
            self.deploy_custom_web()

if __name__ == "__main__":
    factory = GhostCloneFactory()
    factory.deploy_pro_suite()
