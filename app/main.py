from pathlib import Path
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def fetch_page_text(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/135.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines = [line for line in lines if line]

    return "\n".join(cleaned_lines)


@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "job_url": "",
            "message": "채용공고 URL을 입력해보세요.",
            "preview": ""
        }
    )


@app.post("/analyze", response_class=HTMLResponse)
def analyze_job(request: Request, job_url: str = Form(...)):
    preview = ""

    try:
        text = fetch_page_text(job_url)
        preview = text[:3000]
        message = "페이지 읽기 성공"
    except Exception as e:
        message = f"에러 발생: {str(e)}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "job_url": job_url,
            "message": message,
            "preview": preview
        }
    )