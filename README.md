# 🦘 Quokka Reports

<div align="center">
  <img src="quokka-reports.png" alt="Quokka Reports Logo" width="220"/>
</div>

<p align="center">

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-orange.svg)](https://fastapi.tiangolo.com)

</p>

**Quokka Reports** is a lightweight, open-source reporting platform that transforms SQL queries and external data sources into beautiful, shareable reports in **HTML**, **PDF**, and **Excel** formats.

Designed around a modular architecture, Quokka Reports separates **report definitions**, **datasets**, and **data providers**, making it easy to build custom reporting solutions while keeping the project simple to configure and extend.

---

# ✨ Features

## 📊 Reporting

* Generate reports in **HTML**, **PDF**, and **Excel**
* Multi-dataset reports
* Multi-sheet Excel export (one worksheet per dataset)
* HTML/CSS template-based rendering
* Printable and shareable reports

## 🔄 Data Sources

* PostgreSQL support
* Graylog support
* Modular data provider architecture
* Easily extendable with custom providers

## 🔐 Security

* SHA256 password hashing
* Active/Inactive user management
* Login authentication
* Multi-language interface through locale files

## 🛠 Administration

* Interactive user management utility
* Password reset
* User activation/deactivation
* User creation and deletion
* Automatic validation and persistence

---

# 🚀 Quick Start

## Prerequisites

* Python **3.11** or newer

> **Note**
>
> Quokka Reports does not require its own database.
> Databases are only used as data sources during report generation.

## Installation

Clone the repository:

```bash
git clone https://github.com/andreachecchi/quokka-reports.git
cd quokka-reports
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Configure your users:

```bash
python management.py
```

Configure your datasets inside the `datasets/` directory.

Start the application:

```bash
python quokka.py
```

Open your browser:

```
http://localhost:7489
```

---

# 📁 Project Structure

```text
quokka-reports/
├── quokka.py            # FastAPI application
├── auth.py              # Authentication
├── config.py            # Application configuration
├── engine.py            # Report generation engine
├── excel.py             # Excel export
├── pdf.py               # PDF generation
├── management.py        # User management utility
├── users.json           # User database
│
├── data_providers/
│   ├── postgresql.py
│   ├── graylog.py
│   └── ...
│
├── datasets/
│   └── [dataset].ds/
│       └── dataset.json
│
├── reports/
│   └── [report].rp/
│       ├── report.json
│       ├── report.html
│       └── report.css
│
├── generated/
├── templates/
└── locales/
```

---

# 📝 Configuration

## Supported Data Providers

Quokka Reports currently supports the following data providers:

| Provider     | Description          |
| ------------ | -------------------- |
| `postgresql` | PostgreSQL databases |
| `graylog`    | Graylog Search API   |

Every provider is implemented as a Python module inside:

```text
data_providers/
```

Each provider must expose a `fetch_data()` function.

---

## PostgreSQL Dataset Example

```json
{
  "id": "my_dataset",
  "name": "My Dataset",
  "description": "Description of my dataset",
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "mydb",
    "username": "myuser",
    "password": "mypassword"
  },
  "params": [
    {
      "id": "from_date",
      "type": "date",
      "name": "Start Date"
    },
    {
      "id": "to_date",
      "type": "date",
      "name": "End Date"
    }
  ],
  "query": "SELECT * FROM my_table WHERE date >= ${from_date} AND date <= ${to_date}"
}
```

---

## Graylog Dataset Example

```json
{
  "id": "graylog_dataset",
  "name": "Graylog Logs",
  "description": "Graylog search data",
  "database": {
    "type": "graylog",
    "url": "http://localhost:9000",
    "token": "my-graylog-token"
  },
  "params": [
    {
      "id": "from",
      "type": "datetime",
      "name": "Start Time"
    },
    {
      "id": "to",
      "type": "datetime",
      "name": "End Time"
    }
  ],
  "fields": [
    "timestamp",
    "user",
    "msg"
  ],
  "query": "action:tunnel-stats",
  "time_range": {
    "from": "${from}",
    "to": "${to}"
  }
}
```

---

## Report Definition Example

```json
{
  "id": "my_report",
  "name": "My Report",
  "description": "A detailed report",
  "category": "Sales",
  "tags": [
    "monthly",
    "sales"
  ],
  "datasets": [
    {
      "id": "my_dataset"
    }
  ],
  "template": "report.html",
  "active": true
}
```

---

# 🛠 User Management

Quokka Reports includes an interactive administration utility:

```bash
python management.py
```

The management console provides:

* Interactive menu system
* List all users
* Display detailed user information
* Create new users
* Update existing users
* Change passwords
* Activate or deactivate users
* Delete users
* Save changes automatically to `users.json`

Additional features include:

* Email validation
* Username uniqueness verification
* Password confirmation
* Automatic timestamp management
* Persistent storage

For backward compatibility, both the legacy `isactive` field and the current `active` field are supported.

Supported values are:

* `true` / `false`
* `1` / `0`

New users are always created using the `active` field.

---

# 🔒 Authentication

Quokka Reports stores passwords using **SHA256 hashing**.

A user can be:

| Status   | Description                                 |
| -------- | ------------------------------------------- |
| Active   | Can authenticate and access the application |
| Inactive | Login is denied                             |

---

# 📊 Output Formats

Reports can be generated in three formats.

| Format | Description                               |
| ------ | ----------------------------------------- |
| HTML   | Interactive web reports                   |
| PDF    | Printable and shareable documents         |
| Excel  | Multi-sheet workbook for further analysis |

---

# 🔌 Creating a Custom Data Provider

Adding support for a new data source is straightforward.

Create a new Python module inside:

```text
data_providers/
```

Implement the following function:

```python
def fetch_data(dataset_config):
    """
    Args:
        dataset_config: dataset configuration dictionary

    Returns:
        {
            "columns": [...],
            "rows": [...]
        }
    """

    return {
        "columns": ["column1", "column2"],
        "rows": [
            ["value1", "value2"]
        ]
    }
```

Then reference the provider name inside the dataset configuration:

```json
{
  "database": {
    "type": "my_provider"
  }
}
```

Quokka Reports will automatically load the corresponding module.

---

# 🐛 Troubleshooting

## PDF generation fails

Install the required Playwright browser:

```bash
playwright install chromium
```

---

## Database connection errors

Verify:

* Database credentials
* Network connectivity
* Firewall rules
* Provider configuration

---

## Template rendering issues

Ensure that:

* every dataset referenced by a report exists;
* dataset IDs match those declared in `report.json`;
* report templates are located inside the correct report directory.

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/my-feature
```

3. Commit your changes.

```bash
git commit -m "Add my feature"
```

4. Push your branch.

```bash
git push origin feature/my-feature
```

5. Open a Pull Request.

---

# 📄 License

This project is licensed under the **AGPL v3 License**.

See the `LICENSE` file for additional details.

---

# 📬 Contact

GitHub Repository:

https://github.com/andreachecchi/quokka-reports

---

<div align="center">

Made with ❤️ by the Quokka Team

</div>
