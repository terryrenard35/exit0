# 1. Configuration du Provider Google
provider "google" {
  project = "friendly-cubist-480305-s6"
  region  = "europe-west1"
}

# 2. Réseau VPC principal
resource "google_compute_network" "exit0_vpc" {
  name                    = "exit0-vpc-network"
  auto_create_subnetworks = false
  description             = "VPC principal pour la plateforme d'entraide Exit0"
}

# 3. Sous-réseau privé
resource "google_compute_subnetwork" "exit0_subnet_private" {
  name                     = "exit0-subnet-eu-west1"
  ip_cidr_range            = "10.0.1.0/24"
  region                   = "europe-west1"
  network                  = google_compute_network.exit0_vpc.id
  private_ip_google_access = true
}

# 4. Connecteur VPC pour Cloud Run (Version v2 pour éviter le conflit 409)
resource "google_vpc_access_connector" "exit0_connector_v2" {
  name          = "exit0-vpc-conn-v2"
  region        = "europe-west1"
  ip_cidr_range = "10.8.0.0/28"
  network       = google_compute_network.exit0_vpc.name
  
  # Paramètres obligatoires pour éviter l'erreur Code 3
  min_instances = 2
  max_instances = 3
  machine_type  = "e2-micro"
}

# 5. Firewall de base (Autoriser le trafic interne)
resource "google_compute_firewall" "exit0_allow_internal" {
  name    = "exit0-allow-internal"
  network = google_compute_network.exit0_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  source_ranges = ["10.0.1.0/24", "10.8.0.0/28"]
}

# 6. Activation des APIs nécessaires (Cloud Run et Firestore)
resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "run.googleapis.com",
    "firestore.googleapis.com",
    "vpcaccess.googleapis.com"
  ])
  service = each.key
  disable_on_destroy = false
}

# 7. Création de la base de données Firestore (Mode Native)
resource "google_firestore_database" "database" {
  name        = "(default)" # GCP impose "(default)" pour la base principale
  location_id = "europe-west1"
  type        = "FIRESTORE_NATIVE"

  # On s'assure que l'API est activée avant de créer la base
  depends_on = [google_project_service.enabled_apis]
}
