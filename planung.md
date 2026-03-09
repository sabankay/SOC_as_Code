![Cyber Devence Homelab](/images/planung.png)

# Projektplanung – DevSecOps Cyber-Defense Homelab (On-Premise)

## 1. Ausgangslage
Im Homelab existiert eine FortiGate-Firewall und ein Cisco Switch. Ein Raspberry Pi betreibt einen DNS-Dienst (Domain Name System – Namensauflösung), ein Intel NUC (Linux, 12 GB RAM – Random Access Memory, Arbeitsspeicher) steht als Server zur Verfügung.

## 2. Projektidee
Aufbau eines lokalen Cyber-Defense Labs (SOC-Light – Security Operations Center, Mini-Sicherheitsbetrieb), bei dem Services, Firewall-Policies und Angriffssimulationen vollständig **code-basiert** aus Git reproduzierbar deployt werden (DevSecOps – Development Security Operations).

## 3. Projektziele

### 3.1 Hauptziel
Implementierung einer reproduzierbaren, lokalen DevSecOps-Umgebung, in der:
- Services (z.B. Monitoring / SIEM – Security Information and Event Management) automatisiert deployt werden (GitOps / CI/CD – Continuous Integration / Continuous Deployment).
- Firewall-Regeln der FortiGate als Code verwaltet und automatisiert angewendet werden (Policy-as-Code – Richtlinien als Code).
- definierte Angriffssimulationen als Services gestartet werden (Attack-as-Code – Angriffssimulation als Code), um Erkennung und Logging nachweisbar zu testen.

### 3.2 Teilziele (messbar)
1. **GitOps Deployment**
   - Ein Repository enthält alle Deployments (Docker Compose – Multi-Container Deployment Tool) und Pipeline-Konfiguration.
   - Ein Push (Commit) triggert ein automatisches Deployment auf dem Intel NUC.
2. **Policy-as-Code**
   - Mindestens 3–5 Firewall-Policies werden als Dateien (z.B. YAML/JSON – Konfigurationsformate) versioniert.
   - Ein Script wendet diese Policies über die FortiGate-API (Application Programming Interface – Programmschnittstelle) automatisiert an.
3. **Attack-as-Code**
   - Mindestens 3 standardisierte Angriffssimulationen sind als Container/Jobs reproduzierbar startbar.
   - Für jede Simulation werden Logs/Events gesammelt und ausgewertet (Nachweis).
4. **Monitoring & Evidence**
   - Ereignisse (Firewall-Logs, Host-Logs, DNS-Logs) werden zentral sichtbar gemacht (Dashboard/Reports).
   - Pro Use Case existiert ein Evidence-Pack (Beweis-Set): Screenshots, Logauszüge, Beschreibung, Ergebnis.

## 4. Nicht-Ziele (Abgrenzung)
- Keine Nutzung von Public Cloud (z.B. AWS – Amazon Web Services, Azure – Microsoft Azure).
- Kein produktiver Penetration Test (Pentest – Sicherheitstest) gegen fremde Systeme.
- Kein vollständiger Unternehmens-SOC Ausbau; Fokus ist ein didaktisches Lab mit klar definierten Use Cases.

## 5. Projektumfang / Deliverables (Abgabe)

### 5.1 Repository-Struktur
```
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
│   └── healthcheck.sh
├── attacks/
│   ├── README.md
│   └── scenarios/
├── policies/
│   ├── README.md
│   └── fortigate/
├── evidence/
│   └── .gitkeep
└── pipeline/
    └── gitea-actions.yml
```

### 5.2 Technische Deliverables
- Lauffähiger Deployment-Prozess auf Intel NUC (Linux).
- Automatisiertes Anwenden von FortiGate Policies (mind. 3–5 Regeln).
- 3 Angriffssimulationen + Auswertung.
- Dokumentation inkl. Entscheidungspunkten (Warum diese Tools/Architektur?).

## 6. Systemübersicht (Soll-Architektur)

### 6.1 Rollen der Hardware
- **FortiGate**
  - Zentrale Segmentierung und Policy Enforcement (PEP – Policy Enforcement Point, Richtliniendurchsetzung)
  - Logquelle via Syslog (System Logging Protocol – Logübertragung)
- **Raspberry Pi**
  - DNS (z.B. Pi-hole) + optionale Logquelle / Agent (z.B. Wazuh Agent)
- **Intel NUC**
  - Git Server / Runner (CI/CD Ausführung)
  - Docker Engine (Container Runtime – Container Ausführungsumgebung)
  - Services (Monitoring / SIEM / Dashboards)

### 6.2 Datenflüsse (High Level)
- FortiGate Logs → NUC (Log Collector / SIEM)
- Raspberry Pi Logs (DNS) → NUC (Log Collector / SIEM)
- Git Push → Pipeline → NUC Deployment
- Attack Jobs → erzeugen Events → Logs/Dashboards

## 7. Use Cases (Security Tests, reproduzierbar)

### UC-1 Portscan Simulation
- Ziel: Erzeugen von Firewall/Traffic Events, sichtbar in Logs/Dashboards.
- Erfolgskriterium: Scan-Ereignisse werden erkannt und dokumentiert.

### UC-2 Brute Force Simulation (harmlos, Testdienst)
- Ziel: Viele fehlgeschlagene Logins auf einen Testdienst generieren.
- Erfolgskriterium: Auth-Fehler sind sichtbar; Alert/Rule reagiert.

### UC-3 DNS Anomaly Simulation
- Ziel: Ungewöhnliches DNS-Verhalten erzeugen (z.B. viele Requests).
- Erfolgskriterium: DNS-Events sind in Pi-hole/Logs sichtbar; Auswertung möglich.

## 8. Meilensteine & Zeitplan (Quartal, ca. 25–30h)

### M1 – Planung & Design (Woche 1–2)
- Architektur- und Netzwerkdiagramm aktualisieren
- Repo-Struktur erstellen
- Toolauswahl begründen

### M2 – GitOps Basis (Woche 3–4)
- Git Server (Gitea oder GitLab) auf NUC
- Runner/Agent einrichten
- Pipeline für `docker compose up -d` implementieren
- Erfolgstest: Ein Commit deployt Services reproduzierbar

### M3 – Policy-as-Code FortiGate (Woche 5–7)
- Policies definieren (3–5 Kernregeln)
- Apply-Script (API) implementieren
- Logging / Change Nachweis (Changelog, Screenshots)

### M4 – Attack-as-Code (Woche 8–9)
- 3 Simulationen als Containerjobs/Compose definieren
- Start/Stop automatisieren (manuell oder Pipeline Stage)
- Evidenzen sammeln (Logs/Screenshots)

### M5 – Monitoring, Auswertung, Dokumentation (Woche 10–12)
- Dashboards/Reports erstellen
- Pro Use Case: Ablauf + Nachweis + Ergebnis + Root Cause Analysis (RCA – Ursachenanalyse)
- Abschlussfazit, Lessons Learned (Lernerfahrungen)

## 9. Risiken & Gegenmassnahmen
- **Ressourcenlimit (12 GB RAM)**: Services schlank halten, nicht zu viele Komponenten gleichzeitig.
- **Komplexität FortiGate API**: Scope klein (3–5 Policies), Fokus auf Nachweisbarkeit.
- **Zeitlimit**: Priorität auf reproduzierbare Deployments + 3 Use Cases + saubere Doku.

## 10. Qualitätskriterien (Definition of Done)
- Ein neuer Rechner könnte das Repo klonen und mit dokumentierten Schritten das Lab reproduzieren (Reproduzierbarkeit).
- Pipeline deployt Services erfolgreich (GitOps).
- Policies werden per Code angewendet und sind versioniert (Policy-as-Code).
- 3 Angriffssimulationen sind reproduzierbar ausführbar und erzeugen nachweisbar Logs/Events (Attack-as-Code).
- Dokumentation ist vollständig (Diagramme, Konfigurationen, Testprotokolle, Evidence).

## 11. Zuordnung zur Kompetenzmatrix (Kurzmapping)
- **A1 Ermittlung erforderlicher Services**: Tool-/Servicevergleich, Architekturentscheidungen
- **B1 Integrationskonzept**: Netzwerk-/Log-Flows, Deploymentstrategie
- **C1 Konfiguration & Monitoring**: Dashboards, Alerting, Performance/Healthchecks
- **D1 Netzwerkverbindungen**: Segmentierung, Syslog-Flows, Tests
- **E1 Service-Integration**: GitOps, Compose-Services, Schnittstellen (API)
- **E2 Betrieb & Überwachung**: Betriebskonzept, Wartung, Monitoring, Alerts
- **F1 Fehleranalyse**: Testfälle, Loganalyse, RCA
- **I1 Dokumentation**: Diagramme, Prozesse, reproduzierbare Anleitungen



## Zusatzziele Eventuell
- Honeypot