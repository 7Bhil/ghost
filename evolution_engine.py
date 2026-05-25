import os
import random

class EvolutionEngine:
    def __init__(self, clone_path):
        self.clone_path = clone_path
        self.decoys_path = os.path.join(clone_path, "decoys")
        if not os.path.exists(self.decoys_path):
            os.makedirs(self.decoys_path)

    def generate_fake_credentials(self):
        """Génère de faux fichiers de credentials irrésistibles"""
        creds = [
            ("admin_backup.txt", "admin:Admin1234!\nroot:toor\ndb_user:super_secret_pwd"),
            (".env.production", "DB_PASSWORD=mirage_fake_db_pass\nAWS_SECRET_KEY=AKIA_GHOST_TRAP_EXAMPLE"),
            ("config.php.bak", "<?php\n$db_pass = 'sql_prod_2026_secure';\n?>")
        ]
        for filename, content in creds:
            with open(os.path.join(self.clone_path, filename), "w") as f:
                f.write(content)
        print(f"[+] Évolution : Credentials générés dans {self.clone_path}")

    def generate_fake_database(self):
        """Génère une fausse base de données SQLite remplie de données inutiles"""
        import sqlite3
        db_path = os.path.join(self.clone_path, "customers.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('CREATE TABLE users (id INTEGER, username TEXT, email TEXT, credit_card TEXT)')
        
        # Insérer 100 faux utilisateurs
        for i in range(100):
            c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', 
                      (i, f"user_{i}", f"user_{i}@company-corp.com", f"4506-{random.randint(1000,9999)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"))
        
        conn.commit()
        conn.close()
        print(f"[+] Évolution : Fausse base de données 'customers.db' générée.")

    def add_labyrinthe_files(self):
        """Crée un labyrinthe de dossiers pour perdre l'attaquant"""
        base = os.path.join(self.clone_path, "secrets")
        for i in range(5):
            path = os.path.join(base, f"vault_{i}")
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, "hint.txt"), "w") as f:
                f.write(f"The real data is in vault_{random.randint(0,10)}")
        print(f"[+] Évolution : Labyrinthe de fichiers créé.")

    def evolve_all(self):
        self.generate_fake_credentials()
        self.generate_fake_database()
        self.add_labyrinthe_files()
