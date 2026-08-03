import json
from pathlib import Path
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from config import SERVER_PORT, USERS_FILE, APP_TITLE
from auth import authenticate_user, hash_password, get_user_by_username
from urllib.parse import quote, unquote

# Create FastAPI app
app = FastAPI(title=APP_TITLE)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/generated", StaticFiles(directory="generated"), name="generated")
app.mount("/locales", StaticFiles(directory="locales"), name="locales")


# ==================== Pydantic Models ====================

class LoginRequest(BaseModel):
    username: str
    password: str


class ExecuteReportRequest(BaseModel):
    params: dict


# ==================== Helper Functions ====================

def check_session(request: Request) -> bool:
    """Check if user is authenticated via cookies."""
    return request.cookies.get("authenticated") == "true"


def get_report_details(report_id: str) -> dict:
    """Get report details from report.json file by report ID."""
    reports_dir = Path("reports")
    
    if not reports_dir.exists():
        return None
    
    # Search for report by ID in report.json files
    for rp_dir in reports_dir.iterdir():
        if rp_dir.is_dir():
            report_json_path = rp_dir / "report.json"
            if report_json_path.exists():
                try:
                    with open(report_json_path, "r") as f:
                        report_config = json.load(f)
                    
                    # Match by the 'id' field in report.json
                    if report_config.get("id") == report_id:
                        return report_config
                except json.JSONDecodeError:
                    continue
    
    return None


def get_dataset_params(dataset_id: str) -> dict:
    """Get dataset info from dataset.json file."""
    datasets_dir = Path("datasets")
    
    if not datasets_dir.exists():
        return {}
    
    for ds_dir in datasets_dir.iterdir():
        if ds_dir.is_dir():
            ds_json_path = ds_dir / "dataset.json"
            if ds_json_path.exists():
                try:
                    with open(ds_json_path, "r") as f:
                        ds_config = json.load(f)
                    if ds_config.get("id") == dataset_id:
                        return {
                            "id": ds_config.get("id"),
                            "name": ds_config.get("name", ""),
                            "description": ds_config.get("description", ""),
                            "params": ds_config.get("params", [])
                        }
                except:
                    continue
    
    return {}


def get_reports_list() -> list:
    """Get all available reports from filesystem."""
    reports_dir = Path("reports")
    reports = []
    
    if not reports_dir.exists():
        return reports
    
    for report_dir in reports_dir.iterdir():
        if report_dir.is_dir():
            report_json_path = report_dir / "report.json"
            if report_json_path.exists():
                try:
                    with open(report_json_path, "r") as f:
                        report_config = json.load(f)
                    
                    report_info = {
                        "id": report_config.get("id", report_dir.name),
                        "name": report_config.get("name", report_dir.name),
                        "description": report_config.get("description", ""),
                        "category": report_config.get("category", ""),
                        "tags": report_config.get("tags", [])
                    }
                    if report_config.get("active", True):  # default to True if "active" is missing
                        reports.append(report_info)
                except json.JSONDecodeError:
                    continue
    
    return sorted(reports, key=lambda r: r["name"])


# ==================== Pages ====================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect to login page."""
    if check_session(request):
        return RedirectResponse(url="/reports")
    return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    """Show login page."""
    html_path = Path("templates/login.html")
    if not html_path.exists():
        raise HTTPException(status_code=500, detail="Template not found")
    
    with open(html_path, "r") as f:
        html_content = f.read()
    
    # Replace APP_TITLE in the template
    html_content = html_content.replace("Report System", APP_TITLE)
    
    return HTMLResponse(content=html_content)


@app.get("/reports", response_class=HTMLResponse)
async def show_reports(request: Request):
    """Show reports list page (requires authentication)."""
    if not check_session(request):
        return RedirectResponse(url="/login")
    
    # Get reports data from filesystem
    reports = get_reports_list()
    
    # Read the HTML file from templates
    html_path = Path("templates/reports.html")
    if not html_path.exists():
        raise HTTPException(status_code=500, detail="Template not found")
    
    with open(html_path, "r") as f:
        html_content = f.read()
    
    # Replace the empty REPORTS_DATA with actual data and APP_TITLE
    reports_json = json.dumps(reports)
    html_content = html_content.replace("const REPORTS_DATA = [];", f"const REPORTS_DATA = {reports_json};")
    html_content = html_content.replace("Report System", APP_TITLE)
    
    return HTMLResponse(content=html_content)


@app.get("/report/{report_id}", response_class=HTMLResponse)
async def show_report_page(request: Request, report_id: str):
    """Show report execution page (requires authentication)."""
    if not check_session(request):
        return RedirectResponse(url="/login")
    
    report = get_report_details(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Get dataset parameters
    datasets_info = []
    for dataset_config in report.get("datasets", []):
        dataset_id = dataset_config.get("id")
        if dataset_id:
            dataset_info = get_dataset_params(dataset_id)
            if dataset_info:
                datasets_info.append(dataset_info)
    
    # Read the HTML file from templates
    html_path = Path("templates/report.html")
    if not html_path.exists():
        raise HTTPException(status_code=500, detail="Template not found")
    
    with open(html_path, "r") as f:
        html_content = f.read()
    
    # Replace placeholders with actual data
    report_json = json.dumps(report)
    datasets_json = json.dumps(datasets_info)
    
    html_content = html_content.replace("{report_name}", report.get("name", "Report"))
    html_content = html_content.replace("{report_description}", report.get("description", ""))
    html_content = html_content.replace("const REPORT_DATA = {};", f"const REPORT_DATA = {report_json};")
    html_content = html_content.replace("const DATASETS_DATA = [];", f"const DATASETS_DATA = {datasets_json};")
    html_content = html_content.replace("Report System", APP_TITLE)
    
    return HTMLResponse(content=html_content)


# ==================== API Endpoints ====================

@app.post("/api/login")
async def login(login_data: LoginRequest):
    """Handle login request."""
    username = login_data.username
    password = login_data.password
    
    # Authenticate using users.json
    user = authenticate_user(username, password)
    
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    display_name = user.get('name', user.get('username', 'Unknown'))
    # Remove any quotes that might be part of the string value
    display_name = str(display_name).strip('"').strip("'")
    
    # Get locale if it exists
    locale = user.get('locale', None)
    
    response = JSONResponse(content={
        "success": True,
        "username": username,
        "display_name": display_name
    })
    response.set_cookie("authenticated", "true", httponly=True, max_age=3600)
    response.set_cookie("username", username, httponly=True, max_age=3600)
    # Set display_name without httponly so JS can read it for display
    # Encode the value to avoid auto-quotes by FastAPI/Starlette
    response.set_cookie("display_name", quote(display_name), path="/", max_age=3600, secure=False, samesite="Lax")
    # Set locale if it exists in user data
    if locale:
        response.set_cookie("locale", quote(locale), path="/", max_age=3600, secure=False, samesite="Lax")
    return response


@app.get("/api/auth/status")
async def auth_status(request: Request):
    """Check if user is authenticated."""
    if check_session(request):
        username = request.cookies.get("username", "unknown")
        locale = request.cookies.get("locale")
        result = {"authenticated": True, "username": username}
        if locale:
            result["locale"] = unquote(locale)
        return result
    raise HTTPException(status_code=401, detail="Not authenticated")


@app.post("/api/logout")
async def logout():
    response = JSONResponse(
        content={"success": True, "redirect": "/login"}
    )

    response.delete_cookie("authenticated", path="/")
    response.delete_cookie("username", path="/")
    response.delete_cookie("display_name", path="/")
    response.delete_cookie("locale", path="/")

    return response


@app.get("/api/reports")
async def list_reports():
    """List all available reports."""
    reports = get_reports_list()
    return {"reports": reports}


@app.get("/api/report/{report_id}")
async def get_report_endpoint(report_id: str):
    """Get report details by ID."""
    report = get_report_details(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Get dataset parameters
    datasets_info = []
    for dataset_config in report.get("datasets", []):
        dataset_id = dataset_config.get("id")
        if dataset_id:
            dataset_info = get_dataset_params(dataset_id)
            if dataset_info:
                datasets_info.append(dataset_info)
    
    return {
        "id": report.get("id", report_id),
        "name": report.get("name", report_id),
        "description": report.get("description", ""),
        "datasets": datasets_info
    }


@app.post("/api/report/{report_id}/execute")
async def execute_report(report_id: str, execute_request: ExecuteReportRequest):
    """Execute a report with given parameters."""
    from engine import generate_report
    
    # Convert params to engine format
    engine_params = []
    for dataset_id, dataset_params in execute_request.params.items():
        if dataset_params:
            engine_params.append({
                "dataset_id": dataset_id,
                "params": [{k: v} for k, v in dataset_params.items()]
            })
    
    try:
        html_path = generate_report(report_id, engine_params)
        return {"success": True, "html_path": str(html_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/report/{report_id}/pdf")
async def generate_pdf(report_id: str, html_path: str):
    """Generate PDF from HTML report."""
    from pdf import html_to_pdf
    
    # Build full path to the generated HTML file
    html_full_path = Path("generated") / html_path
    
    try:
        pdf_path = await html_to_pdf(str(html_full_path))
        return {"success": True, "pdf_path": str(pdf_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/report/{report_id}/excel")
async def generate_excel(report_id: str, html_path: str, params: str):
    """Generate Excel file from HTML report with multiple sheets (one per dataset)."""
    from engine import generate_excel_report
    from urllib.parse import unquote
    
    try:
        # Decode and parse params
        params_dict = json.loads(unquote(params))
        
        # Convert to engine format: dataset_id -> dict of parameters
        engine_params = {}
        for dataset_id, dataset_params in params_dict.items():
            if dataset_params:
                engine_params[dataset_id] = dataset_params
        
        excel_path = generate_excel_report(report_id, engine_params)
        return {"success": True, "excel_path": str(excel_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Main ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("webserve:app", host="0.0.0.0", port=SERVER_PORT, reload=True)
