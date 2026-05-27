import subprocess
import os
import re

class GhostRedirector:
    def __init__(self):
        self.interface = "eth0" # À adapter selon l'interface réseau active

    def _is_valid_ip(self, ip):
        """Valide le format d'une IP pour éviter les injections"""
        return re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip) is not None

    def _run_cmd(self, cmd_list):
        """Exécute une commande de manière sécurisée (sans shell=True)"""
        try:
            # Utilisation de listes au lieu de chaînes pour éviter les injections
            subprocess.run(cmd_list, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            print(f"[!] Erreur Commande : {e.stderr.decode()}")
            return False

    def activate_trap(self, attacker_ip, target_ip, clone_port=8080):
        """
        Redirige tout le trafic venant de l'attaquant vers le port du clone Docker.
        """
        if not self._is_valid_ip(attacker_ip) or not self._is_valid_ip(target_ip):
            print("[!] IP invalide détectée. Annulation du piège.")
            return False

        print(f"[ GHOST] Activation du piège pour l'attaquant {attacker_ip}...")
        
        # 1. Permettre le routage local
        self._run_cmd(["sudo", "sysctl", "-w", "net.ipv4.conf.all.route_localnet=1"])
        
        # 2. Redirection entrante (DNAT)
        dnat_cmd = [
            "sudo", "iptables", "-t", "nat", "-A", "PREROUTING", 
            "-s", attacker_ip, "-d", target_ip, 
            "-p", "tcp", "--dport", "80", 
            "-j", "DNAT", "--to-destination", f"127.0.0.1:{clone_port}"
        ]
        
        # 3. Masquage pour le retour (SNAT)
        snat_cmd = [
            "sudo", "iptables", "-t", "nat", "-A", "POSTROUTING", 
            "-p", "tcp", "--dport", str(clone_port), "-d", "127.0.0.1", 
            "-j", "SNAT", "--to-source", target_ip
        ]

        if self._run_cmd(dnat_cmd) and self._run_cmd(snat_cmd):
            print(f"[] Redirection active : {attacker_ip} est maintenant piégé dans le clone.")
            return True
        return False

    def clear_traps(self):
        """Nettoie toutes les règles de redirection Ghost"""
        print("[*] Nettoyage des redirections Iptables...")
        self._run_cmd(["sudo", "iptables", "-t", "nat", "-F"])
        print("[+] Table NAT nettoyée.")

if __name__ == "__main__":
    import sys
    redirector = GhostRedirector()
    if len(sys.argv) > 2:
        redirector.activate_trap(sys.argv[1], sys.argv[2])
    elif "--clear" in sys.argv:
        redirector.clear_traps()
    else:
        print("Usage: sudo python3 redirection.py <attacker_ip> <target_ip>")
