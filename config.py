# Configurazione applicazione
# Questo file contiene le impostazioni di configurazione

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

# Titolo dell'applicazione
APP_TITLE = "OpenReports"
