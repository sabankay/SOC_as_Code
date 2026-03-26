# Betriebliche Optimierungen am Homelab-Stack

## Ziel

Der bestehende Stack funktionierte bereits, hatte aber noch typische Homelab-Schwächen:

- Secrets lagen direkt im Compose
- Log-Retention war nicht überall konsistent
- Metriken waren schwächer ausgebaut als Logs
- Healthchecks fehlten für mehrere Kernservices
- Betriebswissen war nur teilweise dokumentiert

Die folgenden Anpassungen sollten den Stack nicht neu erfinden, sondern **stabiler, wartbarer und nachvollziehbarer** machen.

---

## Umgesetzte Verbesserungen

### 1. Secrets in `.env` ausgelagert

**Geändert:**

- Grafana- und Wazuh-Credentials aus `hosts/nuc/compose.yml` entfernt
- `hosts/nuc/.env` und `hosts/nuc/.env.example` ergänzt
- Deploy-Workflow so angepasst, dass die Env-Datei aus einem CI-Secret geschrieben werden kann

**Warum:**

- Passwörter stehen nicht mehr direkt im Compose
- lokale und CI-basierte Deployments nutzen denselben Mechanismus
- Änderungen an Credentials werden einfacher und sauberer

---

### 2. Docker-Loglimits gesetzt

**Geändert:**

- einheitliche `json-file`-Loglimits pro Container
- Begrenzung auf zwei Dateien à 25 MB

**Warum:**

- Containerlogs wachsen sonst unkontrolliert
- das ist gerade auf einem NUC unnötiger Speicherverbrauch
- kleine Limits reichen im Homelab aus, weil die eigentliche Analyse ohnehin in Loki erfolgt

---

### 3. Rohlogs per Logrotate begrenzt

**Geändert:**

- Logrotate-Regel für:
  - `syslog-ng`
  - `suricata`
  - `wazuh/runtime/logs`
- Installationsschritt in den NUC-Deploy aufgenommen

**Warum:**

- Loki-Retention alleine reicht nicht
- die Rohdateien auf dem Host würden sonst weiter anwachsen
- so bleibt die Aufbewahrung auch außerhalb von Loki kontrolliert

---

### 4. Prometheus und Node Exporter ergänzt

**Geändert:**

- `prometheus` und `node-exporter` in den NUC-Stack aufgenommen
- Prometheus als zusätzliche Grafana-Datenquelle provisioniert

**Warum:**

- bisher war der Stack stark log-zentriert
- für Betrieb und Kapazität sind Host-Metriken genauso wichtig
- damit lassen sich CPU, RAM, Filesystem und Servicezustand sauber überwachen

---

### 5. Healthchecks ergänzt

**Geändert:**

- Healthchecks für:
  - Grafana
  - Loki
  - Promtail
  - Atomic Validator API
  - Atomic Validator Worker
  - Atomic Validator Agent
  - Prometheus
  - Node Exporter
- bestehendes `scripts/healthcheck.sh` erweitert

**Warum:**

- der Stack wird dadurch schneller prüfbar
- Compose kann Dependencies zuverlässiger aufbauen
- Fehler sind schneller sichtbar als bei reiner Logsuche

---

### 6. Kleine Resource-Grenzen gesetzt

**Geändert:**

- moderate `mem_limit`-Werte für unkritische Dienste

**Warum:**

- verhindert, dass kleine Hilfsdienste unnötig viel Speicher nehmen
- sinnvoll auf einem kompakten Homelab-System
- genug Kontrolle, ohne den Stack unnötig kompliziert zu machen

---

### 7. Betriebsdokumentation ergänzt

**Geändert:**

- Runbook
- Deployment-Doku
- Architekturübersicht
- Detection-Matrix für Atomic Validator und Wazuh

**Warum:**

- Änderungen sollen nicht nur funktionieren, sondern auch später nachvollziehbar bleiben
- gerade bei einem größeren Homelab hilft kurze Dokumentation mehr als reines Ausprobieren
- die Detection-Matrix verbindet Test, erwartete Detection und Query an einem Ort

---

## Ergebnis

Der Stack ist nach diesen Anpassungen nicht „größer“, aber deutlich sauberer im Betrieb:

- weniger Klartext-Secrets
- weniger unkontrolliertes Logwachstum
- bessere Sicht auf Host und Services
- klarere Prüf- und Deploy-Pfade
- nachvollziehbarere Detection-Validierung

Für ein Homelab ist genau das der wichtigste Gewinn: **mehr Stabilität und weniger Überraschungen im Alltag**.
