# DevOps Utilities API

FastAPI-based internal API for operational utilities. Initial focus is system health metrics; additional utilities (AWS usage, log analysis, etc.) will be added incrementally.
This project exposes two main utility areas below: **System Health** and **AWS Utilities**. 

## Overview
- Framework: FastAPI + Uvicorn
- Entry: [main.py](main.py)
- App: [app/api.py](app/api.py)
- Router: [routers/system_health.py](routers/system_health.py)
- Service: [services/metrics_service.py](services/metrics_service.py)

## Run Locally
1. Fork and clone the github repository
	```powershell
	git clone <repo-url>
	```
2. Create and activate a virtual env (Windows):
	```powershell
	python -m venv .venv
	.venv\Scripts\activate
	```
3. Install dependencies:
	```powershell
	pip install -r requirements.txt
	```
4. Start the API:
	```powershell
	python main.py
	```
	- Server: http://127.0.0.1:8000
	- Docs: http://127.0.0.1:8000/docs
	- Redoc: http://127.0.0.1:8000/redoc

## System Health utilities
- Endpoint: `GET /health`
- Description: Returns host CPU, memory and disk usage percentages and a derived `system_status`.
- Thresholds (configurable) and status mapping are defined in [services/metrics_service.py](services/metrics_service.py).
	- CPU: threshold 50, critical 85
	- Memory: threshold 60, critical 85
	- Disk: threshold 60, critical 85

Status mapping per metric:
- Healthy: usage < threshold
- Warning: threshold ≤ usage < critical
- Unhealthy: usage ≥ critical

Example:
```json
{
	"cpu_percentage": 34.2,
	"memory_percentage": 62.1,
	"disk_percentage": 45.8,
	"system_status": "Healthy"
}
```

## AWS Utilities - EC2 & S3
- Service: [services/aws_service.py](services/aws_service.py)
- Description: Returns summary of AWS services - EC2 & S3
- Endpoints (prefix `/aws`):
	- `GET /aws/s3`:S3 bucket summary.
	- `GET /aws/ec2`: EC2 instance summary and details.

`GET /aws/s3` response includes:
- `total_buckets`: Total number of S3 buckets.
- `total_new_buckets`: Number of S3 buckets created within 90days.
- `total_old_buckets`: Number of S3 buckets older than 90days.
- `new_buckets` / `old_buckets`: List containing names of respective S3 buckets.

`GET /aws/ec2` response includes:
- `total_instances`: Total number of EC2 instances discovered.
- `running_count`: Number of instances in `running` state.
- `stopped_count`: Number of instances in `stopped` state.
- `other_count`: Number of instances in any other state (e.g., `pending`, `stopping`, `shutting-down`, `terminated`).
- `state_counts`: Map of exact state name → count (e.g., {"running": 3, "stopped": 2, "terminated": 1}).
- `instances_by_state`: Map of exact state name → list of instance objects.
- `running_instances` / `stopped_instances` / `other_instances`: Compatibility lists for quick access.


## Notes
- The root route (`/`) currently shows a placeholder and is intentionally not documented here. It will be updated later.
- The AWS endpoints require valid AWS credentials. The service performs a lightweight STS validation (`get_caller_identity`).
- Provide credentials via:
	- AWS CLI: Use `aws configure` command.
	- Environment variables

