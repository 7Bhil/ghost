import os
import random
import json
import uuid
from datetime import datetime

class EvolutionEngine:
    """
    Moteur d'évolution pour les leurres GHOST.
    Génère dynamiquement du contenu piégé (Honey-Data) pour tracer l'attaquant.
    """
    def __init__(self, clone_path):
        self.clone_path = clone_path
        self.meta_path = os.path.join(clone_path, ".mirage_meta")
        os.makedirs(self.meta_path, exist_ok=True)
        
        # Liste des Canary Tokens générés
        self.active_tokens = []

    def _generate_canary_token(self, token_type):
        """Crée un token unique pour tracker l'utilisation d'une donnée"""
        token_id = str(uuid.uuid4())[:8]
        token = {
            "id": token_id,
            "type": token_type,
            "created_at": datetime.now().isoformat(),
            "trigger_url": f"http://mirage-oracle.local/trace/{token_id}"
        }
        self.active_tokens.append(token)
        return token

    def generate_fake_credentials(self):
        """Génère des fichiers de credentials contenant des Canary Tokens"""
        token = self._generate_canary_token("ssh_key")
        
        creds = [
            ("admin_backup.txt", f"user: admin\npass: Mirage_{token['id']}!2026\nnote: Do not use outside production."),
            (".env.production", f"DB_PASSWORD=prod_db_{token['id']}\nCLOUD_KEY=AKIA_{token['id'].upper()}GHOST"),
            ("internal_ssh_key", f"-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\n{token['id']}==\n-----END OPENSSH PRIVATE KEY-----")
        ]
        
        for filename, content in creds:
            file_path = os.path.join(self.clone_path, filename)
            with open(file_path, "w") as f:
                f.write(content)
            # Changer le timestamp pour faire croire à un vieux fichier
            os.utime(file_path, (1704067200, 1704067200)) 

    def generate_fake_database(self):
        """Génère une DB SQLite 'piégée' avec des entrées traçables"""
        import sqlite3
        token = self._generate_canary_token("sql_data")
        db_path = os.path.join(self.clone_path, "prod_users.db")
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('CREATE TABLE users (id INTEGER, login TEXT, email TEXT, secret_token TEXT)')
        
        # Insertion de données réalistes
        users = [
            (1, "ceo_admin", "boss@company.com", f"SECRET_{token['id']}"),
            (2, "dev_lead", "dev@company.com", "NOT_A_TOKEN"),
            (3, "hr_manager", "hr@company.com", f"TOKEN_{uuid.uuid4().hex[:6]}")
        ]
        c.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)
        
        conn.commit()
        conn.close()

    def add_labyrinthe_files(self):
        """Crée une arborescence complexe pour ralentir l'attaquant (Tarpit)"""
        base = os.path.join(self.clone_path, "mnt/backups")
        os.makedirs(base, exist_ok=True)
        
        folders = ["daily", "weekly", "monthly", "emergency", "deprecated"]
        for folder in folders:
            path = os.path.join(base, folder)
            os.makedirs(path, exist_ok=True)
            for i in range(10):
                dummy_file = os.path.join(path, f"backup_2025_{i}.tar.gz")
                with open(dummy_file, "wb") as f:
                    f.write(os.urandom(1024)) # Remplissage aléatoire

    def save_meta(self):
        """Sauvegarde les tokens générés pour qu'ORACLE puisse les surveiller"""
        with open(os.path.join(self.meta_path, "tokens.json"), "w") as f:
            json.dump(self.active_tokens, f, indent=4)

    def evolve_all(self):
        print(f"[*] Amélioration stratégique du leurre dans {self.clone_path}...")
        self.generate_fake_credentials()
        self.generate_fake_database()
        self.add_labyrinthe_files()
        self.save_meta()
        print("[+] Leurre prêt : Données piégées et labyrinthe opérationnel.")

if __name__ == "__main__":
    # Test rapide
    engine = EvolutionEngine("./test_clone")
    engine.evolve_all()
