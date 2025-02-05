from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files (for CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/subgen")
def read_root(request: Request):
    return templates.TemplateResponse("subgen.html", {"request": request})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Receives an uploaded video or audio file and extracts data."""
    file_data = await file.read()  # Read the file into memory
    file_info = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(file_data),  # Size in bytes
        "data": file_data,
    }

    # Process file_data if needed (e.g., extract metadata, waveform, etc.)
    return {"message": "File received", "file_info": file_info}
