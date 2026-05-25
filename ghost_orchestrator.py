import sys
import os
import time
from snapshot import GhostSnapshot
from clone_factory import GhostCloneFactory
from redirection import GhostRedirector
from evolution_engine import EvolutionEngine
from honey_logger import HoneyLogger

class GhostOrchestrator:
    def __init__(self):
        self.workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.redirector = GhostRedirector()

    def trap_attacker(self, attacker_ip, target_ip):
        print(f"=== 👻 MIRAGE GHOST : DÉPLOIEMENT DU PIÈGE ===")
        
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
        logger = HoneyLogger(clone_id, self.workspace_root)
        log_thread = threading.Thread(target=logger.start_logging, daemon=True)
        log_thread.start()

        print(f"\n[🔥] PIÈGE ACTIF : L'attaquant {attacker_ip} est maintenant dans le labyrinthe.")
        print("Toute son activité est enregistrée.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        orch = GhostOrchestrator()
        orch.trap_attacker(sys.argv[1], sys.argv[2])
    else:
        print("Usage: sudo python3 ghost_orchestrator.py <attacker_ip> <target_ip>")
