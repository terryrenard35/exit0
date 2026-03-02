#!/bin/bash

echo "🚀 Démarrage du déploiement FRONTEND..."

# 1. Aller dans le dossier frontend
cd frontend || exit

# 2. Build de l'application (Vite)
echo "🏗️  Compilation du projet React..."
npm run build

# 3. Déploiement Firebase
echo "🔥 Envoi vers Firebase Hosting..."
firebase deploy --only hosting

echo "✅ FRONTEND mis à jour avec succès !"
