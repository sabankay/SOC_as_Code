
![Obababobubazpinguin](/images/logo.png)

# M300 - Cyber Defense Lab

## Inhalt des Repos
- [Planung](planung.md)
- [Tages Journals](/Journal)
- [Scrips](/scripts/)


---

## Inhaltsverzeichnis
[TOC]
## Übersicht

Dieses Projekt implementiert ein vollständig **IaC (Infrastructure as Code – Infrastruktur als Code)** basiertes **DevSecOps (Development Security Operations – integrierte Entwicklung, Sicherheit und Betrieb) Cyber-Defense Homelab** in einer lokalen On-Premise-Umgebung.

Ziel ist der Aufbau eines reproduzierbaren Security-Labs, in dem die gesamte Infrastruktur, Konfiguration und Bereitstellung **zentral über Git** verwaltet wird. Der **Intel NUC** dient dabei als zentrale Steuerungs- und Automatisierungsinstanz. Auf ihm laufen der **Git-Server**, die **CI/CD-Pipeline (Continuous Integration / Continuous Deployment – kontinuierliche Integration und Auslieferung)** und gegebenenfalls ein Runner.

Sobald Änderungen in das Repository gepusht werden, werden diese automatisiert auf die jeweiligen Zielsysteme ausgerollt:

* auf den **Intel NUC** für zentrale Services
* auf den **Raspberry Pi** für DNS- und optionale Log- oder Agent-Dienste
* auf die **FortiGate Firewall** für Netzwerkregeln und Sicherheitsrichtlinien über die **API (Application Programming Interface – Programmierschnittstelle)**

Das Homelab folgt damit konsequent dem Prinzip:

* **Git als zentrale Quelle der Wahrheit**
* **automatisierte Ausbringung auf mehrere Geräte**
* **vollständig reproduzierbare Infrastruktur**
* **Security Testing als Code**

---

# Zielsetzung

Das Projekt verfolgt das Ziel, ein lokales Cyber-Defense Lab aufzubauen, in dem Infrastruktur, Services, Policies und Angriffssimulationen vollständig deklarativ und reproduzierbar verwaltet werden.

Im Zentrum steht nicht nur das automatisierte Deployment einzelner Container auf einem Server, sondern die **zentrale Verwaltung des gesamten Labs als Code**.

Das bedeutet konkret:

* Services werden per Code definiert und automatisiert bereitgestellt
* Firewall-Regeln werden als Dateien versioniert und automatisiert auf die FortiGate angewendet
* Konfigurationen für mehrere Systeme werden aus einem zentralen Repository ausgerollt
* Angriffssimulationen werden reproduzierbar gestartet, um Logging und Erkennung nachweisbar zu testen

---

# Architekturprinzip

## Zentrale Steuerung über den Intel NUC

Der Intel NUC ist die zentrale Automatisierungsplattform des Labs. Er ist **nicht nur Host für lokale Container**, sondern übernimmt die Rolle der zentralen Steuerung.

Auf dem Intel NUC laufen:

* **Git-Server**
* **CI/CD-System (Continuous Integration / Continuous Deployment – kontinuierliche Integration und Auslieferung)**
* Deploymentskripte und Automatisierungslogik
* zentrale Monitoring- und Logging-Services

Von dort aus werden Konfigurationen und Deployments auf weitere Systeme ausgebracht.

---

## Zielsysteme

### Intel NUC

Der Intel NUC hostet die zentrale Plattform für:

* Git-Server
* Pipeline-Ausführung
* Monitoring
* Logging
* Dashboards
* zentrale Automatisierung

### Raspberry Pi

Der Raspberry Pi übernimmt dezentrale Infrastrukturaufgaben wie:

* **DNS (Domain Name System – Namensauflösung)**
* optional Agenten für Logging oder Monitoring
* zusätzliche Lab-Komponenten

Auch diese Konfiguration wird per Code verwaltet und durch die Pipeline automatisiert aktualisiert.

### FortiGate Firewall

Die FortiGate stellt bereit:

* Netzwerksegmentierung
* Policy Enforcement
* zentrale Firewall-Regeln
* Log-Erzeugung über **Syslog (System Logging Protocol – Protokoll zur Logübertragung)**

Die Firewall-Konfiguration wird als **Policy-as-Code** versioniert und automatisiert über die API angewendet.

---

# Kernidee: Das gesamte Lab als IaC

Dieses Projekt versteht das Homelab als vollständig code-gesteuerte Umgebung.

Das umfasst:

## Infrastruktur als Code

Systemnahe Konfigurationen, Service-Definitionen und Abläufe werden versioniert und automatisiert ausgerollt.

## Policy-as-Code

Firewall-Regeln und Netzwerkrichtlinien werden nicht manuell gepflegt, sondern als Dateien im Repository verwaltet und automatisiert angewendet.

## GitOps

Ein Push in das zentrale Repository löst automatisierte Prozesse aus, die den gewünschten Zustand auf die Zielsysteme ausbringen.

## Attack-as-Code

Definierte Angriffssimulationen sind standardisiert und reproduzierbar als Jobs, Skripte oder Container ausführbar.

---

# High-Level Ablauf

```text
Änderung im Repository
        │
        ▼
Push auf Git-Server am Intel NUC
        │
        ▼
CI/CD-Pipeline wird gestartet
        │
        ▼
Automatisierte Verteilung der Änderungen
        │
        ├── Deployment zentraler Services auf den Intel NUC
        ├── Ausrollen von Konfigurationen / Diensten auf den Raspberry Pi
        └── Anwenden von Firewall-Policies auf die FortiGate per API
        │
        ▼
Lab entspricht dem im Repository definierten Soll-Zustand
```

---

# Architekturübersicht

## Hardware und Rollen

| Komponente             | Rolle im Lab                                                               |
| ---------------------- | -------------------------------------------------------------------------- |
| **FortiGate Firewall** | Segmentierung, Firewall-Policies, Logquelle, Policy Enforcement            |
| **Cisco Switch**       | Netzwerkanbindung und Verteilung                                           |
| **Raspberry Pi**       | DNS-Dienst, optionale Log- oder Agent-Komponente                           |
| **Intel NUC**          | Git-Server, CI/CD-Steuerung, zentrales Monitoring, Logging, Orchestrierung |

---

## Daten- und Steuerflüsse

```text
Git Push
   │
   ▼
Git-Server auf Intel NUC
   │
   ▼
CI/CD-Pipeline
   │
   ├── deployt Services auf Intel NUC
   ├── verteilt Konfiguration auf Raspberry Pi
   └── wendet Policies auf FortiGate an
   │
   ▼
Logs und Events aus allen Systemen
   │
   ▼
zentrale Auswertung im Monitoring-Stack
```

---

# Projektziele

## Hauptziel

Implementierung eines reproduzierbaren lokalen DevSecOps Cyber-Defense Labs, in dem das gesamte Homelab zentral aus einem Repository verwaltet und automatisiert auf mehrere Geräte ausgerollt wird.

## Teilziele

### 1. GitOps für mehrere Zielsysteme

* Ein zentrales Repository enthält alle Definitionen für Infrastruktur, Services und Policies
* Ein Push startet automatisch die Pipeline
* Die Pipeline bringt Änderungen auf den Intel NUC, den Raspberry Pi und die FortiGate aus

### 2. Vollständiger IaC-Ansatz

* Infrastruktur und Konfigurationen werden nicht manuell gepflegt
* Zustände sind versioniert, nachvollziehbar und reproduzierbar
* Änderungen können wiederholt und kontrolliert angewendet werden

### 3. Policy-as-Code

* Firewall-Regeln werden in Dateien beschrieben
* Die FortiGate wird automatisiert per API konfiguriert
* Änderungen an Policies sind versioniert und dokumentiert

### 4. Attack-as-Code

* Angriffssimulationen werden standardisiert gestartet
* Logs und Erkennungsereignisse werden zentral gesammelt
* Die Wirksamkeit von Regeln und Monitoring wird nachweisbar getestet

### 5. Monitoring und Nachweisbarkeit

* Logs von Firewall, Host und DNS werden zentral gesammelt
* Dashboards und Reports machen Ereignisse sichtbar
* Für jeden Use Case existiert ein Evidence-Pack mit Nachweisen

---

# Repository-Struktur

```text
defense-lab-soc/
├── README.md
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   └── use-cases.md
├── services/
│   ├── compose.yml
│   ├── grafana/
│   │   └── provisioning/
│   ├── loki/
│   │   └── config.yml
│   ├── promtail/
│   │   └── config.yml
│   └── syslog-ng/
│       └── syslog-ng.conf
├── scripts/
│   ├── deploy.sh
│   ├── stop.sh
│   ├── logs.sh
│   ├── healthcheck.sh
|   └── hids.py
├── attacks/
│   ├── README.md
│   └── scenarios/
├── policies/
│   ├── README.md
│   └── fortigate/
├── hosts/
│   ├── nuc/
│   ├── raspberrypi/
│   └── fortigate/
├── evidence/
│   └── .gitkeep
└── pipeline/
    └── gitea-actions.yml
```

---

# Deployment-Modell

Das Deployment erfolgt nicht nur lokal auf einem Host, sondern als zentrale Verteilung auf mehrere Systeme.

## Beispiel

* Änderungen an `services/` werden auf dem Intel NUC angewendet
* Änderungen an `hosts/raspberrypi/` werden auf den Raspberry Pi ausgerollt
* Änderungen an `policies/fortigate/` werden automatisiert auf die FortiGate übertragen

Dadurch kann das gesamte Lab aus einem einzigen Repository heraus betrieben werden.

---

# Use Cases

## UC-1 Portscan Simulation

Ziel ist das Erzeugen von Netzwerkereignissen, die in Firewall-Logs und Dashboards sichtbar werden.

## UC-2 Brute-Force-Simulation

Ziel ist das reproduzierbare Erzeugen fehlgeschlagener Anmeldeversuche auf einem Testdienst.

## UC-3 DNS-Anomalie-Simulation

Ziel ist das Erzeugen ungewöhnlicher DNS-Aktivität, die im DNS-Logging und Monitoring sichtbar wird.

---

# Monitoring

Zentral sichtbar gemacht werden unter anderem:

* FortiGate-Logs
* Host-Logs
* DNS-Logs
* Ereignisse aus Angriffssimulationen
* Health- und Statusinformationen der Services

Mögliche Komponenten:

* **Grafana** für Dashboards
* **Loki** für Log-Aggregation
* **Promtail** für Log-Erfassung
* **Syslog-NG** als Log-Collector

---

# Definition of Done

Das Projekt ist erfolgreich abgeschlossen, wenn:

* das gesamte Lab aus dem Repository reproduzierbar aufgebaut werden kann
* der Intel NUC als zentrale Git- und Deployment-Instanz funktioniert
* Änderungen automatisiert auf mehrere Zielsysteme ausgerollt werden
* FortiGate-Policies per Code angewendet werden
* der Raspberry Pi per Code konfiguriert oder aktualisiert wird
* Angriffssimulationen reproduzierbar ausführbar sind
* Logs und Nachweise zentral dokumentiert werden

---

# Nicht-Ziele

Nicht Teil des Projekts sind:

* Public-Cloud-Umgebungen
* produktive Sicherheitstests gegen fremde Systeme
* vollständige Unternehmens-Sicherheitsplattformen

Der Fokus liegt auf einem didaktischen, lokalen und reproduzierbaren Cyber-Defense Lab.

---

# Mögliche Erweiterungen

* Honeypot-Integration
* zusätzliche Netzsegmente
* automatisches Alerting
* Konfigurationsmanagement mit Ansible
* erweiterte Korrelationen im **SIEM (Security Information and Event Management – Sicherheitsinformations- und Ereignismanagement)**

---



> [⇧ **Nach oben**](#README.md)

---


