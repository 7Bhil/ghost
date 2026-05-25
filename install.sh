#!/bin/bash
# --- MIRAGE GHOST INSTALLER ---

if [ "$EUID" -ne 0 ]; then
  echo "❌ Veuillez lancer avec sudo (nécessaire pour Docker/Iptables)"
  exit 1
fi

echo "Installation de Mirage Ghost..."

# Dépendances système
apt-get update && apt-get install -y docker.io docker-compose iptables

# Python setup
python3 -m venv venv
source venv/bin/activate
pip install requests PyYAML

echo "[+] Installation terminée."
