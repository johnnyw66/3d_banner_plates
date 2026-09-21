## 3D Text Banner Generator Service

A containerised parametric 3D CAD service powered by **FastAPI**, **`build123d`**, and **Three.js**. It generates watertight, 3D-printable binary STL plates with solid or outlined text directly from TrueType (`.ttf`) and OpenType (`.otf`) fonts.

---

### Project Structure

Ensure your directory structure looks like this before building:

```text
banner_service/
├── Dockerfile
├── requirements.txt
├── app.py
├── fonts/
│   └── Roboto-Bold.ttf      # At least one default font
└── templates/
    └── index.html           # Three.js 3D WebGL UI

```

### Prerequisites

Docker Desktop (macOS, Linux, or Windows)

(Optional) Any .ttf or .otf font files placed in the fonts/ directory.

## Build & Run

### 1. Build the Docker Image
From the root of your banner_service directory:

Bash
```
docker build -t text-banner-service .
```


### 2. Run the Container
Standard Run:

Bash
```
docker run -d \
  --name banner-gen \
  -p 8000:8000 \
  text-banner-service
```


## Recommended (with persistent host font directory):

Mount your local fonts/ folder so any new fonts dropped onto your machine are instantly available inside the app without rebuilding the image:

Bash
```
docker run -d \
  --name banner-gen \
  -p 8000:8000 \
  -v "$(pwd)/fonts:/app/fonts" \
  text-banner-service
```

Usage
Open your browser and navigate to:

```
http://localhost:8000
```

Configure Parameters:

++ Banner Text: The string to engrave or raise.

++ Style: Choose Solid (filled characters) or Outline (hollow perimeter stroke).

++ Font: Select a pre-installed font from the dropdown, or upload your own .ttf / .otf file.

++ Dimensions (mm): Adjust font size, text relief height, baseplate thickness, margins (padding), and corner radiuses.


Interactive 3D Preview:


+ Click Update 3D Preview to trigger CSG compilation.
+ Left Click + Drag: Rotate around the plate.
+ Right Click + Drag / Scroll: Pan and zoom.
+ Check the top-right HUD for exact physical dimensions ($X \times Y \times Z\text{ in mm}$) and triangle count.

Export: Click Download STL to save the binary file.

Headless API Usage (curl)
You can also automate batch generations programmatically without the web interface:

Bash

```
curl -X POST "http://localhost:8000/generate" \
  -F "text=DRAWER-01" \
  -F "style=solid" \
  -F "selected_font=Roboto-Bold.ttf" \
  -F "font_size=20.0" \
  -F "text_relief=1.6" \
  -F "plate_thickness=2.4" \
  -F "padding_x=8.0" \
  -F "padding_y=6.0" \
  -F "corner_radius=3.0" \
  -o "drawer_01.stl"
```


## Container Management

### View live server logs:
```
docker logs -f banner-gen
```
### Stop Container

```
docker stop banner-gen
```

### Restart container:

```
docker start banner-gen
```

### Rebuild after making code changes:
```
docker stop banner-gen && docker rm banner-gen
docker build --no-cache -t text-banner-service .
docker run -d -p 8000:8000 --name banner-gen -v "$(pwd)/fonts:/app/fonts" text-banner-service
```
