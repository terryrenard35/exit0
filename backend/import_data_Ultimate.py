import firebase_admin
from google.cloud import firestore
from datetime import datetime, timezone

# Initialisation Firestore
db = firestore.Client(project="friendly-cubist-480305-s6")
current_date = datetime.now(timezone.utc)

data = [
    # ==========================================
    # 🐧 LINUX SYSTEM (Administration Système)
    # ==========================================
    {"app": "linux", "issue": "disk-full-inodes", "blocks": [{"type": "text", "content": "Le disque indique qu'il est plein alors que 'df -h' montre de l'espace libre. C'est souvent un épuisement des inodes (trop de petits fichiers)."}, {"type": "code", "content": "df -i"}]},
    {"app": "linux", "issue": "find-large-files", "blocks": [{"type": "text", "content": "Trouver les 10 plus gros fichiers sur le système pour faire de la place."}, {"type": "code", "content": "du -ah / | sort -rh | head -n 10"}]},
    {"app": "linux", "issue": "memory-clear-cache", "blocks": [{"type": "text", "content": "Libérer la RAM (PageCache, dentries et inodes) sans redémarrer (Attention en prod)."}, {"type": "code", "content": "sync; echo 3 > /proc/sys/vm/drop_caches"}]},
    {"app": "linux", "issue": "port-in-use-process", "blocks": [{"type": "text", "content": "Savoir quel processus écoute sur un port spécifique (ex: 8080)."}, {"type": "code", "content": "lsof -i :8080"}]},
    {"app": "linux", "issue": "ssh-host-key-changed", "blocks": [{"type": "text", "content": "Erreur 'Remote host identification has changed'. Supprimer l'ancienne clé connue."}, {"type": "code", "content": "ssh-keygen -R <IP_ADDRESS>"}]},
    {"app": "linux", "issue": "tar-extract-gz", "blocks": [{"type": "text", "content": "Extraire une archive .tar.gz classique."}, {"type": "code", "content": "tar -xzvf archive.tar.gz"}]},
    {"app": "linux", "issue": "grep-search-string", "blocks": [{"type": "text", "content": "Chercher une chaîne de caractères récursivement dans tous les fichiers d'un dossier."}, {"type": "code", "content": "grep -rnw '/path/to/search/' -e 'pattern'"}]},
    {"app": "linux", "issue": "chmod-recursive", "blocks": [{"type": "text", "content": "Donner les droits 755 aux dossiers et 644 aux fichiers récursivement (Standard Web)."}, {"type": "code", "content": "find . -type d -exec chmod 755 {} \\;\nfind . -type f -exec chmod 644 {} \\;"}]},
    {"app": "linux", "issue": "user-add-sudo", "blocks": [{"type": "text", "content": "Ajouter un utilisateur existant au groupe sudo (Debian/Ubuntu)."}, {"type": "code", "content": "usermod -aG sudo <username>"}]},
    {"app": "linux", "issue": "watch-command", "blocks": [{"type": "text", "content": "Exécuter une commande en boucle toutes les 2 secondes pour surveiller un changement."}, {"type": "code", "content": "watch -n 2 'ls -l'"}]},

    # ==========================================
    # 🌐 NGINX (Serveur Web)
    # ==========================================
    {"app": "nginx", "issue": "413-entity-too-large", "blocks": [{"type": "text", "content": "Erreur lors de l'upload de fichiers. Il faut augmenter la limite de taille du corps de la requête."}, {"type": "code", "content": "client_max_body_size 100M; # Dans nginx.conf ou server block"}]},
    {"app": "nginx", "issue": "502-bad-gateway", "blocks": [{"type": "text", "content": "Nginx n'arrive pas à communiquer avec le backend (PHP-FPM ou Node). Vérifiez si le service backend tourne."}, {"type": "code", "content": "systemctl status php8.1-fpm"}]},
    {"app": "nginx", "issue": "test-config", "blocks": [{"type": "text", "content": "Vérifier la syntaxe de la configuration avant de redémarrer."}, {"type": "code", "content": "nginx -t"}]},
    {"app": "nginx", "issue": "redirect-www-to-non-www", "blocks": [{"type": "text", "content": "Rediriger tout le trafic www vers le domaine racine."}, {"type": "code", "content": "server_name www.example.com;\nreturn 301 $scheme://example.com$request_uri;"}]},
    {"app": "nginx", "issue": "enable-cors", "blocks": [{"type": "text", "content": "Autoriser les requêtes Cross-Origin (CORS) simples."}, {"type": "code", "content": "add_header Access-Control-Allow-Origin *;"}]},
    {"app": "nginx", "issue": "log-format-json", "blocks": [{"type": "text", "content": "Configurer les logs en JSON pour les envoyer vers ELK/Graylog."}, {"type": "code", "content": "log_format json_combined escape=json '{ \"time_local\": \"$time_local\", \"remote_addr\": \"$remote_addr\" ... }';"}]},

    # ==========================================
    # 🪶 APACHE (Serveur Web)
    # ==========================================
    {"app": "apache", "issue": "rewrite-mod-enable", "blocks": [{"type": "text", "content": "Les fichiers .htaccess ne fonctionnent pas (Erreur 404 sur les routes). Activez le mod_rewrite."}, {"type": "code", "content": "a2enmod rewrite && systemctl restart apache2"}]},
    {"app": "apache", "issue": "ah00558-fqdn", "blocks": [{"type": "text", "content": "Warning au démarrage : Could not reliably determine the server's fully qualified domain name."}, {"type": "code", "content": "echo \"ServerName localhost\" >> /etc/apache2/apache2.conf"}]},
    {"app": "apache", "issue": "allow-override-all", "blocks": [{"type": "text", "content": "Autoriser la surcharge de configuration par .htaccess dans un VirtualHost."}, {"type": "code", "content": "<Directory /var/www/html>\n    AllowOverride All\n</Directory>"}]},
    {"app": "apache", "issue": "403-forbidden-permissions", "blocks": [{"type": "text", "content": "Erreur 403. Apache n'a pas les droits de lecture sur le dossier."}, {"type": "code", "content": "chown -R www-data:www-data /var/www/html"}]},

    # ==========================================
    # 🐬 MYSQL / MARIADB (Base de données)
    # ==========================================
    {"app": "mysql", "issue": "reset-root-password", "blocks": [{"type": "text", "content": "Réinitialiser le mot de passe root perdu (méthode UPDATE)."}, {"type": "code", "content": "ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewPassword';"}]},
    {"app": "mysql", "issue": "error-1040-too-many-connections", "blocks": [{"type": "text", "content": "Le serveur refuse les connexions. Augmentez la limite dans my.cnf."}, {"type": "code", "content": "max_connections = 500"}]},
    {"app": "mysql", "issue": "dump-database", "blocks": [{"type": "text", "content": "Sauvegarder une base de données vers un fichier SQL."}, {"type": "code", "content": "mysqldump -u user -p database_name > backup.sql"}]},
    {"app": "mysql", "issue": "import-database", "blocks": [{"type": "text", "content": "Importer un fichier SQL dans une base."}, {"type": "code", "content": "mysql -u user -p database_name < backup.sql"}]},
    {"app": "mysql", "issue": "show-running-queries", "blocks": [{"type": "text", "content": "Voir les requêtes en cours d'exécution (pour débugger les lenteurs)."}, {"type": "code", "content": "SHOW FULL PROCESSLIST;"}]},
    {"app": "mysql", "issue": "grant-remote-access", "blocks": [{"type": "text", "content": "Autoriser un utilisateur à se connecter depuis une IP distante."}, {"type": "code", "content": "GRANT ALL PRIVILEGES ON *.* TO 'user'@'IP' IDENTIFIED BY 'password'; FLUSH PRIVILEGES;"}]},

    # ==========================================
    # 🐘 POSTGRESQL (Base de données)
    # ==========================================
    {"app": "postgres", "issue": "pg-hba-conf-reject", "blocks": [{"type": "text", "content": "Erreur 'no pg_hba.conf entry for host'. Il faut autoriser l'IP dans la config."}, {"type": "code", "content": "host    all             all             0.0.0.0/0            md5 # dans pg_hba.conf"}]},
    {"app": "postgres", "issue": "list-databases-cli", "blocks": [{"type": "text", "content": "Lister les bases de données via la ligne de commande psql."}, {"type": "code", "content": "\\l"}]},
    {"app": "postgres", "issue": "active-connections", "blocks": [{"type": "text", "content": "Compter le nombre de connexions actives par base."}, {"type": "code", "content": "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"}]},
    {"app": "postgres", "issue": "vacuum-full", "blocks": [{"type": "text", "content": "Récupérer l'espace disque perdu par les suppressions (bloquant !)."}, {"type": "code", "content": "VACUUM FULL;"}]},

    # ==========================================
    # ⚙️ SYSTEMD (Gestion de services)
    # ==========================================
    {"app": "systemd", "issue": "service-failed-start", "blocks": [{"type": "text", "content": "Voir les logs précis d'un service qui refuse de démarrer."}, {"type": "code", "content": "journalctl -xeu <service_name>.service"}]},
    {"app": "systemd", "issue": "list-failed-units", "blocks": [{"type": "text", "content": "Lister tous les services en échec sur le système."}, {"type": "code", "content": "systemctl --failed"}]},
    {"app": "systemd", "issue": "enable-at-boot", "blocks": [{"type": "text", "content": "Activer un service pour qu'il démarre automatiquement au boot."}, {"type": "code", "content": "systemctl enable <service_name>"}]},
    {"app": "systemd", "issue": "reload-daemon", "blocks": [{"type": "text", "content": "Recharger la configuration systemd après avoir modifié un fichier .service."}, {"type": "code", "content": "systemctl daemon-reload"}]},

    # ==========================================
    # 🐙 GIT (Version Control)
    # ==========================================
    {"app": "git", "issue": "detached-head", "blocks": [{"type": "text", "content": "Vous êtes en mode 'Detached HEAD'. Pour sauvegarder vos changements, créez une branche."}, {"type": "code", "content": "git checkout -b new-branch-name"}]},
    {"app": "git", "issue": "ignore-file-already-tracked", "blocks": [{"type": "text", "content": "Le .gitignore ne marche pas car le fichier est déjà suivi. Il faut le retirer de l'index."}, {"type": "code", "content": "git rm --cached <file>"}]},
    {"app": "git", "issue": "squash-commits", "blocks": [{"type": "text", "content": "Fusionner les 3 derniers commits en un seul (interactive rebase)."}, {"type": "code", "content": "git rebase -i HEAD~3"}]},
    {"app": "git", "issue": "force-pull-overwrite", "blocks": [{"type": "text", "content": "Abandonner les changements locaux et forcer la mise à jour depuis le serveur."}, {"type": "code", "content": "git fetch --all && git reset --hard origin/main"}]},
    {"app": "git", "issue": "tag-create-push", "blocks": [{"type": "text", "content": "Créer un tag de version et l'envoyer sur le dépôt distant."}, {"type": "code", "content": "git tag -a v1.0 -m \"Version 1.0\" && git push origin v1.0"}]},

    # ==========================================
    # 🔐 SSH (Secure Shell)
    # ==========================================
    {"app": "ssh", "issue": "permission-denied-publickey", "blocks": [{"type": "text", "content": "Vérifiez que les permissions du dossier .ssh sont correctes (très strictes)."}, {"type": "code", "content": "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"}]},
    {"app": "ssh", "issue": "copy-id-to-server", "blocks": [{"type": "text", "content": "Copier facilement votre clé publique vers un serveur distant."}, {"type": "code", "content": "ssh-copy-id user@hostname"}]},
    {"app": "ssh", "issue": "tunnel-port-forwarding", "blocks": [{"type": "text", "content": "Créer un tunnel pour accéder au port 8080 d'un serveur distant via le port 9090 local."}, {"type": "code", "content": "ssh -L 9090:localhost:8080 user@hostname"}]},
    {"app": "ssh", "issue": "keep-alive", "blocks": [{"type": "text", "content": "Éviter que la session SSH ne coupe en cas d'inactivité."}, {"type": "code", "content": "ServerAliveInterval 60 # dans ~/.ssh/config"}]},

    # ==========================================
    # 📦 NPM / NODEJS
    # ==========================================
    {"app": "npm", "issue": "eacces-permission-error", "blocks": [{"type": "text", "content": "Erreur de permission lors de l'installation globale. Ne pas utiliser sudo, mais corriger le owner."}, {"type": "code", "content": "sudo chown -R $USER /usr/local/lib/node_modules"}]},
    {"app": "npm", "issue": "peer-dependency-conflict", "blocks": [{"type": "text", "content": "Forcer l'installation malgré les conflits de versions (Attention aux bugs)."}, {"type": "code", "content": "npm install --legacy-peer-deps"}]},
    {"app": "npm", "issue": "clear-cache-force", "blocks": [{"type": "text", "content": "Nettoyer le cache NPM en cas de comportement bizarre."}, {"type": "code", "content": "npm cache clean --force"}]},
    {"app": "node", "issue": "increase-memory-limit", "blocks": [{"type": "text", "content": "Erreur 'JavaScript heap out of memory'. Augmenter la RAM allouée à Node."}, {"type": "code", "content": "export NODE_OPTIONS=\"--max-old-space-size=4096\""}]}
]

def inject():
    print(f"🔥 LANCEMENT INJECTION ULTIME : {len(data)} SOLUTIONS EXPERTES.")
    for entry in data:
        doc_ref = db.collection("applications").document(entry["app"])
        new_sol = {
            "author": "Terry Knowledge Base",
            "blocks": entry["blocks"],
            "upvotes": 0,
            "created_at": current_date
        }
        doc_ref.set({
            "application": entry["app"],
            "solutions": firestore.ArrayUnion([new_sol])
        }, merge=True)
        print(f"✅ [OK] {entry['app'].upper()} : {entry['issue']}")
    print("\n💎 BASE DE DONNÉES SYNCHRONISÉE AVEC SUCCÈS.")

if __name__ == "__main__":
    inject()
