# 👻 Mirage Ghost Engine

> **Le Piège Invisible.**  
> Troisième pilier de l'écosystème **MIRAGE**, ce module est un moteur de déception capable de cloner des machines compromises pour y piéger les attaquants.

## ✨ Fonctionnalités clés (100% Terminées)

- ✅ **Snapshot (Jour 12)** : Capture l'identité d'une machine (Bannières, Headers).
- ✅ **Clone Virtuel (Jour 13)** : Génération automatique de Honeypots Docker.
- ✅ **Redirection (Jour 14)** : Basculement transparent via Iptables NAT.
- ✅ **Évolution (Jour 15)** : Faux fichiers, bases de données SQLite et credentials dynamiques.
- ✅ **Enregistrement (Jour 16)** : Logging temps réel de l'activité de l'attaquant.

## 🚀 Utilisation (Le Piège Complet)

Pour piéger un attaquant détecté :

```bash
sudo venv/bin/python3 ghost_orchestrator.py <IP_ATTAQUANT> <IP_CIBLE>
```

Ce script va automatiquement :
1. Prendre un snapshot de la cible.
2. Créer un clone Docker avec les mêmes headers.
3. Injecter des faux fichiers secrets dans le clone.
4. Rediriger l'attaquant vers le clone sans qu'il s'en rende compte.
5. Enregistrer ses actions.

---
© 2026 Mirage Security - "L'attaquant ne sait plus où il est."
