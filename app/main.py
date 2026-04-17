from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"job_url": "", "message": "채용공고 URL을 입력해보세요."}
    )
    
@app.post("/analyze", response_class=HTMLResponse)
def analyze_job(request: Request, job_url: str = Form(...)):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "job_url": job_url,
            "message": f"입력한 URL: {job_url}"
        }
    )