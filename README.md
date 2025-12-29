# DevOps Utilities API

FastAPI-based internal API for operational utilities. Initial focus is system health metrics; additional utilities (AWS usage, log analysis, etc.) will be added incrementally.

## Overview
- Framework: FastAPI + Uvicorn
- Entry: [main.py](main.py)
- App: [app/api.py](app/api.py)
- Router: [routers/system_health.py](routers/system_health.py)
- Service: [services/metrics_service.py](services/metrics_service.py)

## Run Locally
1. Create and activate a virtual env (Windows):
	```powershell
	python -m venv .venv
	.venv\Scripts\activate
	```
2. Install dependencies:
	```powershell
	pip install -r requirements.txt
	```
3. Start the API:
	```powershell
	python main.py
	```
	- Server: http://127.0.0.1:8000
	- Docs: http://127.0.0.1:8000/docs
	- Redoc: http://127.0.0.1:8000/redoc

## Endpoints
- System Health: `GET /health`
  - Returns CPU, Memory, Disk usage percentages and an overall `system_status` derived from thresholds in [services/metrics_service.py](services/metrics_service.py).
  - Example response:
	 ```json
	 {
		"cpu_percentage": 34.2,
		"memory_percentage": 62.1,
		"disk_percentage": 45.8,
		"system_status": "Healthy"
	 }
	 ```

## Metrics Thresholds
Defined in [services/metrics_service.py](services/metrics_service.py):
- CPU: threshold 50, critical 85
- Memory: threshold 60, critical 85
- Disk: threshold 60, critical 85

Status mapping per metric:
- Healthy: usage < threshold
- Warning: threshold ≤ usage < critical
- Unhealthy: usage ≥ critical

## Notes
- The root route (`/`) currently shows a placeholder and is intentionally not documented here. It will be updated later.
