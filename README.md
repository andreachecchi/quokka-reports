# 🦘 Quokka Reports

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-orange.svg)](https://fastapi.tiangolo.com)

**Quokka Reports** is a lightweight, open-source report generation system that transforms database queries and external data sources into beautiful, shareable reports in multiple formats (HTML, PDF, Excel).

<div align="center">
  <img src="quokka-reports.jpg" alt="Quokka Reports Logo" width="200"/>
</div>

## ✨ Features

- 📊 **Multi-format report generation**: Generate reports as HTML, PDF, or Excel files
- 🔄 **Dynamic data sources**: Support for PostgreSQL database and custom data providers
- 🎨 **Template-based design**: Create stunning reports using HTML/CSS templates
- 🔐 **User authentication**: Built-in SHA256 password hashing and user management
- 📁 **Organized structure**: Reports, datasets, and templates organized in separate directories
- 🌐 **Modern web interface**: Built with FastAPI and static HTML/JavaScript
- 📤 **Export versatility**: Export data to Excel with multiple sheets (one per dataset)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+

**Note:** Quokka Reports does not require a database to run - databases are only used as data sources for generating reports.

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/quokka-reports.git
cd quokka-reports
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure users**
Edit `users.json` to add your users:
```json
{
  "users": [
    {
      "id": 1,
      "name": "Your Name",
      "username": "your_username",
      "password": "SHA256_HASH_HERE",
      "email": "your@email.com",
      "isactive": 1,
      "group": "admins",
      "locale": "en"
    }
  ]
}
```

4. **Configure data sources**
Edit your dataset JSON files in the `datasets/` directory to connect to your databases.

5. **Run the server**
```bash
python webserve.py
```

6. **Access the application**
Open your browser and navigate to `http://localhost:7489`

## 📁 Project Structure

```
quokka-reports/
├── auth.py              # User authentication module (SHA256)
├── config.py            # Application configuration
├── engine.py            # Report generation engine
├── excel.py             # Excel export functionality
├── pdf.py               # PDF generation using Playwright
├── webserve.py          # FastAPI web server
├── users.json           # User accounts database
├── data_providers/      # Data source implementations
│   ├── postgresql.py    # PostgreSQL connector
├── datasets/            # Dataset definitions
│   └── [dataset_name].ds/
│       └── dataset.json
├── reports/             # Report templates
│   └── [report_name].rp/
│       ├── report.json
│       ├── report.html
│       └── report.css
├── generated/           # Generated report output
└── templates/           # Web interface templates
    ├── login.html
    ├── reports.html
    └── report.html
```

## 📝 Configuration

### Data Provider Types

Quokka Reports supports various data provider types:

| Type | Description | Required Config |
|------|-------------|-----------------|
| `postgresql` | PostgreSQL database | host, port, name, username, password, query |

### Dataset Configuration Example

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
    { "id": "from_date", "type": "date", "name": "Start Date" },
    { "id": "to_date", "type": "date", "name": "End Date" }
  ],
  "query": "SELECT * FROM my_table WHERE date >= ${from_date} AND date <= ${to_date}"
}
```

### Report Configuration Example

```json
{
  "id": "my_report",
  "name": "My Report",
  "description": "A detailed report",
  "category": "Sales",
  "tags": ["monthly", "sales"],
  "datasets": [
    { "id": "my_dataset" }
  ],
  "template": "report.html"
}
```

## 🔒 Authentication

Quokka Reports uses SHA256 hashing for password storage. To create a new user:

1. Generate a SHA256 hash of your password:
```bash
python3 -c "import hashlib; print(hashlib.sha256('your_password'.encode()).hexdigest())"
```

2. Add the user to `users.json` with the hashed password

## 📊 Report Generation

Reports can be generated in three formats:

1. **HTML** - Interactive web-based reports (default)
2. **PDF** - Static documents for printing/sharing
3. **Excel** - Multi-sheet spreadsheets for data analysis

## 🔌 Extending Data Providers

Add support for new data sources by creating a new file in `data_providers/`:

```python
def fetch_data(dataset_config):
    """
    Your data provider implementation.
    
    Args:
        dataset_config: Full dataset configuration dictionary
    
    Returns:
        Dictionary with 'columns' and 'rows' keys
    """
    # Your data fetching logic here
    return {
        'columns': ['col1', 'col2'],
        'rows': [['value1', 'value2']]
    }
```

Then reference the provider type in your dataset configuration.

## 🐛 Troubleshooting

**Common Issues:**

1. **PDF generation fails**: Ensure Chromium/Chrome is installed and Playwright dependencies are set up
   ```bash
   playwright install chromium
   ```

2. **Database connection errors**: Verify your database credentials and network access

3. **Template rendering issues**: Ensure all dataset IDs in the report match available datasets

## 📄 License

This project is licensed under the AGPL v3 License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📬 Contact

Project Link: [https://github.com/andreachecchi/quokka-reports](https://github.com/andreachecchi/quokka-reports)

---

*Made with ❤️ by the Quokka Team*
