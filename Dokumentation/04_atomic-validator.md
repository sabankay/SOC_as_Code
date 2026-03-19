# Atomic Validator für Detection-Nachweise

## 1. Ziel

Im bisherigen Monitoring-Stack konnten Logs und Security Events zentral gesammelt und visualisiert werden. Es fehlte jedoch ein reproduzierbarer Mechanismus, um nachzuweisen, **ob definierte Detection-Pfade wirklich funktionieren**.

Dafür wurde ein zusätzlicher Dienst entwickelt: der **Atomic Validator**.

Der Atomic Validator erweitert das Lab um folgende Funktionen:

* automatisierte Ausführung ungefährlicher Linux-Atomics
* Abgleich der erzeugten Logs mit **Loki**
* Bewertung, ob eine Detection **validiert**, **teilweise belegt** oder **nicht belegt** ist
* Visualisierung der Ergebnisse in einer eigenen Weboberfläche
* Nachweis der Detection direkt anhand von konkreten Log-Einträgen

Damit wird aus reinem Logging ein überprüfbarer Detection-Workflow.

---

## 2. Ausgangslage

Das Projekt enthält bereits:

* einen Git-Server mit **Gitea**
* eine GitOps Deployment-Pipeline
* einen Monitoring-Stack aus **Grafana**, **Loki**, **Promtail**, **syslog-ng** und **Suricata**

Diese Komponenten liefern bereits Rohdaten und Visualisierung. Für den Nachweis von Regeln und Erkennungen war aber bisher keine dedizierte Test- und Bewertungslogik vorhanden.

Der Atomic Validator schliesst genau diese Lücke.

---

## 3. Architektur

Der Atomic Validator besteht aus drei Diensten:

| Komponente | Aufgabe |
| --- | --- |
| `atomic-validator-agent` | Führt erlaubte Tests zyklisch aus |
| `atomic-validator-api` | Stellt Weboberfläche und REST-API bereit |
| `atomic-validator-worker` | Prüft in Loki, ob für eine Execution passende Evidence vorhanden ist |

Ergänzt wird dies durch:

* `policy.yml` für erlaubte Tests und Monitoring-Regeln
* `generate_inventory.py` zur Erzeugung eines Linux-Testinventars
* eine SQLite-Datenbank für Tests, Executions und Detections

High-Level Ablauf:

```text
Agent startet Test
    │
    ▼
Execution wird an API gemeldet
    │
    ▼
Agent schreibt Marker "ATOMIC_VALIDATOR ..." in Docker-Logs / Syslog
    │
    ▼
Promtail sammelt Logs und sendet sie an Loki
    │
    ▼
Worker fragt Loki mit definierter Query ab
    │
    ▼
Detection wird als stark / schwach gespeichert
    │
    ▼
Web-UI zeigt Status und Evidence an
```

---

## 4. Technische Umsetzung

### 4.1 Inventory-Generierung

Die Datei `generate_inventory.py` liest die Atomic-Red-Team YAML-Dateien aus dem eingebundenen Atomics-Repository und erzeugt daraus ein Linux-Inventar.

Wichtige Punkte:

* nur Linux-kompatible Tests werden berücksichtigt
* blockierte Techniken werden ausgeschlossen
* Tests werden standardmässig deaktiviert angelegt
* nur explizit erlaubte Test-IDs aus `policy.yml` werden automatisch aktiviert

Dadurch bleibt die Testmenge kontrollierbar und sicher.

---

### 4.2 Sichere Testauswahl

Um das Lab nicht durch destruktive oder unkontrollierte Atomics zu gefährden, wurde die Policy auf wenige harmlose Tests reduziert.

Aktiviert wurden nur ungefährliche Linux-Tests wie zum Beispiel:

* `t1033-atomic-2`
* `t1059-004-atomic-5`
* `t1059-004-atomic-6`
* `t1059-004-atomic-7`
* `t1059-004-atomic-8`
* `t1059-004-atomic-9`
* `t1059-004-atomic-11`
* `t1059-004-atomic-13`

Diese Tests erzeugen kontrollierte Ereignisse, ohne produktive Dienste oder Systemzustände zu gefährden.

---

### 4.3 Evidence-Nachweis mit Loki

Die Tests erzeugen während Start und Abschluss Marker der Form:

```text
ATOMIC_VALIDATOR host=<host> execution_id=<id> test_id=<id> technique_id=<id> phase=<phase> status=<status>
```

Diese Marker werden:

* in die Docker-Logs geschrieben
* zusätzlich per `logger` an das Host-Logging übergeben

Der Worker sucht danach in Loki über definierte LogQL-Queries.

Beispiel:

```logql
{job="docker"} |= "ATOMIC_VALIDATOR" |= "execution_id={execution_id}" |= "phase=finish" |= "status=completed"
```

Wenn die Query Treffer liefert, wird eine Detection gespeichert. Dazu gehören:

* Evidence-Level
* Titel der Detection
* Match-Modus
* verwendete Query
* konkrete Loki-Einträge als Nachweis

---

### 4.4 Datenmodell

Die SQLite-Datenbank enthält drei zentrale Tabellen:

| Tabelle | Inhalt |
| --- | --- |
| `tests` | Definitionen und Monitoring-Konfigurationen |
| `executions` | einzelne Testausführungen |
| `detections` | Evidence-Treffer aus Loki |

Dadurch ist nachvollziehbar:

* welcher Test gelaufen ist
* wann er lief
* ob Loki passende Evidence geliefert hat
* anhand welcher Logs die Detection bewertet wurde

---

## 5. Weboberfläche

Für den Atomic Validator wurde eine eigene Weboberfläche gebaut.

Ziele der UI:

* weniger unübersichtlich als eine rohe JSON-Ausgabe
* Fokus auf **validierte Detection-Pfade**
* schnelle Übersicht über Automation, letzte Läufe und Threat-Mappings
* direkte Anzeige der Beweise

Die Oberfläche enthält:

* KPI-Karten für validierte, teilweise belegte und unbelegte Tests
* Bereich für automatisch aktivierte Tests
* Bereich für letzte Executions
* Bereich für Threat-Mappings
* Evidence-Block pro validiertem Test

Zusätzlich wurde die Darstellung verbessert:

* Zeitstempel werden lesbar formatiert
* validierte Tests zeigen die konkrete Loki-Evidence
* die verwendete Query und Log-Zeilen werden sichtbar gemacht

Damit ist sofort ersichtlich, **warum** ein Test als validiert bewertet wurde.

---

## 6. Automatisierung

Der Agent wurde als eigener Compose-Dienst integriert und läuft dauerhaft.

Wichtige Eigenschaften:

* zyklische Ausführung im Loop
* fest definierter Hostname
* persistenter State
* Forcelauf bei jedem geplanten Intervall

Damit werden die freigegebenen Tests regelmässig erneut ausgeführt und die Detection-Pfade laufend überprüft.

---

## 7. Typische Probleme und Lösungen

### Problem 1: Tests wurden zwar ausgeführt, aber nicht validiert

Ursache:

* Marker landeten nicht zuverlässig in Loki

Lösung:

* `ATOMIC_VALIDATOR` Marker zusätzlich auf `stdout` schreiben
* Promtail liest die Docker-Container-Logs

---

### Problem 2: UI zeigte Executions, aber 0 Tests

Ursache:

* `linux_inventory.json` war leer oder inkonsistent geladen

Lösung:

* Inventory-Loading gehärtet
* bei leerem Inventory wird automatisch neu generiert
* bei erneut leerem Ergebnis startet der Dienst nicht still weiter

---

### Problem 3: Agent zeigte `eligible=0`

Ursache:

* Cooldown und State verhinderten weitere zyklische Ausführungen

Lösung:

* Agent in Compose mit `--force` im Loop betreiben

---

## 8. Ergebnis

Mit dem Atomic Validator wurde das Lab um einen wichtigen Baustein erweitert:

* Detection-Tests laufen automatisiert
* Loki-Treffer werden maschinell bewertet
* der Nachweis ist im Dashboard sichtbar
* validierte Detection-Pfade lassen sich direkt belegen

Das System erfüllt damit den Anspruch des Projekts deutlich besser:

Nicht nur Logs werden gesammelt, sondern die Wirksamkeit von Detection-Regeln wird reproduzierbar geprüft und dokumentiert.

---

## 9. Einordnung ins Gesamtprojekt

Der Atomic Validator ergänzt die bestehenden Projektsäulen sinnvoll:

* **GitOps**: Konfiguration und Policies sind versioniert
* **IaC**: Dienste laufen vollständig über Docker Compose und Code
* **Attack-as-Code**: standardisierte Tests werden reproduzierbar ausgeführt
* **Monitoring & Evidence**: Detections werden nicht nur angezeigt, sondern belegt

Damit ist der Atomic Validator ein zentraler Nachweisbaustein für das Cyber-Defense Lab.
