
# Internal DevOps Utilities API

Lightweight internal FastAPI service that exposes small operational utilities for system health, AWS usage inspection, and quick developer tools.

#### Key points
- Small, self-contained FastAPI app with a polished static home UI at `/` (served from `app/static/index.html`).
- Exposes operational endpoints for system health and AWS resources (S3, EC2, cost summary).

### Quick start

1. Fork & clone the repo:

```bash
git clone <repo-url>
```

2. Create a virtual environment and install requirements:

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

3. Run the app:

```bash
py main.py
```

4. Open http://127.0.0.1:8000/ to see the UI and `/docs` for the OpenAPI UI.

### Main files
- `app/api.py`: FastAPI application.
- `app/static/index.html`: Landing page with quick usage guide.
- `app/static/styles.css`: Styling for the landing page.
- `routers/*`: API routers (system health, aws)
- `services/*`: helper/service code used by routers

### Endpoints
- `GET /health` — basic system health check.
- `GET /aws/s3` — S3 bucket listing / info.
- `GET /aws/s3/analytics` — S3 analytics/sample reports.
- `GET /aws/ec2` — EC2 instance info.
- `GET /aws/summary` — Cost and usage summary.


### Notes
- This repo is intended for internal use. Keep credentials and sensitive config out of the codebase.
- If you want `/` to show a different page, edit `app/api.py` and `app/static/index.html` accordingly.
- The app mounts `app/static` at `/static`, so the landing page and assets are available under `/static/*`.

