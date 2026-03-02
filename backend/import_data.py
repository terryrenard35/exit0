import firebase_admin
from google.cloud import firestore
from datetime import datetime, timezone

# Initialisation Firestore
db = firestore.Client(project="friendly-cubist-480305-s6")

# On utilise une date Python fixe pour le remplissage initial
# Cela évite le bug de la sentinelle dans ArrayUnion
current_date = datetime.now(timezone.utc)

data = [
    # --- DOCKER (10 solutions) ---
    {"app": "docker", "issue": "permission-denied", "blocks": [{"type": "text", "content": "Ajouter l'utilisateur actuel au groupe docker pour éviter le sudo."}, {"type": "code", "content": "sudo usermod -aG docker $USER && newgrp docker"}]},
    {"app": "docker", "issue": "no-space-left", "blocks": [{"type": "text", "content": "Nettoyer les données inutilisées (images, containers, réseaux)."}, {"type": "code", "content": "docker system prune -a --volumes"}]},
    {"app": "docker", "issue": "container-exit-137", "blocks": [{"type": "text", "content": "Le container a été tué par le OOM Killer (Manque de RAM). Augmentez la limite mémoire."}, {"type": "code", "content": "docker run -m 2g my-image"}]},
    {"app": "docker", "issue": "port-already-allocated", "blocks": [{"type": "text", "content": "Identifier et tuer le processus qui occupe le port."}, {"type": "code", "content": "sudo lsof -i :<PORT> && kill -9 <PID>"}]},
    {"app": "docker", "issue": "cannot-connect-daemon", "blocks": [{"type": "text", "content": "Vérifier si le service docker est bien lancé."}, {"type": "code", "content": "sudo systemctl start docker"}]},
    {"app": "docker", "issue": "image-pull-limit", "blocks": [{"type": "text", "content": "Docker Hub limite le pull anonyme. Connectez-vous."}, {"type": "code", "content": "docker login"}]},
    {"app": "docker", "issue": "dangling-volumes", "blocks": [{"type": "text", "content": "Supprimer les volumes orphelins qui consomment du disque."}, {"type": "code", "content": "docker volume prune"}]},
    {"app": "docker", "issue": "inspect-ip-address", "blocks": [{"type": "text", "content": "Récupérer rapidement l'IP d'un container en marche."}, {"type": "code", "content": "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <ID>"}]},
    {"app": "docker", "issue": "logs-follow", "blocks": [{"type": "text", "content": "Suivre les logs en temps réel d'un container."}, {"type": "code", "content": "docker logs -f <CONTAINER_NAME>"}]},
    {"app": "docker", "issue": "copy-file-from-container", "blocks": [{"type": "text", "content": "Extraire un fichier d'un container vers votre machine."}, {"type": "code", "content": "docker cp <CONTAINER_ID>:/path/to/file ./local-path"}]},

    # --- KUBERNETES (10 solutions) ---
    {"app": "kubernetes", "issue": "crashloopbackoff", "blocks": [{"type": "text", "content": "Vérifier les logs du container précédent pour comprendre le crash."}, {"type": "code", "content": "kubectl logs <POD_NAME> --previous"}]},
    {"app": "kubernetes", "issue": "pod-terminating-stuck", "blocks": [{"type": "text", "content": "Forcer la suppression d'un pod bloqué."}, {"type": "code", "content": "kubectl delete pod <POD> --grace-period=0 --force"}]},
    {"app": "kubernetes", "issue": "image-pull-backoff", "blocks": [{"type": "text", "content": "Vérifier le secret de tirage d'image."}, {"type": "code", "content": "kubectl describe pod <POD> | grep Events"}]},
    {"app": "kubernetes", "issue": "describe-node-resources", "blocks": [{"type": "text", "content": "Voir l'utilisation CPU/RAM d'un node spécifique."}, {"type": "code", "content": "kubectl describe node <NODE_NAME> | grep -A 7 Allocated"}]},
    {"app": "kubernetes", "issue": "context-switch", "blocks": [{"type": "text", "content": "Changer rapidement de cluster/contexte."}, {"type": "code", "content": "kubectl config use-context <CONTEXT_NAME>"}]},
    {"app": "kubernetes", "issue": "get-all-namespaces", "blocks": [{"type": "text", "content": "Lister toutes les ressources de tous les namespaces."}, {"type": "code", "content": "kubectl get all --all-namespaces"}]},
    {"app": "kubernetes", "issue": "exec-shell", "blocks": [{"type": "text", "content": "Ouvrir un shell interactif dans un Pod."}, {"type": "code", "content": "kubectl exec -it <POD_NAME> -- /bin/bash"}]},
    {"app": "kubernetes", "issue": "port-forward", "blocks": [{"type": "text", "content": "Accéder à un service interne depuis localhost."}, {"type": "code", "content": "kubectl port-forward svc/<SERVICE_NAME> 8080:<TARGET_PORT>"}]},
    {"app": "kubernetes", "issue": "decode-secret", "blocks": [{"type": "text", "content": "Lire la valeur d'un secret encodé en base64."}, {"type": "code", "content": "kubectl get secret <NAME> -o jsonpath='{.data.password}' | base64 --decode"}]},
    {"app": "kubernetes", "issue": "rollout-status", "blocks": [{"type": "text", "content": "Suivre l'état d'un déploiement en cours."}, {"type": "code", "content": "kubectl rollout status deployment/<NAME>"}]},

    # --- TERRAFORM (10 solutions) ---
    {"app": "terraform", "issue": "state-lock", "blocks": [{"type": "text", "content": "Forcer le déverrouillage du state après un crash."}, {"type": "code", "content": "terraform force-unlock <LOCK_ID>"}]},
    {"app": "terraform", "issue": "init-upgrade", "blocks": [{"type": "text", "content": "Mettre à jour les providers et modules."}, {"type": "code", "content": "terraform init -upgrade"}]},
    {"app": "terraform", "issue": "taint-resource", "blocks": [{"type": "text", "content": "Forcer la recréation d'une ressource au prochain apply."}, {"type": "code", "content": "terraform apply -replace='<RESOURCE_ADDR>'"}]},
    {"app": "terraform", "issue": "output-json", "blocks": [{"type": "text", "content": "Extraire les outputs pour un script tiers."}, {"type": "code", "content": "terraform output -json"}]},
    {"app": "terraform", "issue": "validate-config", "blocks": [{"type": "text", "content": "Vérifier la syntaxe sans rien déployer."}, {"type": "code", "content": "terraform validate"}]},
    {"app": "terraform", "issue": "plan-out", "blocks": [{"type": "text", "content": "Sauvegarder un plan pour garantir son exécution identique."}, {"type": "code", "content": "terraform plan -out=tfplan && terraform apply tfplan"}]},
    {"app": "terraform", "issue": "state-list", "blocks": [{"type": "text", "content": "Voir toutes les ressources actuellement gérées."}, {"type": "code", "content": "terraform state list"}]},
    {"app": "terraform", "issue": "refresh-only", "blocks": [{"type": "text", "content": "Mettre à jour le state sans modifier l'infra réelle."}, {"type": "code", "content": "terraform apply -refresh-only"}]},
    {"app": "terraform", "issue": "import-resource", "blocks": [{"type": "text", "content": "Importer une ressource existante dans le state."}, {"type": "code", "content": "terraform import <ADDR> <ID_REELLE>"}]},
    {"app": "terraform", "issue": "fmt-recursive", "blocks": [{"type": "text", "content": "Formater récursivement tous les fichiers .tf du projet."}, {"type": "code", "content": "terraform fmt -recursive"}]},

    # --- GIT (10 solutions) ---
    {"app": "git", "issue": "undo-commit-keep-changes", "blocks": [{"type": "text", "content": "Annuler le dernier commit mais garder les fichiers modifiés."}, {"type": "code", "content": "git reset --soft HEAD~1"}]},
    {"app": "git", "issue": "change-commit-message", "blocks": [{"type": "text", "content": "Modifier le message du dernier commit non poussé."}, {"type": "code", "content": "git commit --amend -m 'nouveau message'"}]},
    {"app": "git", "issue": "discard-local-changes", "blocks": [{"type": "text", "content": "Forcer le retour à l'état du serveur (Attention : perte de données local)."}, {"type": "code", "content": "git reset --hard origin/<BRANCH>"}]},
    {"app": "git", "issue": "stash-save", "blocks": [{"type": "text", "content": "Mettre de côté vos changements pour changer de branche."}, {"type": "code", "content": "git stash && git stash pop"}]},
    {"app": "git", "issue": "delete-local-branch", "blocks": [{"type": "text", "content": "Supprimer proprement une branche fusionnée."}, {"type": "code", "content": "git branch -d <NAME>"}]},
    {"app": "git", "issue": "log-graph", "blocks": [{"type": "text", "content": "Visualiser l'historique de manière lisible."}, {"type": "code", "content": "git log --oneline --graph --all"}]},
    {"app": "git", "issue": "cherry-pick", "blocks": [{"type": "text", "content": "Appliquer un commit spécifique sur votre branche actuelle."}, {"type": "code", "content": "git cherry-pick <HASH>"}]},
    {"app": "git", "issue": "check-config", "blocks": [{"type": "text", "content": "Vérifier votre identité configurée."}, {"type": "code", "content": "git config --list"}]},
    {"app": "git", "issue": "undo-merge", "blocks": [{"type": "text", "content": "Annuler une fusion qui vient de se produire."}, {"type": "code", "content": "git reset --hard HEAD~1"}]},
    {"app": "git", "issue": "find-branch-by-commit", "blocks": [{"type": "text", "content": "Savoir dans quelle branche se trouve un commit."}, {"type": "code", "content": "git branch -a --contains <HASH>"}]},

    # --- AWS CLI (10 solutions) ---
    {"app": "aws", "issue": "s3-sync", "blocks": [{"type": "text", "content": "Synchroniser un dossier local avec un bucket S3."}, {"type": "code", "content": "aws s3 sync ./local s3://my-bucket"}]},
    {"app": "aws", "issue": "whoami", "blocks": [{"type": "text", "content": "Vérifier l'identité et le compte connecté."}, {"type": "code", "content": "aws sts get-caller-identity"}]},
    {"app": "aws", "issue": "list-instances-running", "blocks": [{"type": "text", "content": "Lister uniquement les instances EC2 allumées."}, {"type": "code", "content": "aws ec2 describe-instances --filters 'Name=instance-state-name,Values=running'"}]},
    {"app": "aws", "issue": "ecr-login", "blocks": [{"type": "text", "content": "Authentifier Docker pour pousser sur ECR."}, {"type": "code", "content": "aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com"}]},
    {"app": "aws", "issue": "lambda-logs", "blocks": [{"type": "text", "content": "Récupérer les derniers logs d'une fonction Lambda."}, {"type": "code", "content": "aws logs tail /aws/lambda/<FUNCTION_NAME>"}]},
    {"app": "aws", "issue": "copy-s3-to-s3", "blocks": [{"type": "text", "content": "Copier un fichier entre deux buckets sans passer par le local."}, {"type": "code", "content": "aws s3 cp s3://source-bucket/file s3://dest-bucket/"}]},
    {"app": "aws", "issue": "get-instance-ip", "blocks": [{"type": "text", "content": "Récupérer l'IP publique d'une instance EC2."}, {"type": "code", "content": "aws ec2 describe-instances --instance-ids <ID> --query 'Reservations[*].Instances[*].PublicIpAddress' --output text"}]},
    {"app": "aws", "issue": "delete-s3-bucket-force", "blocks": [{"type": "text", "content": "Supprimer un bucket même s'il n'est pas vide."}, {"type": "code", "content": "aws s3 rb s3://<BUCKET_NAME> --force"}]},
    {"app": "aws", "issue": "list-profiles", "blocks": [{"type": "text", "content": "Voir tous les profils AWS configurés."}, {"type": "code", "content": "aws configure list-profiles"}]},
    {"app": "aws", "issue": "secrets-manager-get", "blocks": [{"type": "text", "content": "Récupérer la valeur d'un secret."}, {"type": "code", "content": "aws secretsmanager get-secret-value --secret-id <NAME>"}]}
]

def inject():
    print("⏳ Début de l'injection massive...")
    for entry in data:
        doc_ref = db.collection("applications").document(entry["app"])
        new_sol = {
            "author": "Terry Ops Engine",
            "blocks": entry["blocks"],
            "upvotes": 0,
            "created_at": current_date # Utilisation d'une date Python standard
        }
        
        # On injecte
        doc_ref.set({
            "application": entry["app"],
            "solutions": firestore.ArrayUnion([new_sol])
        }, merge=True)
        print(f"✅ Log ajouté : {entry['app']} -> {entry['issue']}")
    
    print("\n✨ Félicitations ! Ta base de données est maintenant remplie de 50 solutions d'experts.")

if __name__ == "__main__":
    inject()
