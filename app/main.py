import base64
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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
def upload_file(file_data: FileData):
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
