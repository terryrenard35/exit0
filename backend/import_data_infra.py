import firebase_admin
from google.cloud import firestore
from datetime import datetime, timezone

# Initialisation Firestore
db = firestore.Client(project="friendly-cubist-480305-s6")
current_date = datetime.now(timezone.utc)

data = [
    # --- ACTIVE DIRECTORY (10 solutions) ---
    {"app": "active-directory", "issue": "dfsr-moribund-state", "blocks": [{"type": "text", "content": "Dossier SYSVOL bloqué en état 'Moribund'. Réinitialisation forcée du service DFSR via le registre (D4/D2)."}, {"type": "code", "content": "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\DFSR\\Parameters\\SysVols\\Seeding Content' -Name 'IsAuthoritative' -Value 1"}]},
    {"app": "active-directory", "issue": "kerberos-token-bloat", "blocks": [{"type": "text", "content": "Utilisateur membre de trop de groupes. Augmentation du MaxTokenSize dans le registre."}, {"type": "code", "content": "New-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Lsa\\Kerberos\\Parameters' -Name 'MaxTokenSize' -Value 65535 -PropertyType DWord"}]},
    {"app": "active-directory", "issue": "dns-srv-missing", "blocks": [{"type": "text", "content": "Enregistrements SRV manquants pour le DC. Force le ré-enregistrement."}, {"type": "code", "content": "nltest /dsregdns"}]},
    {"app": "active-directory", "issue": "locked-out-source-find", "blocks": [{"type": "text", "content": "Identifier la machine source d'un verrouillage de compte."}, {"type": "code", "content": "Get-WinEvent -FilterHashtable @{LogName='Security';ID=4740} | Select-Object -First 1 | fl"}]},
    {"app": "active-directory", "issue": "rid-master-check", "blocks": [{"type": "text", "content": "Vérifier la santé du maître RID pour la création d'objets."}, {"type": "code", "content": "dcdiag /test:ridmanager /v"}]},
    {"app": "active-directory", "issue": "fsmo-role-transfer", "blocks": [{"type": "text", "content": "Transférer les rôles FSMO vers un nouveau DC."}, {"type": "code", "content": "Move-ADDirectoryServerOperationMasterRole -Identity <NewDC> -OperationMasterRole 0,1,2,3,4"}]},
    {"app": "active-directory", "issue": "lingering-objects-cleanup", "blocks": [{"type": "text", "content": "Suppression des objets persistants après une période de 'Tombstone' expirée."}, {"type": "code", "content": "repadmin /removelingeringobjects <Dest_DC_GUID> <Source_DC_GUID> <NC_DN>"}]},
    {"app": "active-directory", "issue": "adprep-forest-update", "blocks": [{"type": "text", "content": "Préparer la forêt pour l'ajout d'un DC plus récent (ex: 2022)."}, {"type": "code", "content": "adprep.exe /forestprep"}]},
    {"app": "active-directory", "issue": "check-secure-channel", "blocks": [{"type": "text", "content": "Vérifier le canal de sécurité entre un serveur membre et le DC."}, {"type": "code", "content": "Test-ComputerSecureChannel -Verbose"}]},
    {"app": "active-directory", "issue": "find-inactive-computers", "blocks": [{"type": "text", "content": "Lister les ordinateurs inactifs depuis plus de 90 jours."}, {"type": "code", "content": "Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 -ComputersOnly"}]},

    # --- DNS WINDOWS (10 solutions) ---
    {"app": "dns-windows", "issue": "scavenging-stale-records", "blocks": [{"type": "text", "content": "Supprimer manuellement les enregistrements DNS obsolètes."}, {"type": "code", "content": "dnscmd /zonerefresh <ZoneName>"}]},
    {"app": "dns-windows", "issue": "cache-poisoning-protection", "blocks": [{"type": "text", "content": "Activer la sécurisation contre la pollution du cache."}, {"type": "code", "content": "dnscmd /config /securecache 1"}]},
    {"app": "dns-windows", "issue": "root-hints-update", "blocks": [{"type": "text", "content": "Mettre à jour les indices de racine DNS."}, {"type": "code", "content": "dnscmd /writerootHints <IP_Root_Server>"}]},
    {"app": "dns-windows", "issue": "conditional-forwarder-fix", "blocks": [{"type": "text", "content": "Réinitialiser un redirecteur conditionnel pour un domaine partenaire."}, {"type": "code", "content": "dnscmd /zoneresetmasters <DomainName> /f <IP1> <IP2>"}]},
    {"app": "dns-windows", "issue": "debug-logging-enable", "blocks": [{"type": "text", "content": "Activer les logs de débug DNS pour traquer les requêtes."}, {"type": "code", "content": "dnscmd /config /loglevel 0x81000001"}]},
    {"app": "dns-windows", "issue": "zone-transfer-test", "blocks": [{"type": "text", "content": "Tester le transfert de zone AXFR."}, {"type": "code", "content": "nslookup -type=axfr <ZoneName> <DNS_Server>"}]},
    {"app": "dns-windows", "issue": "ptr-registration-fail", "blocks": [{"type": "text", "content": "Forcer l'enregistrement de l'enregistrement inverse (PTR)."}, {"type": "code", "content": "ipconfig /registerdns"}]},
    {"app": "dns-windows", "issue": "delegation-check", "blocks": [{"type": "text", "content": "Vérifier la délégation vers un sous-domaine."}, {"type": "code", "content": "dnscmd /enumzones"}]},
    {"app": "dns-windows", "issue": "clear-server-cache", "blocks": [{"type": "text", "content": "Vider totalement le cache récursif du serveur."}, {"type": "code", "content": "dnscmd /clearcache"}]},
    {"app": "dns-windows", "issue": "edns-tuning", "blocks": [{"type": "text", "content": "Désactiver EDNS si les firewalls bloquent les paquets DNS > 512 octets."}, {"type": "code", "content": "dnscmd /config /enableednsprobes 0"}]},

    # --- SUPERVISION (ZABBIX/PRTG) & NOTES DE FRAIS (LUCCA/NOTILUS) (10 solutions) ---
    {"app": "zabbix", "issue": "unreachable-poller-busy", "blocks": [{"type": "text", "content": "Augmenter le nombre de processus pour les hôtes injoignables."}, {"type": "code", "content": "StartPollersUnreachable=10 # dans zabbix_server.conf"}]},
    {"app": "zabbix", "issue": "database-down-slow", "blocks": [{"type": "text", "content": "Optimiser MySQL pour Zabbix (InnoDb Buffer Pool)."}, {"type": "code", "content": "innodb_buffer_pool_size = <75% RAM>"}]},
    {"app": "prtg", "issue": "wmi-connectivity-issue", "blocks": [{"type": "text", "content": "Réparer le dépôt WMI corrompu sur le serveur cible."}, {"type": "code", "content": "winmgmt /salvagerepository"}]},
    {"app": "prtg", "issue": "sensor-limit-warning", "blocks": [{"type": "text", "content": "La sonde PRTG Core sature. Déplacer des capteurs vers une sonde distante (Remote Probe)."}, {"type": "code", "content": "PRTG_Remote_Probe_Installer.exe"}]},
    {"app": "lucca-cleemy", "issue": "accounting-export-fail", "blocks": [{"type": "text", "content": "Code journal ou compte comptable manquant dans l'export Lucca."}, {"type": "code", "content": "LOG: Missing_GL_Account_Code"}]},
    {"app": "lucca-cleemy", "issue": "ik-mapping-error", "blocks": [{"type": "text", "content": "Grille IK non trouvée pour l'année fiscale en cours."}, {"type": "code", "content": "FIX: Update_Fiscal_IK_Grid"}]},
    {"app": "notilus", "issue": "sso-saml-auth-fail", "blocks": [{"type": "text", "content": "Certificat de fédération SAML expiré pour l'accès Notilus."}, {"type": "code", "content": "CHECK: Metadata_XML_Expiry"}]},
    {"app": "notilus", "issue": "erp-connector-stuck", "blocks": [{"type": "text", "content": "Flux d'intégration bloqué. Redémarrer le service de connecteur Notilus."}, {"type": "code", "content": "Restart-Service 'NotilusConnector'"}]},
    {"app": "supervision", "issue": "snmp-v3-auth-fail", "blocks": [{"type": "text", "content": "Échec d'auth SNMPv3. Vérifiez l'engineID et l'algorithme (SHA/AES)."}, {"type": "code", "content": "snmpwalk -v 3 -u <user> -l authPriv -a SHA -A <pass> <IP>"}]},
    {"app": "active-directory", "issue": "ntp-time-skew", "blocks": [{"type": "text", "content": "Décalage horaire trop important avec le PDC Master (Kerberos error)."}, {"type": "code", "content": "w32tm /resync /force"}]}
]

def inject():
    print(f"⏳ Injection de 30 solutions expertes dans Exit0...")
    for entry in data:
        doc_ref = db.collection("applications").document(entry["app"])
        new_sol = {
            "author": "Terry Ops Intelligence",
            "blocks": entry["blocks"],
            "upvotes": 0,
            "created_at": current_date
        }
        doc_ref.set({
            "application": entry["app"],
            "solutions": firestore.ArrayUnion([new_sol])
        }, merge=True)
        print(f"✅ Ajouté : {entry['app']} -> {entry['issue']}")
    print("\n✨ Base de données massivement peuplée avec succès.")

if __name__ == "__main__":
    inject()
