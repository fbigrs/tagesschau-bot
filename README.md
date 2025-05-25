# Tagesschau Eilmeldungs-Bot für Discord

Dieser Bot postet automatisch neue **Eilmeldungen** von tagesschau.de in einen von dir gewählten Discord-Channel – schön formatiert mit Embed, Bild und Link.

## ✅ Features
- Holt regelmäßig Eilmeldungen von der Tagesschau API
- Postet sie als Embed in Discord
- Erkennt doppelte Nachrichten automatisch
- Nutzt `.env` für sichere Einstellungen
- Logging über Konsole
- Optional: Erwähnt eine bestimmte Rolle bei neuen Eilmeldungen

## 🔧 Einrichtung

1. Python 3.9+ installieren
2. Repository klonen oder Dateien speichern
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
4. `.env` Datei anlegen:
   ```env
   DISCORD_BOT_TOKEN=dein-token
   DISCORD_CHANNEL_ID=deine-channel-id
   DISCORD_ROLE_ID=deine-role-id  # Optional: Rolle die bei Eilmeldungen erwähnt wird
   ```
   > **Hinweis zur Role ID**: Aktiviere den "Entwicklermodus" in Discord (Einstellungen > App-Einstellungen > Erweitert), dann kannst du per Rechtsklick auf eine Rolle die ID kopieren.
5. Starte den Bot:
   ```bash
   python bot.py
   ```

## 📂 Dateien
- `bot.py`: Der Hauptbot
- `.env`: Enthält vertrauliche Konfigurationen
- `last_ids.json`: Speichert bereits gesendete Meldungen
- `requirements.txt`: Python-Abhängigkeiten

## 🛠 Hinweise
- Die API wird alle 60 Sekunden abgefragt
- Nachrichten werden **nur gepostet**, wenn sie das Tag `"Eilmeldung"` enthalten
- Stelle sicher, dass der Bot die Berechtigung hat, Rollen zu erwähnen
- Die zu erwähnende Rolle muss als "erwähnbar" konfiguriert sein
