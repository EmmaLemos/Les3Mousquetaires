import base64
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, UploadFile, File, HTTPException


app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files (for CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/subgen")
def read_root(request: Request):
    return templates.TemplateResponse("subgen.html", {"request": request})


class FileData(BaseModel):
    filename: str
    content_type: str
    data: str  # On attend une chaîne Base64


@app.post("/upload")
def upload_file(file_data: FileData):
    """Reçoit un fichier encodé en Base64 et affiche ses infos."""

    # Décoder la base64 en bytes
    file_bytes = base64.b64decode(file_data.data)

    file_info = {
        "filename": file_data.filename,
        "content_type": file_data.content_type,
        "size": len(file_bytes),  # Taille du fichier en octets
    }

    print(f"Fichier reçu: {file_info}")  # Debug

    return {"message": "Fichier reçu", "file_info": file_info}
