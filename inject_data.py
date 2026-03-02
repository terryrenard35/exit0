import firebase_admin
from firebase_admin import credentials, firestore

# Initialisation (Assure-toi d'avoir ton serviceAccountKey.json dans le dossier)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Bibliothèque de connaissances Ops 
knowledge_base = {
    "terraform-state": {
        "description": "Réparer un state Terraform bloqué ou corrompu",
        "blocks": [
            {"type": "text", "content": "Libérer manuellement un verrou (lock) sur le state S3/Azure."},
            {"type": "code", "content": "terraform force-unlock <LOCK_ID>"},
            {"type": "text", "content": "Importer une ressource existante dans le state pour éviter la destruction."},
            {"type": "code", "content": "terraform import <RESOURCE_ID> <PROVIDER_ID>"}
        ]
    },
    "aws-s3-security": {
        "description": "Audit rapide des permissions publiques S3",
        "blocks": [
            {"type": "text", "content": "Lister tous les buckets S3 qui n'ont pas le blocage public activé."},
            {"type": "code", "content": "aws s3api get-public-access-block --bucket <name>"}
        ]
    },
    "security-pentest": {
        "description": "Scanner de vulnérabilités réseau rapide",
        "blocks": [
            {"type": "text", "content": "Détecter les versions de services et l'OS d'une cible."},
            {"type": "code", "content": "nmap -sV -O -T4 <target_ip>"},
            {"type": "text", "content": "Chercher les vulnérabilités connues (scripts NSE)."},
            {"type": "code", "content": "nmap --script vuln <target_ip>"}
        ]
    },
    "azure-ad-connect": {
        "description": "Forcer la synchronisation Azure AD Connect",
        "blocks": [
            {"type": "text", "content": "Déclencher un cycle de synchronisation Delta (modifications uniquement)."},
            {"type": "code", "content": "Start-ADSyncSyncCycle -PolicyType Delta"},
            {"type": "text", "content": "Forcer une synchronisation complète (Full)."},
            {"type": "code", "content": "Start-ADSyncSyncCycle -PolicyType Initial"}
        ]
    },
    "nginx-tuning": {
        "description": "Optimiser Nginx pour les fortes charges",
        "blocks": [
            {"type": "text", "content": "Augmenter le nombre de connexions simultanées par worker."},
            {"type": "code", "content": "worker_connections 1024;"},
            {"type": "text", "content": "Activer la compression Gzip pour réduire la bande passante."},
            {"type": "code", "content": "gzip on; gzip_types text/plain application/xml;"}
        ]
    },
    "linux-disk-full": {
        "description": "Trouver les fichiers géants qui saturent le disque",
        "blocks": [
            {"type": "text", "content": "Lister les 10 plus gros dossiers à partir de la racine."},
            {"type": "code", "content": "du -ah / | sort -rh | head -n 10"},
            {"type": "text", "content": "Vérifier les fichiers ouverts mais supprimés (ghost files)."},
            {"type": "code", "content": "lsof +L1"}
        ]
    },
    "ansible-debug": {
        "description": "Tester la connectivité sur un inventaire",
        "blocks": [
            {"type": "text", "content": "Lancer un ping module sur tous les serveurs du groupe 'web'."},
            {"type": "code", "content": "ansible web -m ping"},
            {"type": "text", "content": "Récupérer tous les facts (hardware/IP) d'une machine."},
            {"type": "code", "content": "ansible <hostname> -m setup"}
        ]
    },
    "windows-port-check": {
        "description": "Équivalent de Netcat sur Windows (PowerShell)",
        "blocks": [
            {"type": "text", "content": "Tester si un port distant est ouvert sans installer d'outil tiers."},
            {"type": "code", "content": "Test-NetConnection -ComputerName <IP> -Port 443"}
        ]
    },
    "git-cleanup": {
        "description": "Nettoyer les branches locales fusionnées",
        "blocks": [
            {"type": "text", "content": "Supprimer toutes les branches locales qui ont déjà été mergées dans master."},
            {"type": "code", "content": "git branch --merged | grep -v '\\*' | xargs -n 1 git branch -d"}
        ]
    },
    "redis-performance": {
        "description": "Monitorer les requêtes Redis en temps réel",
        "blocks": [
            {"type": "text", "content": "Voir toutes les commandes reçues par le serveur (attention en prod)."},
            {"type": "code", "content": "redis-cli monitor"}
        ]
    }
}

# Injection dans Firestore
print("🛰️ Synchronisation de la base de données EXIT0...")

for app_id, content in knowledge_base.items():
    doc_ref = db.collection("applications").document(app_id)
    doc_ref.set({
        "application": app_id,
        "solutions": [{
            "author": "System Architect",
            "blocks": content["blocks"]
        }]
    })
    print(f"📦 Indexé : {app_id}")

print("\n🚀 Transfert terminé. Ton terminal de recherche est prêt.")
