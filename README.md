# Augmented Reality & 3D Gaussian Splatting im Web

Interaktive Quarto-Webseite zu **Thema 8 — Augmented Reality + Gaussian Splatting im Web**
(Modul Visual Computing). Sie führt vom theoretischen Hintergrund von 3D Gaussian Splatting
(3DGS) über die Capture-/Trainings-Pipeline bis zur interaktiven Darstellung im Browser:
ein Orbit-Viewer, eine begehbare Szene und eine WebXR-AR-Demo.

- **Live-Seite:** via GitHub Pages (Branch `gh-pages`, automatisch deployt — siehe
  [Veröffentlichen](#veröffentlichen)).
- **Technik:** [Quarto](https://quarto.org/) + [Babylon.js](https://www.babylonjs.com/)
  (WebGL/WebGPU, nativer Gaussian-Splatting-Support), WebXR für AR.

---

## Projektstruktur

| Seite / Datei | Owner | Inhalt |
|---|---|---|
| `index.qmd` | C | Startseite, Überblick, Team |
| `theorie/index.qmd` | A | Geschichte (NeRF→3DGS), Repräsentation, Rendering, Vergleich |
| `pipeline/index.qmd` | B | Use-Cases, Aufnahme, COLMAP, LichtFeld-Training, Export |
| `web-ar/index.qmd` | C | Babylon.js, WebXR, Orbit-Viewer, AR-Demo, Begehung („X") |
| `quiz/index.qmd` | C | Lernzielabfrage |
| `credits/index.qmd` | alle | Wer hat was gemacht |

Zentrale Dateien:

- **`_quarto.yml`** — Projektkonfiguration: Navbar, Theme (`cosmo`), `freeze: auto`,
  Render-Globs.
- **`references.bib`** — Literaturverweise (Quarto-Zitate).
- **`styles.css`** — projektweite CSS-Ergänzungen.
- **`.github/workflows/publish.yml`** — CI: rendert & deployt nach gh-pages.

> Wer macht was: **A** = Theorie & Methodik, **B** = Capture & Pipeline (eigenes 3DGS-Modell),
> **C** = Web & AR Integration.

---

## Lokal bauen & Vorschau

Voraussetzungen: [Quarto](https://quarto.org/docs/get-started/) und Python (für die
Jupyter-/Berechnungs-Zellen). Das `venv/` im Repo ist git-ignoriert; bei Bedarf neu anlegen.

```bash
# Live-Vorschau mit Auto-Reload (öffnet den Browser)
quarto preview

# Einmalig komplett rendern -> Ausgabe in _site/
quarto render

# Nur eine Seite rendern (schneller beim Iterieren)
quarto render web-ar/index.qmd
```

`freeze: auto` cached berechnete Zellen, damit unveränderte Inhalte nicht jedes Mal neu
ausgeführt werden. `_site/` ist der Build-Output und git-ignoriert — **nicht** committen.

---

## Veröffentlichen

Ein **Push auf `main`** löst `.github/workflows/publish.yml` aus: Quarto rendert die Seite und
publisht sie auf den Branch `gh-pages`, von dem GitHub Pages ausliefert. Es ist **kein**
manueller Schritt nötig.

> **Wichtig für AR:** WebXR (`immersive-ar`) braucht einen sicheren Kontext (HTTPS). Die
> GitHub-Pages-URL erfüllt das; ein lokaler `http://`-Preview kann AR nicht starten.

---

## Interaktive Bausteine (Seite „Web & AR")

Alles in `web-ar/index.qmd`. Babylon.js wird per CDN geladen (zwei `<script src=…>` ganz oben
im ersten `=html`-Block); beide Viewer teilen sich diese eine Babylon-Instanz.

1. **Orbit-Viewer** (`initSplatViewer`, Canvas `renderCanvas`) — freie Maus-/Touch-Steuerung
   um das Modell (`ArcRotateCamera`), Modellauswahl per Dropdown.
2. **AR-Demo** (`initXR`) — startet eine `immersive-ar`-Session mit Hit-Test & Platzierung.
   Läuft zuverlässig nur auf **Android-Chrome**; auf Desktop/iOS degradiert sie sauber
   (Hinweistext + QR-Code), die übrigen Viewer funktionieren überall.
3. **Begehung / „X"** (`initWalkViewer`, Canvas `walkCanvas`) — Ich-Perspektive an festen
   Standpunkten: **Ziehen** = umsehen, **Klick** = zum nächsten Standpunkt (sanft animiert).
   Funktioniert ohne AR-Hardware und ist die Demo für die Präsentation am Laptop.

---

## ★ Eigenes Modell einbinden — Anleitung für Person B

Aktuell laufen öffentliche Beispiel-Splats. So ersetzt du sie durch dein eigenes Modell.

### 1. Exportieren

Aus LichtFeld Studio / SuperSplat als **`.spz`** exportieren (komprimiertes Web-Format,
deutlich kleiner als `.ply`/`.splat`). Details siehe Pipeline-Seite (`pipeline/index.qmd`).
`.ply` als Master behalten, `.spz` ist die Web-Auslieferung.

### 2. Datei ablegen

Lege die Datei **neben** `web-ar/index.qmd`, z. B. `web-ar/scene.spz`. Dateien in diesem
Ordner kopiert Quarto automatisch mit in den Build (genau wie `web-ar/qr-ar-demo.svg`); sie
ist dann **relativ** über ihren Dateinamen erreichbar.

> **Dateigröße beachten:** `.spz`-Modelle sind oft 10–50 MB. Git ignoriert sie **nicht**
> automatisch. Bis ~50 MB ist ein direkter Commit ok; bei größeren Dateien
> [Git LFS](https://git-lfs.com/) nutzen oder das Modell extern hosten und die volle URL
> verwenden. Lade-Geschwindigkeit = Dateigröße → so klein wie möglich exportieren.

### 3. URL in den Viewern setzen

**Begehung** (`web-ar/index.qmd`, im `initWalkViewer`-Script): die Zeile mit dem Beispiel-Splat
ändern —

```js
// vorher:
const url = "https://assets.babylonjs.com/splats/gs_Skull.splat";
// nachher (Datei liegt in web-ar/):
const url = "scene.spz";
```

**Orbit-Viewer** (`initSplatViewer`-Script): im `<select id="splat-select">` eine eigene Option
ergänzen oder die Beispiele ersetzen —

```html
<option value="scene.spz">Unser Modell</option>
```

### 4. Prüfen

`quarto preview` starten, Seite „Web & AR" öffnen: Das Modell muss in beiden Viewern erscheinen.
Lädt nichts, steht der Fehler unten links im jeweiligen Canvas (Statuszeile).

---

## ★ Standpunkte der Begehung setzen — Anleitung für Person B

Die Begehung zeigt das Modell aus vier festen **Standpunkten**, durch die ein Klick reihum
schaltet. Die Standpunkte stehen in einem **auf die Szene ausgerichteten Koordinatensystem**,
damit man sie intuitiv setzen kann.

### Das mentale Modell

- **`FACE_TARGET`** — der Punkt, den die Kamera **immer anschaut** (das Zentrum deines Motivs,
  z. B. ein Gesicht oder die Raummitte).
- **`FACE_VIEW`** — **ein** guter Standpunkt, von dem aus man frontal auf das Motiv blickt.
- **`wp(x, y, z)`** — rechnet Szenen-Koordinaten in Weltkoordinaten um:
  - **`z`** = Tiefe (Richtung Motiv): `wp(0, 0, 1)` ist **genau** `FACE_VIEW`; `z<1` näher dran,
    `z>1` weiter weg.
  - **`x`** = seitlich (links/rechts), **`y`** = hoch/runter — jeweils senkrecht zur
    Blickrichtung.

Das System ist nur **gedreht und gleichmäßig skaliert** auf deine Szene — deshalb „normalisiert".
Du musst also nur `FACE_TARGET` und `FACE_VIEW` einmal richtig setzen; danach sind alle vier
Standpunkte bequem über `wp(...)` ausdrückbar.

### Schritt 1 — Zentrum (`FACE_TARGET`) finden

Modell laden (Schritt oben), Seite öffnen, Browser-Konsole (F12) öffnen und einfügen:

```js
// Mittelpunkt des geladenen Splat-Modells (Welt-Koordinaten)
const scene = BABYLON.EngineStore.Instances
  .flatMap(e => e.scenes)
  .find(s => s.meshes.some(m => m.getClassName?.().includes("GaussianSplatting")));
const m = scene.meshes.find(m => m.getClassName?.().includes("GaussianSplatting"));
m.computeWorldMatrix(true);
console.log("FACE_TARGET ≈", m.getBoundingInfo().boundingBox.centerWorld);
```

Den ausgegebenen Punkt als `FACE_TARGET` eintragen (oft nahe `(0, …, 0)`).

### Schritt 2 — guten Blickwinkel (`FACE_VIEW`) finden

Der **Orbit-Viewer** lässt sich frei mit der Maus drehen/zoomen — ideal, um einen schönen
Frontal-Winkel zu suchen. Stell den gewünschten Blick ein und lies dann in der Konsole die
Kamera-Position aus:

```js
// Aktuelle Position/Ziel der Orbit-Kamera = guter Standpunkt
const orbit = BABYLON.EngineStore.Instances
  .flatMap(e => e.scenes)
  .map(s => s.activeCamera)
  .find(c => c && c.getClassName() === "ArcRotateCamera");
console.log("FACE_VIEW   =", orbit.position);   // -> als FACE_VIEW eintragen
console.log("FACE_TARGET =", orbit.target);     // -> bestätigt das Zentrum
```

Die ausgegebene `position` als `FACE_VIEW` setzen, `target` als `FACE_TARGET`. Beide stehen
oben im `initWalkViewer`-Script:

```js
const FACE_TARGET = new BABYLON.Vector3(0, 0.1, 0);    // <- Zentrum aus Schritt 1
const FACE_VIEW   = new BABYLON.Vector3(-2.0, 0.0, 1.5); // <- Blickwinkel aus Schritt 2
```

### Schritt 3 — die vier Standpunkte

Jetzt nur noch das `WAYPOINTS`-Array mit `wp(x, y, z)` füllen. Beispiel:

```js
const WAYPOINTS = [
  { pos: wp( 0.0, 0.0, 1.0), target: FACE_TARGET }, // frontal (= FACE_VIEW)
  { pos: wp( 0.8, 0.0, 1.0), target: FACE_TARGET }, // seitlich versetzt
  { pos: wp( 0.0, 0.5, 1.0), target: FACE_TARGET }, // etwas von oben
  { pos: wp( 0.0, 0.0, 1.6), target: FACE_TARGET }, // weiter weg
];
```

Faustregeln:

- **Abstand** über `z`: `z` zwischen ~1 und ~2 sind meist gute Werte; `target` bleibt immer
  `FACE_TARGET`, die Kamera dreht sich automatisch zum Motiv.
- **Augenhöhe** über `y`: ein kleines positives `y` hebt den Blick leicht an (natürlicher als
  exakt waagerecht).
- **Seite** über `x`: das Vorzeichen kippt nach links/rechts — bei „falscher" Seite einfach
  das Vorzeichen tauschen.
- Mehr oder weniger als vier Standpunkte? Einfach Einträge hinzufügen/entfernen — der Zähler
  („Standpunkt i / N") passt sich automatisch an.

Nach jeder Änderung `quarto preview` neu laden und durchklicken.

---

## Bekannte Grenzen & Wartungs-Hinweise

- **AR nur auf Android-Chrome.** Desktop/iOS unterstützen `immersive-ar` nicht — dort
  degradiert die Demo bewusst (Hinweis + QR). Das ist erwartetes Verhalten, kein Bug.
- **Animations-`loopMode` muss `ANIMATIONLOOPMODE_CONSTANT` sein.** Beim Standpunkt-Wechsel
  (`CreateAndStartAnimation` in `goToWaypoint`) sorgt das dafür, dass die Bewegung **einmal**
  läuft und am Ziel hält. `ANIMATIONLOOPMODE_RELATIVE` (Wert `0`) würde endlos loopen und die
  Position akkumulieren — nicht zurückdrehen.
- **Eigene Tap-Erkennung statt `POINTERTAP`.** Der Klick-zum-Standpunkt nutzt bewusst
  pointerdown/up mit Bewegungs-/Zeitschwelle (statt Babylons `POINTERTAP`), weil dessen
  Doppelklick-Verzögerung Klicks verschluckt hat. So bleiben Klick (Wechsel) und Ziehen
  (Umsehen) sauber getrennt.

---

## Team & Credits

Aufgabenverteilung siehe `credits/index.qmd`. Repo:
[VC8-AR-Gaussian-Splatting-in-web/website](https://github.com/VC8-AR-Gaussian-Splatting-in-web/website).
