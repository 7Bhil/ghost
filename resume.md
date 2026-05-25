# 📝 Résumé technique : Module GHOST

**Rôle** : Le Piège (Honeypot, Déception & Enregistrement)
**État** : 100% Terminée (Jour 12-16 + Intégration Pro)

## 🚀 Fonctionnalités implémentées
- **Snapshot Identity** (`snapshot.py`) : Capture des bannières SSH et headers HTTP de la cible originale pour un clonage crédible.
- **Factory de Clones** (`clone_factory.py`) : Déploiement automatique de l'artillerie de déception :
    - **Cowrie** (SSH Honeypot Pro) : Enregistre toutes les commandes de l'attaquant.
    - **Dionaea** (Multi-protocol Honeypot Pro) : Capture les malwares SMB/SQL/FTP.
    - **Custom Nginx** : Clone web imitant parfaitement la cible originale.
- **Redirection Invisible** (`redirection.py`) : Détournement transparent du trafic attaquant via **Iptables NAT** (DNAT/SNAT).
- **Moteur d'Évolution** (`evolution_engine.py`) : Injection dynamique de faux secrets (base SQLite, fichiers `.env`, credentials PHP).
- **Honey Logging** (`honey_logger.py`) : Capture en temps réel de l'activité à l'intérieur des pièges Docker.
- **Orchestration** (`ghost_orchestrator.py`) : Déploiement de toute la chaîne de déception en une commande.

## 🛠️ Stack Technique
- **Docker / Docker-Compose** (Isolation des pièges)
- **Cowrie & Dionaea** (Honeypots standards)
- **Iptables** (Routage transparent)
- **SQLite** (Génération de fausses données)

## 📂 Fichiers clés
- `install.sh` : Configure Docker et le réseau pour Mirage.
- `clones/` : Dossier contenant les environnements de déception actifs.
