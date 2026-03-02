import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Nouvelles solutions à ajouter
ad_expert_solutions = [
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Récupérer un objet supprimé (Corbeille AD)"}, {"type": "code", "content": "Get-ADObject -Filter 'Name -like \"*\"' -IncludeDeletedObjects | Restore-ADObject"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Lister les GPO liées à une Unité d'Organisation (OU)"}, {"type": "code", "content": "Get-GPInheritance -Target \"OU=Marketing,DC=exit0,DC=tech\""}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Vérifier le statut de réplication SYSVOL (DFSR)"}, {"type": "code", "content": "dfsrdiag replicationstate"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Trouver les comptes admin sans expiration de mot de passe"}, {"type": "code", "content": "Get-ADUser -Filter 'PasswordNeverExpires -eq $true' | Select Name"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Forcer le retrait d'un contrôleur de domaine HS (Metadata Cleanup)"}, {"type": "code", "content": "ntdsutil \"metadata cleanup\" \"remove selected server <NAME>\""}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Vérifier les rôles FSMO du domaine"}, {"type": "code", "content": "netdom query fsmo"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Lister les accès aux partages administratifs"}, {"type": "code", "content": "net share"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Analyser les logs de verrouillage compte (Event ID 4740)"}, {"type": "code", "content": "Get-WinEvent -FilterHashtable @{LogName='Security';ID=4740}"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Vérifier la version du schéma Active Directory"}, {"type": "code", "content": "Get-ADRootDSE | select schemaNamingContext"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Tester la connectivité RPC vers un contrôleur de domaine"}, {"type": "code", "content": "nltest /dsgetdc:exit0.tech"}]}
]

# Mise à jour dans Firestore
doc_ref = db.collection("applications").document("active-directory")
doc_ref.update({
    "solutions": firestore.ArrayUnion(ad_expert_solutions)
})

print("🚀 10 nouvelles solutions AD injectées sur exit0.tech !")
