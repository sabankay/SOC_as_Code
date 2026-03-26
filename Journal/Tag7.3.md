# 🗓️ Tag: 26.3.2026

## 🎯 Tagesziele
- Ziel 1: Monitoring-Stack reproduzierbarer machen
- Ziel 2: Deployments vor dem Ausrollen automatisch validieren
- Ziel 3: Grafana-Dashboards und Alerting versioniert ins Repository übernehmen

---

## ✅ Tagesresultate
Was habe ich heute konkret erreicht?

- Resultat 1: Kernkomponenten wie Grafana, Loki, Promtail, Prometheus, Node Exporter und Suricata wurden auf feste Image-Tags umgestellt.
- Resultat 2: Ein Validierungsskript für die Compose-Stacks und Grafana-Dashboards wurde ergänzt.
- Resultat 3: Die Gitea-Workflows für NUC und Raspberry Pi prüfen den Stack jetzt vor dem Deploy.
- Resultat 4: Ein versioniertes Grafana-Dashboard wurde direkt im Repository abgelegt und per Provisioning eingebunden.
- Resultat 5: Erste Grafana-Alert-Regeln für die Erreichbarkeit der Monitoring-Komponenten wurden ergänzt.
- Resultat 6: Eine Restore-Dokumentation für den NUC-Stack wurde ergänzt.

---

## ⚠️ Probleme & Reflexion
Welche Probleme sind aufgetreten und wie habe ich sie gelöst?

**Problem:**
`latest`-Tags machen Deploys unberechenbar, weil sich Images ohne sichtbare Änderung im Repository verändern können.

**Lösung:**
Die wichtigsten Container wurden auf feste Versionen gesetzt.

**Reflexion:**
Für ein Homelab ist das besonders wichtig, weil Fehler sonst schwerer reproduzierbar sind und Rollbacks unklar werden.

---

**Problem:**
Konfigurationsfehler in Compose oder Grafana würden erst beim echten Deploy auffallen.

**Lösung:**
Ich habe ein Validierungsskript eingebaut und die Workflows so erweitert, dass diese Prüfung vor dem Deployment läuft.

**Reflexion:**
Ein kleiner Vorab-Check spart viel Zeit, weil Fehler früher sichtbar werden und nicht erst auf dem produktiven Host auffallen.

---

**Problem:**
Grafana war bisher eher manuell konfiguriert und dadurch nicht vollständig GitOps-fähig.

**Lösung:**
Das Dashboard und die Alert-Regeln wurden als Dateien ins Repository übernommen und über Grafana-Provisioning eingebunden.

**Reflexion:**
Dashboards und Alerts gehören bei so einem Setup genauso in die Versionskontrolle wie Compose-Dateien oder Skripte.

---

## 📚 Eingesetzte Ressourcen
Welche Quellen habe ich benutzt?

- bestehende Compose-Dateien und Deploy-Skripte im Projekt
- bestehende Grafana-Provisioning-Struktur
- interne Deployment- und Runbook-Dokumentation
- ChatGPT / KI Erklärung

**Kurz-Zusammenfassung der wichtigsten Erkenntnisse:**

- Feste Versionen erhöhen die Stabilität und Nachvollziehbarkeit.
- Validierung vor dem Deploy ist ein einfacher, aber sehr wirksamer Qualitätsschritt.
- Dashboards und Alert-Regeln sollten versioniert werden.

---

## 🧪 Eigene praktische Übung
Was habe ich selbst ausprobiert?

**Beschreibung der Übung:**
Ich habe den NUC- und Pi-Stack vor dem Deployment automatisch validiert und ein Grafana-Dashboard sowie Alert-Regeln direkt aus Dateien laden lassen.

**Code / Umsetzung:**
```code
bash scripts/validate-stack.sh

docker compose \
  --project-directory hosts/nuc \
  --env-file hosts/nuc/.env \
  -f services/common/compose.monitoring.yml \
  -f hosts/nuc/compose.yml \
  config
```
