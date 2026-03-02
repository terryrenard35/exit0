import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

k8s_docker_pack = [
    # --- DOCKER ---
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Nettoyer agressivement le cache, les volumes et images inutilisés"}, {"type": "code", "content": "docker system prune -a --volumes -f"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Récupérer l'adresse IP d'un conteneur spécifique"}, {"type": "code", "content": "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id>"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Suivre les logs de plusieurs conteneurs avec un pattern"}, {"type": "code", "content": "docker ps -q --filter \"name=webapp\" | xargs -L 1 docker logs -f"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Exporter un conteneur vers une image tar pour transfert"}, {"type": "code", "content": "docker export <container_id> > image_backup.tar"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Vérifier la consommation de ressources en temps réel"}, {"type": "code", "content": "docker stats --no-stream"}]},
    
    # --- KUBERNETES ---
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Redémarrer proprement tous les pods d'un déploiement"}, {"type": "code", "content": "kubectl rollout restart deployment <deployment_name>"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Débugger un pod avec une image temporaire (Busybox)"}, {"type": "code", "content": "kubectl run -i --tty --rm debug --image=busybox -- restart=Never -- sh"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Récupérer les logs du conteneur précédent (post-crash)"}, {"type": "code", "content": "kubectl logs <pod_name> --previous"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Lister les évènements triés par date (pour diagnostic rapide)"}, {"type": "code", "content": "kubectl get events --sort-by='.lastTimestamp'"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Forcer la suppression d'un pod bloqué en 'Terminating'"}, {"type": "code", "content": "kubectl delete pod <pod_name> --grace-period=0 --force"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Copier un fichier depuis un pod vers la machine locale"}, {"type": "code", "content": "kubectl cp <namespace>/<pod_name>:/path/to/file ./local_file"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Vérifier l'utilisation CPU/RAM des noeuds du cluster"}, {"type": "code", "content": "kubectl top nodes"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Afficher les secrets décodés (Base64) en une ligne"}, {"type": "code", "content": "kubectl get secret <name> -o jsonpath='{.data}' | base64 --decode"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Mettre un noeud en maintenance (Cordon)"}, {"type": "code", "content": "kubectl cordon <node_name> && kubectl drain <node_name> --ignore-daemonsets"}]},
    {"author": "Terry Ops", "blocks": [{"type": "text", "content": "Vérifier les droits d'une action spécifique (Can I?)"}, {"type": "code", "content": "kubectl auth can-i create deployments"}]}
]

# Injection dans les deux catégories concernées
def update_apps():
    # Pour Docker
    db.collection("applications").document("docker").update({
        "solutions": firestore.ArrayUnion(k8s_docker_pack[:5])
    })
    # Pour Kubernetes
    db.collection("applications").document("kubernetes").update({
        "solutions": firestore.ArrayUnion(k8s_docker_pack[5:])
    })
    print("🚀 20 solutions Docker/K8s injectées !")

update_apps()
