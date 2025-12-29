from fastapi import FastAPI
from routers import system_health, aws

app = FastAPI(
    title="Internal DevOps Utilities API",
    description="This is an Internal API Utitlities App for Monitoring metrics, AWS Usage, Log Analysis, etc",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def hello():
    """
    This is hello api
    """
    return {
        "message": "Hello world!"
    }


app.include_router(system_health.router)
app.include_router(aws.router, prefix="/aws")
#TODO: cost analysis
#TODO: bucket analysis