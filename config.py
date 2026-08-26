from pathlib import Path

# File degli utenti (hash SHA256 delle password)
USERS_FILE = Path(__file__).parent / "users.json"

# Porta del server
SERVER_PORT = 7489

# Directory del progetto
BASE_DIR = Path(__file__).parent

# Directory dei report
REPORTS_DIR = BASE_DIR / "reports"

# Directory dei dataset
DATASETS_DIR = BASE_DIR / "datasets"

# Directory per report generati
GENERATED_DIR = BASE_DIR / "generated"

# Uvicorn server configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7489
SERVER_RELOAD = True
SERVER_WORKERS = 2

# MCP server configuration
MCP_HOST = "0.0.0.0"
MCP_PORT = 6485

# Authentication token for MCP server (set to None to disable auth)
MCP_AUTH_TOKEN = "pippo" #None
