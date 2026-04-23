# SmartGallery Fork Installation Guide

This guide covers installation and updates for this fork of Smart ComfyUI Gallery.

Fork context:

- fork repository: `https://github.com/max-dingsda/smart-comfyui-gallery`
- current fork release: `1.0.0-fork.1`
- upstream baseline: `2.11`
- upstream reference: `https://github.com/biagiomaf/smart-comfyui-gallery`

SmartGallery works fully offline and does not require ComfyUI to be running.

## Requirements

- Python 3.9+
- ffmpeg / ffprobe recommended for video workflow extraction
- Windows, Linux, or macOS

## Install With Python

### Windows

```bat
git clone https://github.com/max-dingsda/smart-comfyui-gallery
cd smart-comfyui-gallery
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `run_smartgallery.bat` in the project folder:

```bat
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat

set "BASE_OUTPUT_PATH=C:/Path/To/ComfyUI/output"
set "BASE_INPUT_PATH=C:/Path/To/ComfyUI/input"
set "BASE_SMARTGALLERY_PATH=C:/Path/To/ComfyUI/output"
set "FFPROBE_MANUAL_PATH=C:/Path/To/ffmpeg/bin/ffprobe.exe"
set SERVER_PORT=8189

python smartgallery.py
pause
```

Use forward slashes in paths, even on Windows.

### macOS / Linux

```bash
git clone https://github.com/max-dingsda/smart-comfyui-gallery
cd smart-comfyui-gallery
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `run_smartgallery.sh` in the project folder:

```bash
#!/bin/bash
source venv/bin/activate

export BASE_OUTPUT_PATH="$HOME/ComfyUI/output"
export BASE_INPUT_PATH="$HOME/ComfyUI/input"
export BASE_SMARTGALLERY_PATH="$HOME/ComfyUI/output"
export FFPROBE_MANUAL_PATH="/usr/bin/ffprobe"
export SERVER_PORT=8189

python smartgallery.py
```

Make it executable and run it:

```bash
chmod +x run_smartgallery.sh
./run_smartgallery.sh
```

## Start The App

Default URL:

```text
http://127.0.0.1:8189/galleryout/
```

On startup, the app scans the configured output path and updates the SQLite cache.

## Update This Fork

If installed with Git:

```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, use:

```bat
git pull
venv\Scripts\activate
pip install -r requirements.txt
```

If you downloaded a ZIP instead of cloning with Git, download the current fork source again and move your local run script into the new folder.

Do not use upstream `biagiomaf/smart-comfyui-gallery` releases as direct updates for this fork. Upstream `2.11` is the baseline, not this fork's release line.

## Docker

Docker support is still based on the inherited SmartGallery Docker setup.

For local fork builds:

```bash
docker build -t smartgallery:latest .
```

Then use `compose.yaml` or the Makefile and point the volume mounts to your local ComfyUI folders.

Full Docker details:

- [DOCKER_HELP.md](DOCKER_HELP.md)

Important Docker note:

- public DockerHub images such as `mmartial/smart-comfyui-gallery` represent the upstream Docker distribution unless this fork publishes its own image
- to run fork-specific code, build the Docker image from this repository

## FFmpeg / FFprobe

FFmpeg is recommended to extract workflows from video files.

Common `ffprobe` locations:

- Windows: `C:/ffmpeg/bin/ffprobe.exe`
- Linux: `/usr/bin/ffprobe`
- macOS: `/opt/homebrew/bin/ffprobe`

Download:

- `https://ffmpeg.org/`

## Reverse Proxy

Point your proxy to:

```text
http://127.0.0.1:8189/galleryout/
```

Example Nginx location:

```nginx
location /gallery/ {
    proxy_pass http://127.0.0.1:8189/galleryout/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

## Troubleshooting

- Check folder permissions.
- Verify the Python version.
- Ensure the `ffprobe` path is correct.
- Check whether port `8189` is already in use.
- Restart the app after changing environment variables.

If problems persist, open an issue with logs from the startup console.
