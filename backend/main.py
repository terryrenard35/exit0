from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import firestore
from typing import List

# Initialisation de l'API
app = FastAPI(title="Exit0 API - Production")

# Configuration CORS pour permettre au Frontend de communiquer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connexion Firestore
db = firestore.Client(project="friendly-cubist-480305-s6")

# Modèles de données
class ContentBlock(BaseModel):
    type: str  # "text" ou "code"
    content: str

class SolutionEntry(BaseModel):
    app_name: str
    issue_id: str
    blocks: List[ContentBlock]
    author: str = "Terry"

@app.get("/")
def read_root():
    return {"status": "online", "version": "1.3", "system": "Exit0 Core"}

# Route pour l'autocomplétion
@app.get("/apps")
def list_apps():
    try:
        docs = db.collection("applications").stream()
        apps = [doc.id for doc in docs]
        return {"apps": apps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route de recherche
@app.get("/search/{app_name}/{issue_id}")
def get_solution(app_name: str, issue_id: str):
    try:
        doc_ref = db.collection("applications").document(app_name.lower())
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="Log non trouvé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route d'ajout de solution avec Timestamp
@app.post("/add-solution")
async def add_solution(entry: SolutionEntry):
    try:
        doc_ref = db.collection("applications").document(entry.app_name.lower())
        
        new_sol_data = {
            "author": entry.author,
            "blocks": [b.dict() for b in entry.blocks],
            "upvotes": 0,
            "created_at": firestore.SERVER_TIMESTAMP  # Date automatique
        }
        
        doc_ref.set({
            "application": entry.app_name.lower(),
            "solutions": firestore.ArrayUnion([new_sol_data])
        }, merge=True)
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
