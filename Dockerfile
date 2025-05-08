# Basis-Image
FROM python:3.11-slim

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY . .

# Bot starten
CMD ["python", "bot.py"]
