# Git Server Setup – Gitea

## 1. Ziel

Im Rahmen des Projekts wurde ein lokaler Git-Server mit **Gitea** eingerichtet.
Der Server dient als zentrale Plattform für:

* Versionsverwaltung des Projekts
* Speicherung der Infrastructure-as-Code (IaC – Infrastructure as Code, Infrastruktur als Code)
* GitOps-basierte Deployments
* Verwaltung von Security Policies und Angriffssimulationen

Der Git-Server stellt damit die **Source of Truth (zentrale Konfigurationsquelle)** für das gesamte DevSecOps Cyber-Defense Homelab dar.

---

# 2. Systemumgebung

| Komponente        | Beschreibung                                    |
| ----------------- | ----------------------------------------------- |
| Hardware          | Intel NUC                                       |
| Betriebssystem    | Linux                                           |
| Container Runtime | Docker Engine                                   |
| Git Server        | Gitea                                           |
| Domains           | `bubatzpinguin.duckdns.org`, `bubatzpinguin.ch` |
| HTTPS             | TLS-Zertifikate von Let's Encrypt               |

---

# 3. Architektur

Der Git-Server läuft containerisiert in Docker auf dem Intel NUC.

```text
Internet
   │
Yallobox
   │
Fritzbox
   │
Port 443
   │
Intel NUC
   │
Docker Container
   │
Gitea Server
   │
Repository Storage
```

Der Zugriff erfolgt über HTTPS:

```
https://bubatzpinguin.duckdns.org
```

oder

```
https://bubatzpinguin.ch
```

---

# 4. Installation

## 4.1 Installation von Docker

Zuerst wurde Docker installiert, um Gitea containerisiert betreiben zu können.

```bash
sudo apt update
sudo apt install docker.io docker-compose-plugin
```

Docker ermöglicht eine einfache und reproduzierbare Bereitstellung des Git-Servers.

---

# 4.2 Projektverzeichnis erstellen

```bash
mkdir ~/gitea
cd ~/gitea
```

Verzeichnisstruktur:

```
gitea/
 ├── docker-compose.yml
 ├── data/
 └── config/
```

---

# 4.3 Docker Compose Konfiguration

Datei: `docker-compose.yml`

```yaml
services:
  gitea:
    image: docker.gitea.com/gitea:latest
    container_name: gitea
    restart: always
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__server__ROOT_URL=https://192.168.188.50/
      - GITEA__server__DOMAIN=192.168.188.50
      - GITEA__server__SSH_DOMAIN=192.168.188.50
      - GITEA__server__START_SSH_SERVER=false
      - GITEA__database__DB_TYPE=sqlite3
    ports:
      - "443:3000"
      - "3080:3080"
      - "2222:22"
    volumes:
      - ./data:/data
      - /etc/letsencrypt:/etc/letsencrypt
    networks:
      - gitea

networks:
  gitea:
    driver: bridge
```

Ports:

| Port | Funktion           |
| ---- | ------------------ |
| 443  | HTTPS Webinterface |
| 2222 | Git SSH Zugriff    |

---

# 5. TLS / HTTPS Einrichtung

Für sichere Verbindungen wurde ein TLS-Zertifikat über **Let's Encrypt** erstellt.

Als ACME-Client wurde **Certbot** verwendet.

---

# 6. Erstellung der Zertifikate

Die Zertifikate wurden mit Certbot erstellt.

```bash
sudo certbot certonly --standalone \
-d bubatzpinguin.duckdns.org \
-d bubatzpinguin.ch
```

Dabei wurde ein **SAN-Zertifikat (Subject Alternative Name – Multi-Domain-Zertifikat)** erzeugt.

Das Zertifikat ist gültig für:

* `bubatzpinguin.duckdns.org`
* `bubatzpinguin.ch`

---

# 7. Speicherort der Zertifikate

Let's Encrypt speichert die Zertifikate unter:

```
/etc/letsencrypt/live/bubatzpinguin.duckdns.org/
```

Wichtige Dateien:

| Datei           | Beschreibung                            |
| --------------- | --------------------------------------- |
| `fullchain.pem` | Serverzertifikat inkl. Zertifikatskette |
| `privkey.pem`   | Privater Schlüssel                      |

Diese Dateien werden vom Gitea-Server verwendet.

---

# 8. Docker Zugriff auf Zertifikate

Damit der Container auf die Zertifikate zugreifen kann, wurde das Let's Encrypt Verzeichnis in Docker gemountet.

```yaml
volumes:
  - ./data:/data
  - /etc/letsencrypt:/etc/letsencrypt
```

Dadurch kann Gitea die Zertifikate direkt verwenden.

---

# 9. Gitea HTTPS Konfiguration

Die Serverkonfiguration befindet sich in:

```
/data/gitea/conf/app.ini
```

Wichtige Parameter:

```ini
[server]
DOMAIN = bubatzpinguin.duckdns.org
PROTOCOL = https
HTTP_PORT = 3000
ROOT_URL = https://bubatzpinguin.duckdns.org/

CERT_FILE = /etc/letsencrypt/live/bubatzpinguin.duckdns.org/fullchain.pem
KEY_FILE = /etc/letsencrypt/live/bubatzpinguin.duckdns.org/privkey.pem

SSH_PORT = 2222
```

Damit verwendet Gitea direkt das Let's Encrypt Zertifikat.

---

# 10. Starten des Git Servers

Der Container wird mit Docker Compose gestartet.

```bash
cd ~/gitea
sudo docker compose up -d
```

Containerstatus prüfen:

```bash
sudo docker ps
```

Logs anzeigen:

```bash
sudo docker logs gitea
```

---

# 11. Zugriff auf den Git Server

Webinterface:

```
https://bubatzpinguin.duckdns.org
```

oder

```
https://bubatzpinguin.ch
```

Repository klonen:

```bash
git clone https://bubatzpinguin.ch/user/repository
```

SSH Zugriff:

```bash
git clone ssh://git@bubatzpinguin.ch:2222/user/repository.git
```

---

# 12. Sicherheitsmassnahmen

Folgende Sicherheitsmassnahmen wurden umgesetzt:

* HTTPS mit TLS-Zertifikat
* Containerisierte Ausführung mit Docker
* Zugriff nur über benötigte Ports
* deaktivierte Benutzerregistrierung
* Git Zugriff über SSH-Port

---

# 13. Automatische Zertifikatserneuerung

Let's Encrypt Zertifikate sind **90 Tage gültig**.

Die automatische Erneuerung erfolgt über Certbot:

```bash
sudo certbot renew
```

Test der automatischen Erneuerung:

```bash
sudo certbot renew --dry-run
```

---

# 14. Rolle im Gesamtprojekt

Der Git-Server bildet die zentrale Plattform für:

* Infrastructure-as-Code
* DevSecOps Pipelines
* Firewall Policy-as-Code
* Angriffssimulationen
* SOC Konfiguration

Alle Komponenten des Cyber-Defense Labs werden über diesen Git-Server versioniert und reproduzierbar deployt.

---

# 15. Ergebnis

Der Git-Server läuft stabil auf dem Intel NUC und ist über HTTPS erreichbar.
Er dient als zentrale Entwicklungs- und Deploymentplattform für das gesamte DevSecOps Cyber-Defense Homelab.


