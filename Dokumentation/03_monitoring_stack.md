# Monitoring Stack Dokumentation

## 1. Ziel des Monitoring Stacks

Der Monitoring Stack dient zur **zentralen Sammlung, Verarbeitung und Visualisierung von Sicherheits- und Systemlogs** im Cyber Defense Lab.

Er ermöglicht:

* zentrale **Logaggregation**
* **Intrusion Detection**
* **Angriffserkennung**
* **Visualisierung von Events**
* **Security Monitoring (SOC-Dashboard)**

Der Stack läuft auf dem **Intel NUC** und sammelt Logs von:

* Intel NUC
* Raspberry Pi
* FortiGate Firewall
* Suricata IDS
* Docker Containern

---

# 2. Architektur

Die Architektur basiert auf dem **Grafana LGTM Stack**.

```text
Devices / Services
      │
      │ Logs / Syslog
      ▼
syslog-ng
      │
      ▼
Promtail
      │
      ▼
Loki
      │
      ▼
Grafana
```

Zusätzlich:

```text
Network Traffic
      │
      ▼
Suricata IDS
      │
      ▼
eve.json Logs
      │
      ▼
Promtail → Loki → Grafana
```

---

# 3. Komponenten des Monitoring Stacks

## 3.1 Grafana

Grafana ist die **Visualisierungsplattform** für Logs und Security Events.

Funktionen:

* Dashboards
* Loganalyse
* Alerting
* Geomap Visualisierung
* Security Monitoring

Port:

```text
3000
```

Login:

```text
admin / admin
```

---

## 3.2 Loki (Log Aggregation System)

Loki ist eine **Logdatenbank für strukturierte Logs**.

Eigenschaften:

* speichert Logs effizient
* nutzt Labels statt vollständiger Indexierung
* integriert mit Grafana
* unterstützt LogQL Queries

Port:

```text
3100
```

Beispiel Query:

```logql
{job="suricata"} |= "alert"
```

---

## 3.3 Promtail (Log Collector)

Promtail sammelt Logs von verschiedenen Quellen und sendet sie an Loki.

Logquellen:

* Systemlogs (`/var/log`)
* Docker Logs
* Suricata IDS Logs
* Syslog Server Logs

Promtail übernimmt außerdem:

* Parsing von JSON Logs
* Labeling von Logs
* Log Enrichment

---

## 3.4 syslog-ng (Syslog Server)

syslog-ng fungiert als **zentraler Syslog Server**.

Er sammelt Logs von Netzwerkgeräten wie:

* FortiGate Firewall
* Raspberry Pi
* anderen Netzwerkgeräten

Ports:

```text
UDP 514
TCP 601
```

Die Logs werden gespeichert unter:

```text
/config/logs/
```

Diese Logs werden anschließend von Promtail verarbeitet.

---

## 3.5 Suricata IDS

Suricata ist ein **Network Intrusion Detection System (NIDS)**.

Es überwacht Netzwerkverkehr und erkennt:

* Port Scans
* ICMP Scans
* Suspicious Traffic
* bekannte Angriffssignaturen

Suricata erzeugt Logs im JSON Format:

```text
eve.json
```

Diese enthalten:

* Source IP
* Destination IP
* Protocol
* Alert Signatures
* Event Types

Beispiel Event:

```json
{
 "event_type": "alert",
 "src_ip": "192.168.188.20",
 "dest_ip": "192.168.188.50",
 "alert": {
   "signature": "Possible SYN scan detected"
 }
}
```

Diese Logs werden anschließend von Promtail in Loki ingestiert.

---

# 4. Log Flow

Der komplette Logfluss im Monitoring Stack:

```text
Devices / Services
       │
       ▼
syslog-ng
       │
       ▼
Promtail
       │
       ▼
Loki
       │
       ▼
Grafana
```

IDS Events:

```text
Network Traffic
       │
       ▼
Suricata IDS
       │
       ▼
eve.json
       │
       ▼
Promtail
       │
       ▼
Loki
       │
       ▼
Grafana Dashboard
```

---

# 5. Deployment

Der Monitoring Stack wird über **Docker Compose** bereitgestellt.

Services:

```text
grafana
loki
promtail
syslog-ng
suricata
```

Start des Stacks:

```bash
docker compose up -d
```

---

# 6. Logquellen

Der Stack sammelt Logs von mehreren Quellen.

## System Logs

```text
/var/log/syslog
/var/log/auth.log
```

Erkennung:

* SSH Login Versuche
* System Events

---

## Docker Logs

```text
/var/lib/docker/containers/*/*.log
```

Erkennung:

* Container Fehler
* Service Logs

---

## Suricata IDS

```text
/suricata/logs/eve.json
```

Erkennung:

* Port Scans
* Network Attacks
* Suspicious Traffic

---

## Syslog Devices

```text
/config/logs/
```

Erkennung:

* Firewall Logs
* Router Logs
* Raspberry Pi Logs

---

# 7. Grafana Dashboards

Das SOC Dashboard zeigt verschiedene Sicherheitsmetriken.

## IDS Alerts

Zeigt erkannte Angriffe.

Query:

```logql
{job="suricata"} |= "alert"
```

---

## Nmap / Scan Detection

Erkennung von Portscans.

Query:

```logql
{job="suricata"} |= "scan"
```

---

## Top Attacker IP

Ermittelt die aggressivsten Angreifer.

```logql
topk(10, sum by (src_ip) (count_over_time({job="suricata"} |= "alert"[10m])))
```

---

## Scan Timeline

Zeigt Angriffsaktivität über Zeit.

```logql
count_over_time({job="suricata"} |= "scan"[1m])
```

---

## SSH Brute Force Detection

Erkennung fehlgeschlagener SSH Logins.

```logql
{job="auth"} |= "Failed password"
```

---

# 8. Angriffssimulation

Angriffe können im Lab simuliert werden.

Beispiel:

## Nmap Scan

```bash
nmap -sS 192.168.188.50
```

Erwartete Ergebnisse:

* Suricata erzeugt Alert
* Promtail sendet Log an Loki
* Grafana Dashboard zeigt Detection

---

# 9. Erweiterungen

Der Monitoring Stack kann erweitert werden um:

### GeoIP Attack Mapping

Darstellung der Herkunft von Angriffen auf einer Weltkarte.

---

### Wazuh HIDS

Hostbasierte Intrusion Detection.

Überwacht:

* File Integrity
* Rootkits
* Systemänderungen

---

### Atomic Red Team

Automatisierte Angriffssimulation.

Pipeline:

```text
Attack Simulation
       │
       ▼
Detection
       │
       ▼
Grafana Visualization
       │
       ▼
Evidence Collection
```

---

# 10. Vorteile dieser Architektur

Der Monitoring Stack bietet:

* zentrale Loganalyse
* Security Monitoring
* Angriffserkennung
* einfache Erweiterbarkeit
* vollständige Open Source Lösung

Er bildet die Grundlage für ein **Security Operations Center (SOC)** im Cyber Defense Lab.

---

