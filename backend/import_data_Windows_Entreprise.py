import firebase_admin
from google.cloud import firestore
from datetime import datetime, timezone

# Initialisation Firestore
# Assure-toi d'être authentifié via 'gcloud auth application-default login'
db = firestore.Client(project="friendly-cubist-480305-s6")
current_date = datetime.now(timezone.utc)

data = [
    # ==========================================
    # 🪟 WINDOWS 10 / 11 (Support Workstation)
    # ==========================================
    {"app": "windows-10", "issue": "update-stuck", "blocks": [{"type": "text", "content": "Réinitialiser complètement les composants Windows Update bloqués."}, {"type": "code", "content": "net stop wuauserv\nnet stop cryptSvc\nnet stop bits\nnet stop msiserver\nRen C:\\Windows\\SoftwareDistribution SoftwareDistribution.old\nnet start wuauserv"}]},
    {"app": "windows-11", "issue": "tpm-missing-bios", "blocks": [{"type": "text", "content": "Vérifier l'état du TPM (Trusted Platform Module) pour BitLocker ou Hello."}, {"type": "code", "content": "get-tpm"}]},
    {"app": "windows-10", "issue": "printer-spooler-stuck", "blocks": [{"type": "text", "content": "Débloquer une file d'impression récalcitrante en vidant le dossier spool."}, {"type": "code", "content": "net stop spooler\ndel /Q /F /S \"%systemroot%\\System32\\Spool\\Printers\\*.*\"\nnet start spooler"}]},
    {"app": "windows-11", "issue": "network-profile-private", "blocks": [{"type": "text", "content": "Passer le réseau de 'Public' à 'Privé' (pour autoriser le partage/ping)."}, {"type": "code", "content": "Set-NetConnectionProfile -Name \"Ethernet\" -NetworkCategory Private"}]},
    {"app": "windows-10", "issue": "windows-activation-kms", "blocks": [{"type": "text", "content": "Forcer l'activation Windows via le serveur KMS de l'entreprise."}, {"type": "code", "content": "slmgr /skms <kms_server_ip>:1688\nslmgr /ato"}]},
    {"app": "windows-11", "issue": "bitlocker-recovery-key", "blocks": [{"type": "text", "content": "Récupérer la clé de récupération BitLocker locale."}, {"type": "code", "content": "manage-bde -protectors -get C:"}]},
    {"app": "windows-10", "issue": "sfc-scannow-dism", "blocks": [{"type": "text", "content": "Réparer l'image système Windows corrompue (quand sfc échoue)."}, {"type": "code", "content": "DISM /Online /Cleanup-Image /RestoreHealth"}]},
    {"app": "windows-11", "issue": "blue-screen-driver", "blocks": [{"type": "text", "content": "Lister tous les drivers installés pour identifier celui qui crash."}, {"type": "code", "content": "driverquery /v"}]},

    # ==========================================
    # 🏢 ACTIVE DIRECTORY & DNS MICROSOFT
    # ==========================================
    {"app": "active-directory", "issue": "account-lockout-source", "blocks": [{"type": "text", "content": "Trouver quel PC verrouille un compte utilisateur (Event 4740)."}, {"type": "code", "content": "Get-WinEvent -FilterHashtable @{LogName='Security';ID=4740} | Select-Object -First 1 | Format-List"}]},
    {"app": "active-directory", "issue": "recycle-bin-restore", "blocks": [{"type": "text", "content": "Restaurer un utilisateur supprimé (si la corbeille AD est active)."}, {"type": "code", "content": "Get-ADObject -Filter 'isDeleted -eq $true' -IncludeDeletedObjects | Restore-ADObject"}]},
    {"app": "active-directory", "issue": "replication-summary", "blocks": [{"type": "text", "content": "Obtenir un résumé rapide de l'état de réplication de la forêt."}, {"type": "code", "content": "repadmin /replsummary"}]},
    {"app": "active-directory", "issue": "last-logon-time", "blocks": [{"type": "text", "content": "Trouver la vraie date de dernière connexion (en interrogeant tous les DC)."}, {"type": "code", "content": "Get-ADUser -Identity <user> -Properties LastLogon | SelectName, @{N='LastLogon'; E={[DateTime]::FromFileTime($_.LastLogon)}}"}]},
    {"app": "microsoft-dns", "issue": "clear-server-cache", "blocks": [{"type": "text", "content": "Vider le cache du SERVEUR DNS (pas du client)."}, {"type": "code", "content": "Clear-DnsServerCache -Force"}]},
    {"app": "microsoft-dns", "issue": "stale-records-scavenging", "blocks": [{"type": "text", "content": "Forcer le nettoyage des enregistrements obsolètes immédiatement."}, {"type": "code", "content": "Start-DnsServerScavenging -Verbose"}]},
    {"app": "microsoft-dns", "issue": "export-zone-file", "blocks": [{"type": "text", "content": "Exporter une zone DNS complète vers un fichier texte."}, {"type": "code", "content": "dnscmd /ZoneExport <ZoneName> <FileName>"}]},

    # ==========================================
    # ☁️ OFFICE 365 / EXCHANGE ONLINE
    # ==========================================
    {"app": "office-365", "issue": "hard-delete-recovery", "blocks": [{"type": "text", "content": "Récupérer des éléments supprimés définitivement (Shift+Del) dans Exchange Online."}, {"type": "code", "content": "Restore-RecoverableItems -Identity <UserEmail> -SubjectContains \"Important\""}]},
    {"app": "office-365", "issue": "shared-mailbox-conversion", "blocks": [{"type": "text", "content": "Convertir une boîte utilisateur en boîte partagée (libère la licence)."}, {"type": "code", "content": "Set-Mailbox -Identity <Email> -Type Shared"}]},
    {"app": "office-365", "issue": "mfa-status-check", "blocks": [{"type": "text", "content": "Vérifier le statut MFA (Multi-Factor Auth) pour un utilisateur."}, {"type": "code", "content": "Get-MsolUser -UserPrincipalName <UPN> | Select-Object StrongAuthenticationRequirements"}]},
    {"app": "office-365", "issue": "full-access-permission", "blocks": [{"type": "text", "content": "Donner l'accès complet (Full Access) à une boîte mail."}, {"type": "code", "content": "Add-MailboxPermission -Identity <TargetMailbox> -User <UserWhoNeedsAccess> -AccessRights FullAccess -InheritanceType All"}]},
    {"app": "office-365", "issue": "smtp-auth-enable", "blocks": [{"type": "text", "content": "Activer l'authentification SMTP pour une imprimante ou un scanner."}, {"type": "code", "content": "Set-CASMailbox -Identity <Email> -SmtpClientAuthenticationDisabled $false"}]},

    # ==========================================
    # 🖥️ MICROSOFT RDS (Remote Desktop Services)
    # ==========================================
    {"app": "microsoft-rds", "issue": "shadow-session", "blocks": [{"type": "text", "content": "Prendre le contrôle (Shadow) d'une session utilisateur à distance."}, {"type": "code", "content": "mstsc /shadow:<SessionID> /v:<ServerName> /control"}]},
    {"app": "microsoft-rds", "issue": "license-server-diag", "blocks": [{"type": "text", "content": "Diagnostiquer les problèmes de licence CAL RDS."}, {"type": "code", "content": "Get-RDLicenseConfiguration"}]},
    {"app": "microsoft-rds", "issue": "user-logoff-force", "blocks": [{"type": "text", "content": "Déconnecter de force un utilisateur bloqué (Session fantôme)."}, {"type": "code", "content": "logoff <SessionID> /server:<ServerName>"}]},
    {"app": "microsoft-rds", "issue": "fslogix-profile-locked", "blocks": [{"type": "text", "content": "Le disque de profil FSLogix (.vhdx) est verrouillé. Trouver qui le tient."}, {"type": "code", "content": "openfiles /query /s <FileServer> | findstr <UserName>"}]},

    # ==========================================
    # ⚙️ SCCM (MECM - Configuration Manager)
    # ==========================================
    {"app": "sccm", "issue": "client-install-fail", "blocks": [{"type": "text", "content": "Vérifier les logs d'installation du client SCCM."}, {"type": "code", "content": "cmtrace %windir%\\ccmsetup\\logs\\ccmsetup.log"}]},
    {"app": "sccm", "issue": "pxe-boot-fail", "blocks": [{"type": "text", "content": "Le boot PXE ne répond pas. Redémarrer le service WDS."}, {"type": "code", "content": "Restart-Service WDSServer"}]},
    {"app": "sccm", "issue": "software-center-sync", "blocks": [{"type": "text", "content": "Forcer la synchronisation des politiques machine sur le client."}, {"type": "code", "content": "Trigger-Schedule -ScheduleId '{00000000-0000-0000-0000-000000000021}'"}]},

    # ==========================================
    # 📊 SUPERVISION (Zabbix, PRTG, Suricata)
    # ==========================================
    {"app": "zabbix", "issue": "zabbix-queue-delay", "blocks": [{"type": "text", "content": "La file d'attente (Queue) explose. Vérifiez si les pollers sont surchargés."}, {"type": "code", "content": "grep 'StartPollers' /etc/zabbix/zabbix_server.conf"}]},
    {"app": "zabbix", "issue": "agent-get-test", "blocks": [{"type": "text", "content": "Tester manuellement une clé d'item depuis le serveur vers un agent."}, {"type": "code", "content": "zabbix_get -s <IP_Agent> -k system.cpu.load[all,avg1]"}]},
    {"app": "prtg", "issue": "probe-disconnected", "blocks": [{"type": "text", "content": "La sonde distante (Remote Probe) est déconnectée. Redémarrer le service windows."}, {"type": "code", "content": "Restart-Service 'PRTGProbeService'"}]},
    {"app": "prtg", "issue": "wmi-access-denied", "blocks": [{"type": "text", "content": "Erreur WMI. Vérifier que le firewall Windows autorise le WMI."}, {"type": "code", "content": "netsh advfirewall firewall set rule group=\"Windows Management Instrumentation (WMI)\" new enable=yes"}]},
    {"app": "suricata", "issue": "rule-update-fail", "blocks": [{"type": "text", "content": "Mettre à jour les règles de détection d'intrusion (Emerging Threats)."}, {"type": "code", "content": "suricata-update"}]},
    {"app": "suricata", "issue": "test-ids-rule", "blocks": [{"type": "text", "content": "Tester si l'IDS détecte bien une attaque (Test ping signature)."}, {"type": "code", "content": "curl http://testmynids.org/uid/index.html"}]},

    # ==========================================
    # 💰 NOTES DE FRAIS (Notilus, N2F)
    # ==========================================
    {"app": "notilus", "issue": "connector-file-stuck", "blocks": [{"type": "text", "content": "Le fichier d'interface comptable ne s'est pas généré. Vérifier le service de l'automate."}, {"type": "code", "content": "Get-Service *Notilus* | Restart-Service"}]},
    {"app": "notilus", "issue": "sso-login-fail", "blocks": [{"type": "text", "content": "Échec authentification SAML. Le certificat ADFS a expiré côté Notilus. (Action Admin)"}, {"type": "code", "content": "Check: ADFS_Signing_Certificate_Expiry"}]},
    {"app": "n2f", "issue": "api-token-invalid", "blocks": [{"type": "text", "content": "L'intégration API échoue (Erreur 401). Régénérer le token API dans le portail Admin."}, {"type": "code", "content": "Action: Admin Panel > Settings > API > Renew Token"}]},
    {"app": "n2f", "issue": "accounting-export-missing-axis", "blocks": [{"type": "text", "content": "Export impossible : L'utilisateur n'a pas de code analytique associé."}, {"type": "code", "content": "Check: User Profile > Analytical Axis 1"}]},
    {"app": "n2f", "issue": "ocr-scan-fail", "blocks": [{"type": "text", "content": "Le scan intelligent échoue. Image trop floue ou format HEIC non supporté sur ancienne version."}, {"type": "code", "content": "Action: Retry with JPG/PDF"}]}
]

def inject():
    print(f"🚀 LANCEMENT INJECTION MICROSOFT & APPS : {len(data)} solutions.")
    for entry in data:
        doc_ref = db.collection("applications").document(entry["app"])
        new_sol = {
            "author": "Terry SysAdmin",
            "blocks": entry["blocks"],
            "upvotes": 0,
            "created_at": current_date
        }
        doc_ref.set({
            "application": entry["app"],
            "solutions": firestore.ArrayUnion([new_sol])
        }, merge=True)
        print(f"✅ [AJOUTÉ] {entry['app'].upper()} : {entry['issue']}")
    print("\n🏁 OPÉRATION TERMINÉE. Ton Exit0 est maintenant certifié 'Enterprise Ready'.")

if __name__ == "__main__":
    inject()
