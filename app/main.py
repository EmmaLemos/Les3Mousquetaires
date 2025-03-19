import os
import uuid
import base64
import shutil
import subprocess
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response, FileResponse
from fastapi import FastAPI, Request, UploadFile, File, HTTPException


app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files (for CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.middleware("http")
async def add_security_headers(request, call_next):
    response: Response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/subgen")
def read_root(request: Request):
    return templates.TemplateResponse("subgen.html", {"request": request})


class FileData(BaseModel):
    translate: bool
    data: str  # On attend une chaîne Base64


@app.post("/upload")
async def upload_file(file_data: FileData):
    """Reçoit un fichier encodé en Base64 et affiche ses infos."""
    # Décoder la base64 en bytes
    file_bytes = base64.b64decode(file_data.data)

    file_info = {
        "size": len(file_bytes),  # Taille du fichier en octets
    }

    print(f"Fichier reçu: {file_info}")

    with open("app/example/input.srt", "r") as f:
        subtitles = f.read()

    return {"subtitles": subtitles}


@app.post("/embed_subtitles")
async def embed_subtitles(
    video: UploadFile = File(...), subtitles: UploadFile = File(...)
):
    # Generate unique filenames
    video_input_path = f"/tmp/{uuid.uuid4()}_{video.filename}"
    subtitles_input_path = f"/tmp/{uuid.uuid4()}_{subtitles.filename}"
    output_path = f"/tmp/{uuid.uuid4()}_output.mp4"

    # Save uploaded files temporarily
    with open(video_input_path, "wb") as video_file:
        shutil.copyfileobj(video.file, video_file)

    with open(subtitles_input_path, "wb") as subtitles_file:
        shutil.copyfileobj(subtitles.file, subtitles_file)

    # FFmpeg command to embed subtitles permanently
    command = [
        "ffmpeg",
        "-i",
        video_input_path,
        "-vf",
        f"subtitles={subtitles_input_path}",
        "-preset",
        "ultrafast",
        "-crf",
        "28",
        output_path,
    ]

    # Execute FFmpeg command
    result = subprocess.run(command, capture_output=True)

    # Check if FFmpeg succeeded
    if result.returncode != 0:
        # Cleanup temporary files
        os.unlink(video_input_path)
        os.unlink(subtitles_input_path)
        raise HTTPException(
            status_code=500, detail=f"FFmpeg Error: {result.stderr.decode()}"
        )

    # Return processed video and clean up temp files afterwards
    response = FileResponse(
        output_path, media_type="video/mp4", filename="video_with_subtitles.mp4"
    )

    # Clean up files after sending response
    @response.call_on_close
    def cleanup_files():
        for path in [video_input_path, subtitles_input_path, output_path]:
            if os.path.exists(path):
                os.unlink(path)

    return response
