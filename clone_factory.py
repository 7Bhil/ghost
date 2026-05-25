import json
import os
import subprocess

class GhostCloneFactory:
    def __init__(self, snapshot_path):
        with open(snapshot_path, 'r') as f:
            self.snapshot = json.load(f)
        self.target_ip = self.snapshot['target']
        self.clone_id = f"ghost_{self.target_ip.replace('.', '_')}"
        self.work_dir = os.path.join("clones", self.clone_id)
        
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)

    def generate_web_clone(self):
        """Génère un serveur web (Nginx) qui imite le snapshot"""
        if "http" not in self.snapshot['services']:
            return False

        http_data = self.snapshot['services']['http']
        
        # Créer une page d'accueil qui ressemble à l'originale
        html_content = f"<!-- Mirage Ghost Clone -->\n{http_data.get('content_preview', 'Welcome')}"
        with open(os.path.join(self.work_dir, "index.html"), "w") as f:
            f.write(html_content)

        # Config Nginx pour injecter les headers originaux (illusion parfaite)
        headers_config = ""
        for key, value in http_data.get('headers', {}).items():
            if key.lower() not in ['content-length', 'content-encoding', 'transfer-encoding']:
                headers_config += f'    add_header "{key}" "{value}";\n'

        nginx_conf = f"""
server {{
    listen 80;
    location / {{
        root /usr/share/nginx/html;
        index index.html;
{headers_config}
    }}
}}
"""
        with open(os.path.join(self.work_dir, "nginx.conf"), "w") as f:
            f.write(nginx_conf)
        return True

    def generate_ssh_clone(self):
        """Génère un serveur SSH avec la même bannière"""
        if "ssh" not in self.snapshot['services']:
            return False
        
        banner = self.snapshot['services']['ssh'].get('banner', 'SSH-2.0-OpenSSH_8.9')
        # On crée un fichier de bannière pour SSH
        with open(os.path.join(self.work_dir, "ssh_banner"), "w") as f:
            f.write(banner + "\n")
        return True

    def deploy(self):
        """Lance le clone via Docker Compose"""
        print(f"[*] Déploiement du clone Ghost pour {self.target_ip}...")
        
        has_web = self.generate_web_clone()
        has_ssh = self.generate_ssh_clone()

        docker_compose = {
            "version": "3.8",
            "services": {
                "clone": {
                    "container_name": self.clone_id,
                    "image": "nginx:alpine" if has_web else "alpine",
                    "ports": [],
                    "restart": "always"
                }
            }
        }

        if has_web:
            docker_compose["services"]["clone"]["volumes"] = [
                f"./index.html:/usr/share/nginx/html/index.html:ro",
                f"./nginx.conf:/etc/nginx/conf.d/default.conf:ro"
            ]
            docker_compose["services"]["clone"]["ports"].append("8080:80")

        # Pour la démo, on utilise un port mappé, la redirection IP se fera au Jour 14
        
        with open(os.path.join(self.work_dir, "docker-compose.yml"), "w") as f:
            json.dump(docker_compose, f, indent=4) # Simplifié pour l'exemple, yaml est mieux

        # Lancer le conteneur
        try:
            subprocess.run(["docker", "compose", "up", "-d"], cwd=self.work_dir, check=True)
            print(f"[✅] Clone déployé avec succès. ID: {self.clone_id}")
        except Exception as e:
            print(f"[!] Erreur déploiement Docker : {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        factory = GhostCloneFactory(sys.argv[1])
        factory.deploy()
    else:
        print("Usage: python3 clone_factory.py <snapshot_json>")
