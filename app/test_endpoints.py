import shutil
import io
from fastapi.testclient import TestClient
from app.main import app, BASE_DIR, UPLOAD_DIR

from PIL import Image, ImageChops

client = TestClient(app)


def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']


# def test_post_home():
#     response = client.post("/")
#     assert response.status_code == 200
#     assert "application/json" in response.headers['content-type']
#     assert response.json() == {"name": "hello world!"}


def test_echo_upload():
    for path in (BASE_DIR / "images").glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None

        response = client.post("/img-echo/", files={"file": open(path, 'rb')})
        if img is None:
            assert response.status_code == 400
        else:
            assert response.status_code == 200
            r_strem = io.BytesIO(response.content)
            echo_img = Image.open(r_strem)
            assert ImageChops.difference(echo_img, img).getbbox() is None

    shutil.rmtree(UPLOAD_DIR)


def test_prediction_upload():
    for path in (BASE_DIR / "images").glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None

        response = client.post("/", files={"file": open(path, 'rb')})
        if img is None:
            assert response.status_code == 400
        else:
            assert response.status_code == 200
            data = response.json()
            assert len(data.keys()) == 1
