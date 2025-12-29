from fastapi import APIRouter, HTTPException
from services.metrics_service import get_system_metrics

router = APIRouter()

@router.get("/health", status_code=200)
def get_system_health():
    """
        This API gets the System Metrics (CPU%, Memory%, Disk%, System Health)
        \nBased on below configurable thresholds:\n
        CPU Usage Threshold = 60
        CPU Usage Critical Threshold = 85
        
        Memory Usage Threshold = 65
        Memory Usage Critical Threshold = 85
        
        Disk Usage Threshold = 65
        Disk Usage Critical Threshold = 85
    """
    try:
        metrics = get_system_metrics()
        return metrics
    except:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
            )