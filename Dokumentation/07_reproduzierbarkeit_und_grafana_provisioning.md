# Reproduzierbarkeit, Validierung und Grafana-Provisioning

## Ziel

Nach dem Umbau der Service-Struktur lag der nächste sinnvolle Schritt darin, den Betrieb stabiler und nachvollziehbarer zu machen.

Dafür wurden drei Bereiche verbessert:

- feste Versionen statt ungebundener `latest`-Tags
- automatische Validierung vor dem Deploy
- versionierte Dashboards und Alert-Regeln in Grafana

---

## 1. Feste Image-Tags

Mehrere Container liefen bisher mit `latest`.

Das ist praktisch für schnelle Tests, aber im Betrieb problematisch:

- ein Deploy kann sich verändern, obwohl im Repository keine sichtbare Konfigurationsänderung gemacht wurde
- Fehler sind schwerer reproduzierbar
- Rollbacks werden unklar

**Warum geändert:**

- Deploys sollen reproduzierbar bleiben
- Versionen sollen bewusst aktualisiert werden
- Betriebsfehler sollen sich besser eingrenzen lassen

Deshalb wurden die wichtigsten Monitoring-Komponenten auf feste Tags gezogen.

---

## 2. Validierung vor dem Deploy

Vorher wurde direkt deployed. Fehler in Compose-Dateien oder Dashboards wären deshalb oft erst auf dem Zielhost aufgefallen.

Neu wurde ein Validierungsskript ergänzt, das vor dem Deployment läuft.

Geprüft werden dabei zum Beispiel:

- die kombinierte Compose-Konfiguration des NUC
- die kombinierte Compose-Konfiguration des Raspberry Pi
- die JSON-Struktur versionierter Grafana-Dashboards
- die dokumentierten Umgebungsvariablen

**Warum geändert:**

- Fehler sollen früher sichtbar werden
- Deployments sollen kontrollierter und sicherer ablaufen
- die CI-Pipeline soll mehr Qualitätssicherung übernehmen

Zusätzlich wurde ein eigener Workflow für die Validierung ergänzt.

---

## 3. Grafana-Provisioning

Das aktuelle Dashboard war vorhanden, aber nicht sauber als versionierte Betriebsdefinition im Repository abgelegt.

Deshalb wurden übernommen:

- ein versioniertes Dashboard
- feste Datasource-UIDs für Loki und Prometheus
- erste Alert-Regeln für die Verfügbarkeit zentraler Monitoring-Komponenten

**Warum geändert:**

- Dashboards sollen nach einem Redeploy automatisch wieder verfügbar sein
- Alerting soll nicht manuell in der Oberfläche nachgebaut werden müssen
- Visualisierung und Monitoring gehören ebenfalls ins GitOps-Modell

---

## 4. Restore-Dokumentation

Mit mehr persistenter Konfiguration steigt auch die Bedeutung eines sauberen Restore-Prozesses.

Deshalb wurde zusätzlich eine Restore-Dokumentation ergänzt.

Sie beschreibt:

- welche Dateien und Volumes gesichert werden sollten
- in welcher Reihenfolge ein Restore sinnvoll ist
- wie der Stack danach wieder gestartet und geprüft wird

**Warum geändert:**

- ein Backup ist nur nützlich, wenn auch klar ist, wie ein Restore abläuft
- bei einem Host-Ausfall oder kaputten Deploy spart das Zeit und reduziert Unsicherheit

---

## Ergebnis

Die Änderungen bringen drei konkrete Vorteile:

- Der Stack ist reproduzierbarer.
- Fehler werden früher erkannt.
- Grafana wird stärker als Teil des Repositorys und nicht nur als manuell gepflegte Oberfläche betrieben.

Für ein Homelab ist das ein sinnvoller Reifegrad-Schritt: weniger improvisiert, besser prüfbar und einfacher wiederherzustellen.
