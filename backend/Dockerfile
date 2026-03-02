# Utilise une image Python légère
FROM python:3.10-slim

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installe les librairies (sans cache pour gagner de la place)
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code du backend
COPY . .

# Expose le port par défaut de Cloud Run
ENV PORT 8080

# Commande pour lancer l'API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
