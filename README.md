# Graphdatenvisualisierung
Sara, Silvia, Adam

## 🚀 Schnellanleitung - Website zum Laufen bringen

### Voraussetzungen

Bevor du startest, stelle sicher, dass **Quarto** installiert ist:

- **Quarto** – zum Rendern der Website (Download: [quarto.org](https://quarto.org/docs/get-started/))

### Schritt 1: Repository klonen

```bash
git clone ...
cd graphdatenvisualisierung
```

### Schritt 2: Website lokal anschauen

Mit folgendem Befehl kannst du die Website live mit Auto-Reload starten:

```bash
quarto preview
```

Dies öffnet automatisch deine Website im Browser unter `http://localhost` und aktualisiert die Seite bei jeder Änderung an den Dateien.

### Schritt 3: Website rendern

Um die Website zu kompilieren und den Output-Ordner zu generieren:

```bash
quarto render
```

Die fertige Website befindet sich dann im Ordner `_site/` oder `docs/` (abhängig der Konfiguration in `_quarto.yml`).

## 📋 Wichtige Quarto-Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `quarto preview` | Website lokal mit Live-Reload öffnen |
| `quarto render` | Website rendern und kompilieren |
| `quarto render --to html` | Nur HTML-Format rendern |
| `quarto render --to pdf` | In PDF konvertieren (falls konfiguriert) |
| `quarto update` | Quarto auf die neueste Version aktualisieren |

## 🛠️ Typischer Workflow

1. **Entwickeln:** Starte `quarto preview` und bearbeite deine `.qmd`-Dateien
2. **Testen:** Deine Änderungen erscheinen automatisch im Browser
3. **Deployen:** Führe `quarto render` aus, um die finale Version zu erstellen

## 📁 Projektstruktur

- `_quarto.yml` – Konfigurationsdatei für das Quarto-Projekt
- `*.qmd` – Quarto Markdown-Dateien (enthält Text, Code und Visualisierungen)
- `_site/` oder `docs/` – Generierte Website (nach `quarto render`)

## ❓ Troubleshooting

**Quarto ist nicht installiert?**
```bash
# Quarto installieren (je nach OS)
# Unter Windows: https://quarto.org/docs/get-started/
# Unter macOS: brew install quarto
# Unter Linux: https://quarto.org/docs/get-started/
```

**Port bereits in Verwendung?**
```bash
quarto preview --port 3000
```

**Cache-Probleme?**
```bash
rm -r .quarto
quarto render
```

---
