# 🗓️ Tag: 26.3.2026

## 🎯 Tagesziele
- Ziel 1: Monitoring-Stack betrieblich härten
- Ziel 2: Secrets, Retention und Healthchecks sauber nachziehen
- Ziel 3: Monitoring- und Detection-Dokumentation ergänzen

---

## ✅ Tagesresultate
Was habe ich heute konkret erreicht?

- Resultat 1: Secrets aus dem NUC-Compose in eine `.env`-Datei ausgelagert.
- Resultat 2: Einheitliche Docker-Loglimits für die Container gesetzt.
- Resultat 3: Loki, Grafana, Promtail und Atomic-Validator-Services mit Healthchecks ergänzt.
- Resultat 4: Prometheus und Node Exporter in den Stack aufgenommen.
- Resultat 5: Logrotate für dateibasierte Rohlogs des NUC ergänzt.
- Resultat 6: Runbook, Deployment- und Architektur-Doku aktualisiert.
- Resultat 7: Eine kleine Detection-Matrix für Atomic Validator und Wazuh ergänzt.

---

## ⚠️ Probleme & Reflexion
Welche Probleme sind aufgetreten und wie habe ich sie gelöst?

**Problem:**
Im Compose-Stack lagen mehrere Passwörter direkt im YAML.

**Lösung:**
Ich habe die Werte in `hosts/nuc/.env` ausgelagert und eine `.env.example` als Vorlage ergänzt.

**Reflexion:**
Secrets im Compose sind für Homelab zwar bequem, aber schlecht wartbar und unnötig sichtbar. Eine getrennte Env-Datei ist sauberer und lässt sich auch besser in CI verwenden.

---

**Problem:**
Die Loki-Retention war begrenzt, aber Rohlogs und Docker-Logs hatten keine einheitliche Begrenzung.

**Lösung:**
Ich habe Docker-Loglimits gesetzt und zusätzlich eine Logrotate-Konfiguration für Wazuh-, Suricata- und Syslog-Dateien ergänzt.

**Reflexion:**
Retention muss auf mehreren Ebenen gedacht werden. Nur Loki zu begrenzen reicht nicht, wenn die Rohlogs auf dem Host weiter wachsen.

---

**Problem:**
Der Stack war funktional, aber der Gesundheitszustand der Services war nur eingeschränkt sichtbar.

**Lösung:**
Für zentrale Dienste wurden Compose-Healthchecks ergänzt und das bestehende Healthcheck-Skript erweitert.

**Reflexion:**
Gerade in einem Homelab spart ein klarer Health-Status viel Zeit bei der Fehlersuche. Das ist einfacher als später ad hoc Logs zu durchsuchen.

---

## 📚 Eingesetzte Ressourcen
Welche Quellen habe ich benutzt?

- Projektinterne Compose-, Deploy- und Config-Dateien
- Docker-Compose Healthcheck-Mechanik
- Prometheus / Node Exporter Standard-Setup
- ChatGPT / KI Erklärung

**Kurz-Zusammenfassung der wichtigsten Erkenntnisse:**

- Ein stabiler Homelab-Stack braucht nicht nur Funktionen, sondern auch klare Betriebsgrenzen.
- Retention, Secrets und Healthchecks sind kleine Änderungen mit großem Nutzen.
- Kurze Runbooks und eine Detection-Matrix helfen später mehr als verstreute Einzelkommentare.

---

## 🧪 Eigene praktische Übung
Was habe ich selbst ausprobiert?

**Beschreibung der Übung:**
Ich habe den NUC-Stack so umgebaut, dass Secrets getrennt, Metriken zusätzlich erfasst und Logs kontrollierter rotiert werden.

**Code / Umsetzung:**
```code
cd /opt/defense-lab-soc/hosts/nuc
sudo docker compose --env-file .env config
sudo docker compose up -d --remove-orphans
bash scripts/healthcheck.sh
```
