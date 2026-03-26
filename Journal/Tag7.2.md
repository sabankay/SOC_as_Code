# 🗓️ Tag: 26.3.2026

## 🎯 Tagesziele
- Ziel 1: Repository-Struktur für mehrere Hosts sauberer aufteilen
- Ziel 2: gemeinsame und host-spezifische Services klar trennen
- Ziel 3: Deployments an die neue Struktur anpassen

---

## ✅ Tagesresultate
Was habe ich heute konkret erreicht?

- Resultat 1: Ein neuer Bereich `services/common` für gemeinsame Dienste wurde eingeführt.
- Resultat 2: `promtail` und `node-exporter` wurden aus den Host-Compose-Dateien in eine gemeinsame Compose-Datei ausgelagert.
- Resultat 3: Die Host-Compose-Dateien für NUC und Raspberry Pi enthalten jetzt nur noch die host-spezifischen Teile und Overrides.
- Resultat 4: Die Deploy-Skripte für NUC und Raspberry Pi wurden auf den kombinierten Compose-Aufruf umgestellt.
- Resultat 5: Die Architektur- und Deployment-Dokumentation wurde an die neue Struktur angepasst.

---

## ⚠️ Probleme & Reflexion
Welche Probleme sind aufgetreten und wie habe ich sie gelöst?

**Problem:**
Gemeinsame Dienste wie `promtail` waren mehrfach in verschiedenen Host-Dateien definiert.

**Lösung:**
Ich habe eine zentrale Compose-Datei unter `services/common` eingeführt und die Host-Dateien auf die host-spezifischen Angaben reduziert.

**Reflexion:**
Sobald mehrere Geräte überwacht werden, wird Duplikation schnell unübersichtlich. Eine gemeinsame Basis vereinfacht spätere Änderungen deutlich.

---

**Problem:**
Die Deploy-Skripte starteten bisher immer nur die jeweilige Host-Compose-Datei.

**Lösung:**
Die Skripte wurden so angepasst, dass sie zuerst die gemeinsame Compose-Datei und danach die host-spezifische Datei laden.

**Reflexion:**
Die Strukturänderung ist nur dann sinnvoll, wenn sie auch im realen Deployment verwendet wird. Sonst bleibt sie reine Repo-Kosmetik.

---

## 📚 Eingesetzte Ressourcen
Welche Quellen habe ich benutzt?

- vorhandene Host-Compose-Dateien im Projekt
- bestehende Deploy-Skripte
- interne Architektur- und Deployment-Doku
- ChatGPT / KI Erklärung

**Kurz-Zusammenfassung der wichtigsten Erkenntnisse:**

- Gemeinsame Agenten sollten zentral gepflegt werden.
- Host-spezifische Dateien bleiben dadurch kleiner und verständlicher.
- Eine saubere Compose-Aufteilung lohnt sich vor allem, wenn weitere Geräte dazukommen.

---

## 🧪 Eigene praktische Übung
Was habe ich selbst ausprobiert?

**Beschreibung der Übung:**
Ich habe den Monitoring-Stack so umgebaut, dass gemeinsame Dienste zentral und host-spezifische Dienste getrennt definiert werden.

**Code / Umsetzung:**
```code
docker compose \
  -f services/common/compose.monitoring.yml \
  -f hosts/nuc/compose.yml \
  --env-file hosts/nuc/.env \
  config

docker compose \
  -f services/common/compose.monitoring.yml \
  -f hosts/rasberrypi/compose.yml \
  config
```
