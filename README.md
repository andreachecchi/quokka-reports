# 🦘 Quokka Reports

> **Transform your data into beautiful reports.**

![Logo](quokka-reports-large.png)

[![License: AGPL
v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-orange.svg)](https://fastapi.tiangolo.com)

Quokka Reports is an open-source reporting platform that transforms SQL
queries and external data sources into elegant HTML, PDF and Excel
reports through a modular architecture based on datasets, templates and
pluggable data providers.

------------------------------------------------------------------------

## 📑 Table of Contents

-   [Why Quokka](#-why-quokka)
-   [Features](#-features)
-   [Architecture](#-architecture)
-   [Quick Start](#-quick-start)
-   [Project Structure](#-project-structure)
-   [Configuration](#-configuration)
-   [User Management](#-user-management)
-   [Authentication](#-authentication)
-   [Output Formats](#-output-formats)
-   [Extending Quokka](#-extending-quokka)
-   [Troubleshooting](#-troubleshooting)
-   [Roadmap](#-roadmap)
-   [Contributing](#-contributing)
-   [Acknowledgem# 🦘 Quokka Reports

> **Transform your data into beautiful reports.**

![Logo](quokka-reports.jpg)

[![License: AGPL
v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-orange.svg)](https://fastapi.tiangolo.com)

Quokka Reports is an open-source reporting platform that transforms SQL
queries and external data sources into elegant HTML, PDF and Excel
reports through a modular architecture based on datasets, templates and
pluggable data providers.

------------------------------------------------------------------------

## 📑 Table of Contents

-   [Why Quokka](#-why-quokka)
-   [Features](#-features)
-   [Architecture](#-architecture)
-   [Quick Start](#-quick-start)
-   [Project Structure](#-project-structure)
-   [Configuration](#-configuration)
-   [User Management](#-user-management)
-   [Authentication](#-authentication)
-   [Output Formats](#-output-formats)
-   [Extending Quokka](#-extending-quokka)
-   [Troubleshooting](#-troubleshooting)
-   [Roadmap](#-roadmap)
-   [Contributing](#-contributing)
-   [Acknowledgements](#-acknowledgements)
-   [Professional Support](#-professional-support)
-   [License](#-license)

------------------------------------------------------------------------

# 🚀 Why Quokka

Quokka Reports was born from real operational needs: generating reusable
reports from heterogeneous systems without embedding business logic into
applications.

Core principles:

-   Separate data retrieval from presentation.
-   Keep datasets reusable.
-   Use HTML/CSS for report design.
-   Make data providers pluggable.
-   Support multiple output formats.

# ✨ Features

### Reporting

-   HTML, PDF and Excel output
-   Multi-dataset reports
-   Multi-sheet Excel export
-   Responsive HTML templates

### Data Sources

-   PostgreSQL
-   Graylog
-   Custom providers

### Administration

-   Interactive user management
-   User activation/deactivation
-   Password management

### Platform

-   FastAPI
-   Localization
-   JSON configuration
-   Modular architecture

# 🏗 Architecture

``` text
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

# 🚀 Quick Start

``` bash
git clone https://github.com/andreachecchi/quokka-reports.git
cd quokka-reports
pip install -r requirements.txt
python management.py
python quokka.py
```

Browse to http://localhost:7489

# 📁 Project Structure

``` text
data_providers/
datasets/
reports/
templates/
generated/
locales/
users.json
```

# 📝 Configuration

Providers are configured through dataset JSON files.

Supported providers:

  Provider     Purpose
  ------------ ---------------------
  postgresql   SQL databases
  graylog      SIEM / Log analysis

Include your previous PostgreSQL / Graylog examples here.

# 🛠 User Management

Run:

``` bash
python management.py
```

Capabilities:

-   Create users
-   Update users
-   Delete users
-   Activate / Deactivate
-   Password reset
-   Validation

# 🔒 Authentication

Passwords are stored using SHA256.

Both `active` and legacy `isactive` fields are supported.

# 📊 Output Formats

  Format   Description
  -------- ----------------------
  HTML     Interactive report
  PDF      Printable document
  Excel    Multi-sheet workbook

# 🔌 Extending Quokka

Create a provider inside `data_providers`.

``` python
def fetch_data(dataset_config):
    return {
        "columns": [],
        "rows": []
    }
```

# 🐛 Troubleshooting

-   Install Playwright Chromium

``` bash
playwright install chromium
```

-   Verify provider credentials.
-   Verify dataset IDs.

# 🛣 Roadmap

-   More providers
-   Scheduling
-   API
-   Charts
-   Docker image

# 🤝 Contributing

Feedback, feature requests and pull requests are welcome.

If you'd like to contribute, please open an Issue first so we can
discuss the proposed change before implementation.

# 🙏 Acknowledgements

Quokka Reports was born from real-world operational experience.

Special thanks to **Qubit Futura Srl**, whose work on enterprise
networking, cybersecurity, infrastructure monitoring and SIEM platforms
inspired the architecture and many of the project's features.

# 🏢 Professional Support

If your organization needs help integrating Quokka Reports into
production environments, **Qubit Futura Srl** can provide professional
services including:

-   Enterprise networking
-   Cybersecurity
-   SIEM and Graylog
-   Log collection and normalization
-   Custom data providers
-   Report design
-   Infrastructure integration

LinkedIn:

https://it.linkedin.com/company/qubitfutura-srl

# 📄 License

Licensed under AGPL v3.
ents](#-acknowledgements)
-   [Professional Support](#-professional-support)
-   [License](#-license)

------------------------------------------------------------------------

# 🚀 Why Quokka

Quokka Reports was born from real operational needs: generating reusable
reports from heterogeneous systems without embedding business logic into
applications.

Core principles:

-   Separate data retrieval from presentation.
-   Keep datasets reusable.
-   Use HTML/CSS for report design.
-   Make data providers pluggable.
-   Support multiple output formats.

# ✨ Features

### Reporting

-   HTML, PDF and Excel output
-   Multi-dataset reports
-   Multi-sheet Excel export
-   Responsive HTML templates

### Data Sources

-   PostgreSQL
-   Graylog
-   Custom providers

### Administration

-   Interactive user management
-   User activation/deactivation
-   Password management

### Platform

-   FastAPI
-   Localization
-   JSON configuration
-   Modular architecture

# 🏗 Architecture

``` text
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

# 🚀 Quick Start

``` bash
git clone https://github.com/andreachecchi/quokka-reports.git
cd quokka-reports
pip install -r requirements.txt
python management.py
python quokka.py
```

Browse to http://localhost:7489

# 📁 Project Structure

``` text
data_providers/
datasets/
reports/
templates/
generated/
locales/
users.json
```

# 📝 Configuration

Providers are configured through dataset JSON files.

Supported providers:

  Provider     Purpose
  ------------ ---------------------
  postgresql   SQL databases
  graylog      SIEM / Log analysis

Include your previous PostgreSQL / Graylog examples here.

# 🛠 User Management

Run:

``` bash
python management.py
```

Capabilities:

-   Create users
-   Update users
-   Delete users
-   Activate / Deactivate
-   Password reset
-   Validation

# 🔒 Authentication

Passwords are stored using SHA256.

Both `active` and legacy `isactive` fields are supported.

# 📊 Output Formats

  Format   Description
  -------- ----------------------
  HTML     Interactive report
  PDF      Printable document
  Excel    Multi-sheet workbook

# 🔌 Extending Quokka

Create a provider inside `data_providers`.

``` python
def fetch_data(dataset_config):
    return {
        "columns": [],
        "rows": []
    }
```

# 🐛 Troubleshooting

-   Install Playwright Chromium

``` bash
playwright install chromium
```

-   Verify provider credentials.
-   Verify dataset IDs.

# 🛣 Roadmap

-   More providers
-   Scheduling
-   API
-   Charts
-   Docker image

# 🤝 Contributing

Feedback, feature requests and pull requests are welcome.

If you'd like to contribute, please open an Issue first so we can
discuss the proposed change before implementation.

# 🙏 Acknowledgements

Quokka Reports was born from real-world operational experience.

Special thanks to **Qubit Futura Srl**, whose work on enterprise
networking, cybersecurity, infrastructure monitoring and SIEM platforms
inspired the architecture and many of the project's features.

# 🏢 Professional Support

![Logo](qubit-futura-logo.jpg)

If your organization needs help integrating Quokka Reports into
production environments, **Qubit Futura Srl** can provide professional
services including:

-   Enterprise networking
-   Cybersecurity
-   SIEM and Graylog
-   Log collection and normalization
-   Custom data providers
-   Report design
-   Infrastructure integration

LinkedIn:

https://it.linkedin.com/company/qubitfutura-srl

# 📄 License

Licensed under AGPL v3.
