#!/bin/bash

# Configuration des variables
PROJECT_ID="friendly-cubist-480305-s6"
REGION="europe-west1"
REPO_NAME="exit0-repo"
IMAGE_NAME="exit0-api"
VPC_CONNECTOR="exit0-vpc-conn-v2"

echo "🚀 Démarrage du déploiement BACKEND..."

# 1. Aller dans le dossier backend
cd backend || exit

# 2. Build de l'image Docker
echo "📦 Build de l'image Docker..."
docker build --platform linux/amd64 -t exit0-backend .

# 3. Tag de l'image
echo "🏷️  Tagging de l'image..."
docker tag exit0-backend ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}

# 4. Push vers Artifact Registry
echo "📤 Push vers Google Cloud..."
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}

# 5. Déploiement sur Cloud Run
echo "🌍 Mise en ligne sur Cloud Run..."
gcloud run deploy ${IMAGE_NAME} \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME} \
  --region ${REGION} \
  --vpc-connector ${VPC_CONNECTOR} \
  --allow-unauthenticated \
  --project ${PROJECT_ID}

echo "✅ BACKEND mis à jour avec succès !"
