from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from pathlib import Path
from routers import system_health, aws

app = FastAPI(
    title="Internal DevOps Utilities API",
    description="This is an Internal API Utitlities App for Monitoring metrics, AWS Usage, Log Analysis, etc",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

HERE = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc):
    if exc.status_code == 404:
        return RedirectResponse(url="/")
    raise exc


@app.get("/")
def home():
    return FileResponse(HERE / "static" / "index.html")


app.include_router(system_health.router)
app.include_router(aws.router, prefix="/aws")
