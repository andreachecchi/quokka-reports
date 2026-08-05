# 🦘 Quokka Reports

> **Transform your data into beautiful reports.**

![Logo](quokka-reports-large.png)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-orange.svg)](https://fastapi.tiangolo.com)

Quokka Reports is an open-source reporting platform that transforms SQL queries and external data sources into polished HTML, PDF and Excel reports through a modular architecture based on datasets, templates and pluggable data providers.

---

## 📑 Table of Contents

- Why Quokka
- Features
- Architecture
- Quick Start
- Project Structure
- Configuration
- User Management
- Authentication
- Output Formats
- Extending Quokka
- Troubleshooting
- Roadmap
- Contributing
- Acknowledgements
- Professional Support
- License

---

## 🚀 Why Quokka

Quokka Reports was created to solve real-world reporting challenges by separating data retrieval from presentation.

Core principles:

- Separate data retrieval from presentation.
- Promote reusable dataset definitions.
- Design reports using standard HTML and CSS.
- Make data providers pluggable.
- Support multiple output formats.

---

## ✨ Features

### Reporting

- HTML, PDF and Excel output
- Multi-dataset reports
- Multi-sheet Excel export
- Responsive HTML templates

### Data Sources

- PostgreSQL
- Graylog
- Custom providers

### Administration

- Interactive user management
- User activation and deactivation
- Password management

### Platform

- FastAPI
- Localization support
- JSON configuration
- Modular architecture

---

## 🏗 Architecture

```text
 PostgreSQL     Graylog     REST APIs
      │             │            │
      └──────┬──────┴────────────┘
             ▼
      Custom Data Providers
             ▼
      Dataset Definitions
             ▼
        Quokka Engine
             ▼
     HTML | PDF | Excel
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/andreachecchi/quokka-reports.git
cd quokka-reports
pip install -r requirements.txt
python management.py
python quokka.py
```

Open your browser at:

`http://localhost:7489`

---

## 📁 Project Structure

```text
data_providers/
datasets/
reports/
templates/
generated/
locales/
users.json
```

---

## 📝 Configuration

Providers are configured through dataset JSON files.

Supported providers:

| Provider | Purpose |
|----------|---------|
| postgresql | SQL databases |
| graylog | SIEM / Log analysis |

---

## 🛠 User Management

Run:

```bash
python management.py
```

Capabilities:

- Create users
- Update users
- Delete users
- Activate / Deactivate users
- Reset passwords
- Validate configuration

---

## 🔒 Authentication

- Passwords are stored using SHA-256 hashes.
- Both `active` and legacy `isactive` fields are supported.

---

## 📊 Output Formats

| Format | Description |
|---------|-------------|
| HTML | Interactive reports |
| PDF | Printable documents |
| Excel | Multi-sheet workbooks |

---

## 🔌 Extending Quokka

Create a new provider inside `data_providers`:

```python
def fetch_data(dataset_config):
    return {
        "columns": [],
        "rows": []
    }
```

---

## 🐛 Troubleshooting

Install Playwright Chromium:

```bash
playwright install chromium
```

Also verify:

- Provider credentials
- Dataset identifiers

---

## 🛣 Roadmap

- Additional data providers
- Report scheduling
- REST API
- Charts and dashboards
- Docker image

---

## 🤝 Contributing

Feedback, feature requests and pull requests are welcome.

Please open an Issue before starting significant changes so we can discuss the proposed implementation.

---

## 🙏 Acknowledgements

Quokka Reports was born from real-world operational experience.

Special thanks to **Qubit Futura Srl**, whose work in enterprise networking, cybersecurity, infrastructure monitoring and SIEM platforms inspired the architecture and many of the project's features.

---

## 🏢 Professional Support

Need help deploying Quokka Reports in production?

**Qubit Futura Srl** offers professional services including:

- Enterprise networking
- Cybersecurity
- SIEM and Graylog integration
- Log collection and normalization
- Custom data providers
- Report design
- Infrastructure integration
- Technical consulting

LinkedIn:

https://it.linkedin.com/company/qubitfutura-srl

---

## 📄 License

Licensed under the AGPL v3 License.

