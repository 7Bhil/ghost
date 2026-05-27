import sys
import os
import time
import threading
from snapshot import GhostSnapshot
from clone_factory import GhostCloneFactory
from redirection import GhostRedirector
from evolution_engine import EvolutionEngine
from honey_logger import HoneyLogger

# Add parent directory for database_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from database_manager import MongoAtlasManager
except ImportError:
    MongoAtlasManager = None

class GhostOrchestrator:
    def __init__(self):
        self.workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.redirector = GhostRedirector()
        self.db = MongoAtlasManager() if MongoAtlasManager else None

    def trap_attacker(self, attacker_ip, target_ip):
        print(f"===  MIRAGE GHOST : DÉPLOIEMENT DU PIÈGE ===")
        
        # Log to Cloud
        if self.db and self.db.db is not None:
            self.db.insert_event({
                "component": "ghost",
                "type": "trap_activation",
                "severity": "high",
                "target": {"ip": target_ip},
                "attacker": {"ip": attacker_ip},
                "message": f"DÉPLOIEMENT DU PIÈGE : L'attaquant {attacker_ip} est en cours de redirection vers un clone de {target_ip}."
            })
        
        # 1. Snapshot instantané
        print("[1/5] Capture de l'identité de la cible...")
        snap = GhostSnapshot(target_ip)
        snap.capture_http()
        snap.capture_ssh_banner()
        snap_path = snap.save()

        # 2. Création du clone
        print("[2/5] Construction du sosie numérique (Docker)...")
        factory = GhostCloneFactory(snap_path)
        factory.deploy()
        clone_id = factory.clone_id
        clone_dir = factory.work_dir

        # 3. Évolution (Faux fichiers/DB)
        print("[3/5] Injection des leurres (Evolution)...")
        evolve = EvolutionEngine(clone_dir)
        evolve.evolve_all()

        # 4. Redirection invisible
        print("[4/5] Activation de la redirection NAT...")
        self.redirector.activate_trap(attacker_ip, target_ip)

        # 5. Enregistrement
        print("[5/5] Lancement du film de l'attaque (Logger)...")
        logger = HoneyLogger(clone_id, self.workspace_root, cloud_db=self.db)
        log_thread = threading.Thread(target=logger.start_logging, daemon=True)
        log_thread.start()

        print(f"\n[] PIÈGE ACTIF : L'attaquant {attacker_ip} est maintenant dans le labyrinthe.")
        print("Toute son activité est enregistrée.")
    def start_daemon(self):
        """Lance Ghost en mode écoute (Démon) pour recevoir des ordres du Cloud"""
        print(f"[*]  MIRAGE GHOST : Démon d'automatisation lancé.")
        self.running = True
        while self.running:
            try:
                if self.db:
                    self.db.send_heartbeat("ghost")
                    commands = self.db.get_pending_commands("ghost")
                    for cmd in commands:
                        action = cmd.get("action")
                        attacker_ip = cmd.get("target_ip")
                        # Permettre au Cloud de spécifier quelle machine cloner
                        target_to_clone = cmd.get("clone_source") or "127.0.0.1"
                        cmd_id = cmd.get("_id")
                        
                        if action == "trap_attacker" and attacker_ip:
                            print(f"[!] ORDRE REÇU : Piéger {attacker_ip} (Source: {target_to_clone})")
                            try:
                                self.trap_attacker(attacker_ip, target_to_clone)
                                self.db.update_command_status(cmd_id, "executed", result=f"Attaquant {attacker_ip} redirigé.")
                            except Exception as e:
                                print(f"[!] Échec du piège : {e}")
                                self.db.update_command_status(cmd_id, "failed", result=str(e))
                            
                time.sleep(5)
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                print(f"[!] Erreur Ghost Daemon : {e}")
                time.sleep(10)

if __name__ == "__main__":
    orch = GhostOrchestrator()
    if "--daemon" in sys.argv:
        orch.start_daemon()
    elif len(sys.argv) > 2:
        orch.trap_attacker(sys.argv[1], sys.argv[2])
    else:
        print("Usage:")
        print("  sudo python3 ghost_orchestrator.py --daemon")
        print("  sudo python3 ghost_orchestrator.py <attacker_ip> <target_ip>")
