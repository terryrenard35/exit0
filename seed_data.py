from google.cloud import firestore

# Initialisation du client (il utilisera tes credentials gcloud)
db = firestore.Client(project="friendly-cubist-480305-s6")

def seed_exit0():
    print("🚀 Injection de la première solution dans Exit0...")
    
    # 1. Création de l'application
    app_ref = db.collection('applications').document('terraform')
    app_ref.set({
        'name': 'Terraform',
        'category': 'IaC',
        'description': 'Infrastructure as Code tool by HashiCorp'
    })

    # 2. Ajout d'une issue célèbre (celle qu'on vient de vivre !)
    issue_ref = app_ref.collection('issues').document('error-409-already-exists')
    issue_ref.set({
        'title': 'Error 409: Requested entity already exists',
        'version': '1.x',
        'tags': ['terraform', 'gcp', 'conflict']
    })

    # 3. Ajout de la solution miracle
    solution_ref = issue_ref.collection('solutions').document('import-command')
    solution_ref.set({
        'content': 'Use the terraform import command to sync your state with existing GCP resources.',
        'author': 'Terry',
        'is_verified': True,
        'upvotes': 100
    })

    print("✅ Succès ! La connaissance est maintenant dans Exit0.")

if __name__ == "__main__":
    seed_exit0()
