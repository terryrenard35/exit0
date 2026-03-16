import firebase_admin
from firebase_admin import credentials, firestore

# Initialisation (Assure-toi que le chemin vers ta clé est correct)
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def update_versions():
    apps_ref = db.collection("applications")
    docs = apps_ref.stream()

    print("--- 🛠️ MISE À JOUR DES VERSIONS EXISTANTES ---")
    for doc in docs:
        data = doc.to_dict()
        solutions = data.get("solutions", [])
        updated = False
        
        for sol in solutions:
            if "version" not in sol or sol["version"] == "":
                sol["version"] = "Stable / Legacy"
                updated = True
        
        if updated:
            apps_ref.document(doc.id).update({"solutions": solutions})
            print(f"✅ Version par défaut ajoutée pour : {doc.id}")

    print("\n--- 🚀 INJECTION DE TESTS MULTI-VERSIONS ---")
    
    # Nouvelles solutions pour tester le filtre
    test_solutions = [
        {
            "author": "Terry Ops",
            "version": "Docker 24.0 (Latest)",
            "blocks": [
                {"type": "text", "content": "Activer les statistiques en temps réel (format JSON)"},
                {"type": "code", "content": "docker stats --format \"{{json .}}\""}
            ]
        },
        {
            "author": "Terry Ops",
            "version": "Docker 19.03",
            "blocks": [
                {"type": "text", "content": "Commande historique pour lister les volumes"},
                {"type": "code", "content": "docker volume ls"}
            ]
        }
    ]

    # Ajout à la catégorie Docker
    db.collection("applications").document("docker").update({
        "solutions": firestore.ArrayUnion(test_solutions)
    })
    print("✅ Solutions Docker multi-versions injectées.")

if __name__ == "__main__":
    update_versions()
