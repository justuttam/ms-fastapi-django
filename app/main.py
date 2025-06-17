import aiofiles
import io
import pathlib
import uuid

from functools import lru_cache
from fastapi import FastAPI, Depends, File, HTTPException, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import pytesseract as ptsr

from .settings import Settings

@lru_cache
def get_settings():
    return Settings()

DEBUG = get_settings().debug

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"

# FastAPI app
app = FastAPI()

# templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
def home_view(request: Request, settings:Settings=Depends(get_settings)):
    return templates.TemplateResponse(request=request, name="home.html", context={"request": request, "abc": 123})


@app.post("/")
async def prediction_view(file: UploadFile, settings:Settings=Depends(get_settings)):
    bytes_stream = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_stream)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    predictions = ptsr.image_to_string(img)
    return {"result": predictions}


# @app.post("/")
# def home_detail_view():
#     return {"name": "hello world!"}


@app.post("/img-echo/", response_class=FileResponse)
async def img_echo_view(file: UploadFile, settings:Settings=Depends(get_settings)):
    if not settings.echo_active:
        raise HTTPException(detail="Invalid endpoint", status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    bytes_stream = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_stream)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    fext = pathlib.Path(file.filename).suffix.lower()  # .jpg, .txt

    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)

    return dest
