# 📅 Woche: [Datum von – bis]

## 🎯 Wochenziele
- Ziel 1: Git server


---

# 🗓️ Tag: 6.3.2026

## 🎯 Tagesziele
- Ziel 1: Git server aufsetzen


---

## ✅ Tagesresultate
Was habe ich heute konkret erreicht?

Ich habe es geschafft den Gitserver aufzusetzen mit einer sicheren https verbindung.
---

## ⚠️ Probleme & Reflexion
Welche Probleme sind aufgetreten und wie habe ich sie gelöst?

**Problem:**
Anfangs habe ich ein selfsigned zertifikat genommen und dann konnte ich nicht klonen.

**Lösung:**
Ich habe schlussendlich mit lets encrypt ein zertifikat geholt.

**Reflexion:**
Ich habe gelernt wie ich einen gitserver aufsetze
---

## 📚 Eingesetzte Ressourcen
Welche Quellen habe ich benutzt?


- ChatGPT / KI Erklärung

---


**Code / Umsetzung:**
```code
services:
  gitea:
    image: docker.gitea.com/gitea:latest
    container_name: gitea
    restart: always
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__server__ROOT_URL=https://192.168.188.50:3000/
      - GITEA__server__DOMAIN=192.168.188.50
      - GITEA__server__SSH_DOMAIN=192.168.188.50
      - GITEA__server__START_SSH_SERVER=false
      - GITEA__database__DB_TYPE=sqlite3
    ports:
      - "3000:3000"
      - "3080:3080"
      - "2222:22"
    volumes:
      - ./data:/data
      - /etc/letsencrypt:/etc/letsencrypt
    networks:
      - gitea

networks:
  gitea:
    driver: bridge