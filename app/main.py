import pathlib

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent

# FastAPI app
app = FastAPI()

# templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
def home_view(request: Request):
    print(dir(request))
    return templates.TemplateResponse(request=request, name="home.html", context={"request": request, "abc": 123})

@app.post("/")
def home_detail_view():
    return {"name": "hello world!"}
