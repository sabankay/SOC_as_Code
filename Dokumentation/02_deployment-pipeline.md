# Einrichtung der GitOps Deployment Pipeline

## 1. Ziel

Ziel dieses Schrittes war es, eine **automatisierte Deployment-Pipeline** für das Cyber-Defense Homelab einzurichten.

Dabei soll gelten:

```text
Git Push → Pipeline → automatisches Deployment
```

Das bedeutet:

* Infrastruktur wird als Code verwaltet (**IaC – Infrastructure as Code**)
* Änderungen werden über Git versioniert
* Deployments erfolgen automatisch über eine CI/CD Pipeline

---

# 2. Verwendete Komponenten

Für das Deployment werden folgende Komponenten verwendet:

| Komponente         | Funktion                               |
| ------------------ | -------------------------------------- |
| **Gitea**          | Git Server                             |
| **Gitea Actions**  | CI/CD Pipeline                         |
| **act_runner**     | Runner zur Ausführung der Pipelines    |
| **SSH**            | Verbindung zum Zielhost                |
| **rsync**          | Synchronisation der Repository Dateien |
| **Docker Compose** | Deployment der Services                |

---

# 3. Git Server Setup

Als Git Plattform wird **Gitea** auf dem Intel NUC betrieben.

Der Server stellt bereit:

```text
Git Repository
CI/CD Pipelines
Runner Integration
```

Zugriff erfolgt über:

```text
https://bubatzpinguin.ch
```

---

# 4. Einrichtung des Gitea Runners

Damit Pipelines ausgeführt werden können, wurde ein **act_runner** eingerichtet.

Der Runner führt automatisch die Workflows aus, wenn ein Git Event ausgelöst wird.

## Runner starten

Der Runner wurde als Docker Container gestartet.

```bash
sudo docker run -d \
--name gitea-runner \
-e GITEA_INSTANCE_URL=https://bubatzpinguin.ch \
-e GITEA_RUNNER_REGISTRATION_TOKEN=<token> \
-v /var/run/docker.sock:/var/run/docker.sock \
-v ./runner-data:/data \
gitea/act_runner:latest
```

Parameter:

| Parameter                         | Bedeutung                 |
| --------------------------------- | ------------------------- |
| `GITEA_INSTANCE_URL`              | URL des Git Servers       |
| `GITEA_RUNNER_REGISTRATION_TOKEN` | Token zur Registrierung   |
| `/var/run/docker.sock`            | Zugriff auf Docker Engine |

Nach dem Start registriert sich der Runner automatisch im Gitea Server.

---

# 5. Repository Struktur

Das Repository wurde so aufgebaut, dass alle Infrastrukturkomponenten versioniert sind.

```text
defense-lab-soc/
├── .gitea/
│   └── workflows/
│       ├── deploy-nuc.yml
│       ├── deploy-pi.yml
│       └── deploy-fortigate.yml
├── hosts/
│   ├── nuc/
│   │   ├── compose.yml
│   │   ├── grafana/
│   │   │   └── provisioning/
│   │   │       ├── datasources/
│   │   │       │   └── loki.yml
│   │   │       └── dashboards/
│   │   │           └── dashboards.yml
│   │   ├── loki/
│   │   │   └── config.yml
│   │   ├── promtail/
│   │   │   └── config.yml
│   │   └── syslog-ng/
│   │       ├── syslog-ng.conf
│   │       └── logs/
│   ├── raspberrypi/
│   │   ├── compose.yml
│   │   ├── pihole/
│   │   └── agent/
│   └── fortigate/
│       └── README.md
├── policies/
│   └── fortigate/
│       ├── address-objects/
│       ├── service-objects/
│       └── firewall-policies/
├── scripts/
│   ├── deploy-nuc.sh
│   ├── deploy-pi.sh
│   ├── apply-fortigate-policies.sh
│   ├── healthcheck.sh
|   ├── hids.py
│   └── logs.sh
├── attacks/
│   ├── README.md
│   └── scenarios/
├── docs/
├── evidence/
├── README.md
└── .gitignore
```

---

# 6. Deployment Workflow

Der Deployment Workflow wird durch einen **Git Push** ausgelöst.

Workflow Datei:

```text
.gitea/workflows/deploy-nuc.yml
```

Beispiel:

```yaml
name: Deploy Intel NUC

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-24.04

    steps:
      - name: Repository auschecken
        uses: actions/checkout@v4

      - name: SSH Key einrichten
        run: |
          mkdir -p ~/.ssh
          printf "%s\n" "${{ secrets.NUC_SSH_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan -H 192.168.188.50 >> ~/.ssh/known_hosts

      - name: Deployment starten
        run: bash scripts/deploy-nuc.sh
```

---

# 7. SSH-basierter Deployment Zugriff

Die Pipeline verbindet sich über **SSH (Secure Shell – verschlüsselte Fernzugriffsschnittstelle)** mit dem Intel NUC.

Dafür wurde ein **SSH Deploy Key** erstellt.

## SSH Key generieren

```bash
ssh-keygen -t ed25519
```

Der Public Key wird auf dem Zielhost hinterlegt.

```text
/home/bob/.ssh/authorized_keys
```

Der Private Key wird als **Secret im Repository gespeichert**.

Repository:

```text
Settings → Actions → Secrets → NUC_SSH_KEY
```

---

# 8. Deployment Benutzer

Für das automatisierte Deployment wurde ein eigener Benutzer erstellt.

```bash
sudo adduser bob
```

Der Benutzer wird ausschließlich für Deployments verwendet.

## Rechte

Docker Zugriff:

```bash
sudo usermod -aG docker bob
```

Passwortloses sudo:

```text
bob ALL=(ALL) NOPASSWD: ALL
```

---

# 9. Deployment Script

Das eigentliche Deployment wird über ein Script ausgeführt.

Datei:

```text
scripts/deploy-nuc.sh
```

Inhalt:

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET_HOST="bob@192.168.188.50"
TARGET_DIR="/opt/defense-lab-soc"

echo "Deploy Intel NUC monitoring stack"

ssh "${TARGET_HOST}" "sudo mkdir -p ${TARGET_DIR}"

rsync -az --delete ./ "${TARGET_HOST}:${TARGET_DIR}/"

ssh "${TARGET_HOST}" "
cd ${TARGET_DIR}/hosts/nuc &&
sudo docker compose pull &&
sudo docker compose up -d --remove-orphans
"
```

---

# 10. Ablauf des Deployments

Der komplette Deployment Prozess läuft wie folgt:

```text
Git Push
   │
   ▼
Gitea Actions Pipeline
   │
   ▼
Runner führt Workflow aus
   │
   ▼
SSH Verbindung
   │
   ▼
Repository wird synchronisiert (rsync)
   │
   ▼
docker compose startet / aktualisiert Services
```

---

# 11. Vorteile dieses Ansatzes

Dieses Deployment Modell bietet mehrere Vorteile:

* **Reproduzierbarkeit**
* **Versionierte Infrastruktur**
* **Automatisches Deployment**
* **Keine manuelle Serverkonfiguration**

Alle Änderungen an der Infrastruktur werden ausschließlich über Git gesteuert.

---

# 12. Ergebnis

Nach der Einrichtung der Pipeline können Deployments automatisch durchgeführt werden.

Beispiel:

```bash
git push
```

führt automatisch aus:

```text
Pipeline startet
→ Code wird übertragen
→ Docker Container werden aktualisiert
→ Monitoring Stack wird gestartet
```

Damit ist eine vollständige **GitOps Deployment Umgebung** für das Homelab geschaffen.

---

