# Strukturierung in gemeinsame und host-spezifische Services

## Ziel

Mit dem Ausbau des Homelabs auf mehrere Geräte wurde klar, dass nicht mehr alle Dienste direkt in den einzelnen Host-Compose-Dateien gepflegt werden sollten.

Vor allem für Monitoring-Agenten war die bisherige Struktur nachteilig:

- gleiche Definitionen an mehreren Orten
- höheres Risiko für Konfigurationsdrift
- unnötig aufwendige Änderungen bei jedem zusätzlichen Host

Deshalb wurde die Struktur erweitert.

---

## Neue Aufteilung

Es gibt jetzt zwei Ebenen:

### 1. Gemeinsame Services

Pfad:

```text
services/common
```

Hier liegen Dienste, die auf mehreren Geräten gleich oder fast gleich eingesetzt werden.

Aktuell:

- `promtail`
- `node-exporter`

### 2. Host-spezifische Services

Pfad:

```text
hosts/<host>
```

Hier bleiben:

- Ports
- lokale Volumes
- Hostnamen
- host-spezifische Dienste wie:
  - `grafana`
  - `loki`
  - `prometheus`
  - `wazuh`
  - `suricata`
  - `pihole`

---

## Warum diese Änderung gemacht wurde

### Weniger Duplikation

Die Definition von `promtail` war nicht mehr nur ein Einzelfall. Sobald mehrere Geräte angebunden werden, entsteht unnötige Wiederholung.

**Warum geändert:**

- Änderungen an gemeinsamen Agenten müssen nur noch einmal gemacht werden
- die Gefahr von leicht unterschiedlichen Konfigurationen sinkt

### Bessere Skalierbarkeit

Der Raspberry Pi soll ebenfalls überwacht werden. Später könnten noch weitere Geräte dazukommen.

**Warum geändert:**

- neue Hosts lassen sich leichter integrieren
- gemeinsame Basisdienste sind sofort wiederverwendbar

### Klarere Verantwortung pro Datei

Vorher war die Host-Datei gleichzeitig Basisdefinition und Host-Spezialfall.

**Warum geändert:**

- `services/common` beschreibt den Standard
- `hosts/<host>` beschreibt nur die lokalen Besonderheiten

Diese Trennung macht das Repository verständlicher.

---

## Technische Umsetzung

Neu eingeführt:

```text
services/common/compose.monitoring.yml
```

Die Deploy-Skripte verwenden jetzt Compose mit mehreren Dateien:

```bash
docker compose \
  -f services/common/compose.monitoring.yml \
  -f hosts/nuc/compose.yml \
  up -d
```

beziehungsweise für den Raspberry Pi:

```bash
docker compose \
  -f services/common/compose.monitoring.yml \
  -f hosts/rasberrypi/compose.yml \
  up -d
```

Dadurch wird zuerst die gemeinsame Basis geladen und danach mit den Host-Definitionen ergänzt.

---

## Ergebnis

Die neue Struktur bringt vor allem organisatorischen und betrieblichen Nutzen:

- weniger doppelte Konfiguration
- einfachere Erweiterung auf weitere Hosts
- kleinere und verständlichere Host-Dateien
- konsistentere Deployments

Für das Homelab ist das ein sinnvoller Zwischenschritt: nicht zu abstrakt, aber deutlich sauberer als vorher.
