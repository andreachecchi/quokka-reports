# 🦘 Quokka Reports - User Documentation

> **Transform your data into beautiful reports.**

This document provides a comprehensive guide to using Quokka Reports, an open-source reporting platform that transforms SQL queries and external data sources into elegantly formatted HTML, PDF, and Excel reports.

---

## 📑 Table of Contents

- [Introduction](#-introduction)
- [Architecture](#-architecture)
- [1. User Management](#1-user-management)
  - [Main Menu of management.py](#main-menu-of-managementpy)
  - [User Operations](#user-operations)
  - [Practical Examples](#practical-examples)
- [2. Dataset Creation](#2-dataset-creation)
  - [Dataset Structure](#dataset-structure)
  - [Database Types and Providers](#database-types-and-providers)
  - [Dataset Parameters](#dataset-parameters)
  - [Practical Examples](#practical-examples-1)
- [3. Report Creation](#3-report-creation)
  - [Report Structure](#report-structure)
  - [Report Files: report.json, report.html, report.css](#report-files-reportjson-reporthtml-reportcss)
  - [Relationship with Datasets](#relationship-with-datasets)
  - [Practical Examples](#practical-examples-2)
- [4. Application Navigation](#4-application-navigation)
  - [Accessing the Application](#accessing-the-application)
  - [Searching for Reports](#searching-for-reports)
  - [Tags and Categories](#tags-and-categories)
  - [Running a Report](#running-a-report)
  - [Choosing Output Formats](#choosing-output-formats)
- [5. Output Formats](#5-output-formats)
  - [HTML](#html)
  - [PDF](#pdf)
  - [Excel](#excel)
- [6. Extensions and Customization](#6-extensions-and-customization)
  - [New Data Providers](#new-data-providers)
  - [Custom Templates](#custom-templates)
- [7. Troubleshooting](#7-troubleshooting)
- [Useful Resources](#useful-resources)

---

## 🚀 Introduction

Quokka Reports is a modular reporting platform designed to separate the data acquisition phase from the presentation phase.

### Core Principles

- **Separation of data from presentation**: Datasets handle data acquisition, reports handle presentation.
- **Dataset reuse**: A dataset can be used by multiple reports.
- **Standard templates**: Reports use standard HTML and CSS, without requiring special templating languages.
- **Pluggable providers**: Support for PostgreSQL, Graylog, and custom providers.

### Workflow Overview

```
1. User Management → 2. Dataset Creation → 3. Report Creation → 4. Execution
```

---

## 🏗 Architecture

```
 PostgreSQL     Graylog     API Custom
      │             │            │
      └──────┬──────┴────────────┘
             ▼
      Data Providers (postgresql.py, graylog.py, etc.)
             ▼
      Dataset Definitions (dataset.json)
             ▼
        Quokka Engine (engine.py)
             ▼
     HTML | PDF | Excel
```

---

## 1. User Management

Users are managed via the **`management.py`** script, which provides an interactive command-line interface for managing the `users.json` file.

### Main Menu of management.py

Run the script with:
```bash
python3 management.py
```

The main menu offers these options:

```
========================================
   USER MANAGEMENT - MAIN MENU
========================================
1. List all users
2. Show user details
3. Change user password
4. Update user data
5. Deactivate user
6. Create new user
7. Delete user
8. Save changes
0. Exit
========================================
```

### User Operations

#### 1. List all users (Listing all users)
Displays a table with:
- ID
- Name
- Username
- Email
- Status (Active/Inactive)

#### 2. Show user details (Viewing a user's details)
Enter the user's ID to see all their data.

#### 3. Change user password (Changing a password)
Enter the user's ID, then enter the new password twice for confirmation.

#### 4. Update user data (Updating user data)
You can modify:
- Name
- Username
- Email
- Group (user group)
- Locale (language, e.g., "it" or "en")

#### 5. Deactivate user (Deactivating a user)
Deactivates a user without deleting them. Deactivated users cannot access the application.

#### 6. Create new user (Creating a new user)
Requires:
- Name
- Username (unique)
- Email (valid)
- Password (displayed as asterisks)
- Group (optional)
- Locale (optional)

#### 7. Delete user (Deleting a user)
Permanently deletes the user from the system.

#### 8. Save changes (Saving changes)
Saves all modifications made to the `users.json` file.

### Practical Examples

**Example 1: Creating a new user**
```bash
$ python3 management.py
========================================
   USER MANAGEMENT - MAIN MENU
========================================
...
6. Create new user
...

Select: 6

Name: Mario Rossi
Username: m.rossi
Email: mario.rossi@azienda.it
New password: ********
Confirm new password: ********
Group [default]: it_department
Locale [default]: it

User created successfully!
```

**Example 2: Changing the password**
```bash
Select: 3

Enter user ID: 42
Changing password for: Mario Rossi (m.rossi)
New password: ********
Confirm new password: ********

Password updated successfully!
```

**Example 3: Deactivating a user**
```bash
Select: 5

Enter user ID: 42
User m.rossi has been deactivated.
```

---

## 2. Dataset Creation

A **dataset** defines how to retrieve data from a source (database, API, etc.) and how to handle parameters to filter results.

### Dataset Structure

A dataset is a directory inside `datasets/` containing:
- `dataset.json` — Main configuration file

**Example structure:**
```
datasets/
├── example01.ds/
│   └── dataset.json
├── sample_v1.ds/
│   └── dataset.json
└── sample_v2.ds/
    └── dataset.json
```

### The dataset.json File

The `dataset.json` file contains:

```json
{
  "id": "unique_identifier",
  "name": "Dataset Display Name",
  "description": "Dataset description",
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "database_name",
    "username": "user",
    "password": "password"
  },
  "params": [
    { "id": "from_date", "type": "date", "name": "Start date" },
    { "id": "to_date", "type": "date", "name": "End date" }
  ],
  "query": "SELECT * FROM table WHERE date >= ${from_date} AND date <= ${to_date}"
}
```

#### Required Parameters:

| Parameter | Description |
|-----------|-------------|
| `id` | Unique identifier for the dataset (used in reports) |
| `name` | Display name |
| `database` | Database configuration |
| `query` | SQL query (can start with `@` to read from file) |

#### Supported Parameter Types:
- `date` — Date
- `string` — Text
- `number` — Number

### Database Types and Providers

**Data providers** are Python modules in `data_providers/` that implement the `fetch_data()` function.

**Available Providers:**

| Provider | File | Description |
|----------|------|-------------|
| PostgreSQL | `postgresql.py` | Connection to PostgreSQL database |
| Graylog | `graylog.py` | Query Graylog API |
| Custom | `custom.py` | Custom providers |

#### PostgreSQL Provider

Configuration in `dataset.json`:
```json
{
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "database_name",
    "username": "user",
    "password": "password"
  },
  "query": "SELECT * FROM table"
}
```

#### Graylog Provider

Configuration in `dataset.json`:
```json
{
  "database": {
    "type": "graylog",
    "url": "http://graylog.example.com:8080",
    "token": "your_token"
  },
  "query": "your_search_query",
  "fields": ["timestamp", "source", "message"],
  "time_range": {
    "from": "2025-01-01T00:00:00.000Z",
    "to": "2027-01-02T00:00:00.000Z"
  },
  "order_by": "timestamp",
  "sort": "desc"
}
```

### Dataset Parameters

**Parameters** allow queries to be dynamic:

```json
{
  "params": [
    { 
      "id": "from_date", 
      "type": "date", 
      "name": "Start date" 
    },
    { 
      "id": "to_date", 
      "type": "date", 
      "name": "End date" 
    }
  ]
}
```

In the query, parameters are used with the `${param_id}` syntax:

```sql
SELECT * FROM intervention 
WHERE start_date >= ${from_date} 
  AND start_date <= ${to_date}
```

### Practical Examples

#### Example 1: PostgreSQL Dataset with Parameters

File: `datasets/sample_v1.ds/dataset.json`
```json
{
  "id": "sample_dataset_v1",
  "name": "Interventions by Period",
  "description": "Extracts maintenance interventions in a period",
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "cronoprogramma",
    "username": "cronos",
    "password": "cronos"
  },
  "params": [
    { "id": "from_date", "type": "date", "name": "Start date" },
    { "id": "to_date", "type": "date", "name": "End date" }
  ],
  "query": "SELECT id, luogo_intervento, data_inizio::date as data_inizio, descrizione_attivita from intervento where data_inizio >= ${from_date} and data_inizio <= ${to_date}"
}
```

#### Example 2: Graylog Dataset for Log Analysis

File: `datasets/example02.ds/dataset.json`
```json
{
  "id": "example_dataset_02",
  "name": "Recent Logs",
  "description": "Extracts recent logs from Graylog",
  "database": {
    "type": "graylog",
    "url": "http://graylog.example.com:8080",
    "token": "your_graylog_token"
  },
  "params": [
    { "id": "from", "type": "datetime", "name": "From date/time" },
    { "id": "to", "type": "datetime", "name": "To date/time" }
  ],
  "query": "level:ERROR",
  "fields": ["timestamp", "source", "message", "level"],
  "time_range": {
    "from": "2025-01-01T00:00:00.000Z",
    "to": "2027-01-02T00:00:00.000Z"
  },
  "order_by": "timestamp",
  "sort": "desc"
}
```

---

## 3. Report Creation

A **report** combines one or more datasets into a single styled HTML/CSS view.

### Report Structure

A report is a directory inside `reports/` containing:

```
reports/
├── example_01.rp/
│   ├── report.json       ← Main configuration
│   ├── report.html       ← HTML template
│   ├── report.css        ← CSS styles (optional)
│   └── quokka-reports.jpg ← Resources (images, etc.)
└── sample_v1.rp/
    ├── report.json
    ├── report.html
    ├── report.css
    └── report2.css
```

### Report Files: report.json, report.html, report.css

#### report.json

Main configuration file:

```json
{
  "id": "report_sample_v1",
  "name": "Example Report 01",
  "description": "This report demonstrates the system functionality",
  "category": "Test",
  "tags": ["example", "demo", "fun"],
  "datasets": [
    { "id": "sample_dataset_v1" },
    { "id": "sample_dataset_v2" }
  ],
  "template": "report.html",
  "active": true
}
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `id` | ✅ | Unique identifier for the report |
| `name` | ✅ | Display name |
| `description` | ✅ | Report description |
| `category` | ❌ | Category for organization (e.g., "Sales", "IT", "HR") |
| `tags` | ❌ | Array of tags for searching |
| `datasets` | ✅ | Array of datasets to use |
| `template` | ❌ | HTML template file name (default: "report.html") |
| `active` | ❌ | `true`/`false` to enable/disable |

#### report.html

Standard HTML template with placeholders for datasets:

```html
<html>
  <head>
    <link rel="stylesheet" href="report.css" />
  </head>
  <body>
    <h1>Report Title</h1>
    
    <table>
      <thead>
        <tr><th>Name</th><th>Value</th></tr>
      </thead>
      <tbody data-id="sample_dataset_v1"></tbody>
    </table>
    
    <h2>Another table</h2>
    <table>
      <thead>
        <tr><th>ID</th><th>Data</th></tr>
      </thead>
      <tbody data-id="sample_dataset_v2"></tbody>
    </table>
  </body>
</html>
```

**Important:**
- Use `data-id="dataset_name"` in `<tbody>` tags to identify where to insert data
- CSS/JS/image paths are relative to the report directory

#### report.css

Optional CSS file to customize the report style.

### Relationship with Datasets

A report references datasets using their `id`:

```json
{
  "datasets": [
    { "id": "sample_dataset_v1" },
    { "id": "sample_dataset_v2" }
  ]
}
```

The system:
1. Reads datasets from `dataset.json`
2. Retrieves necessary parameters
3. Executes queries
4. Inserts results into the HTML template at locations marked with `data-id`

### Practical Examples

#### Example 1: Simple Report with One Dataset

File: `reports/example_01.rp/report.json`
```json
{
  "id": "example_report_01",
  "name": "Example report 01",
  "description": "This is the example report number 01",
  "category": "Generic",
  "tags": ["fun", "test"],
  "datasets": [
    { "id": "example_dataset_01" }
  ],
  "template": "report.html",
  "active": true
}
```

File: `reports/example_01.rp/report.html`
```html
<html>
  <head>
    <link rel="stylesheet" href="report.css" />
  </head>
  <body>
    <h1>Example Report</h1>
    <table>
      <thead>
        <tr><th>Name</th><th>Value</th></tr>
      </thead>
      <tbody data-id="example_dataset_01"></tbody>
    </table>
  </body>
</html>
```

#### Example 2: Multi-Dataset Report with Multiple Tables

File: `reports/sample_v1.rp/report.json`
```json
{
  "id": "report_sample_v1",
  "name": "Example Report 01",
  "description": "This report demonstrates the system functionality",
  "category": "Test",
  "tags": ["example", "demo", "fun"],
  "datasets": [
    { "id": "sample_dataset_v1" },
    { "id": "sample_dataset_v2" }
  ],
  "template": "report.html"
}
```

File: `reports/sample_v1.rp/report.html`
```html
<html>
  <head>
    <link rel="stylesheet" href="report2.css" />
  </head>
  <body>
    <div>
      <img src="quokka-reports.jpg">
      <h1>Example Title</h1>
      
      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>luogo_intervento</th>
            <th>data_inizio</th>
            <th>descrizione_attivita</th>
          </tr>
        </thead>
        <tbody data-id="sample_dataset_v1"></tbody>
      </table>
      
      <h2>another table</h2>
      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>luogo_intervento</th>
            <th>data_inizio</th>
            <th>descrizione_attivita</th>
          </tr>
        </thead>
        <tbody data-id="sample_dataset_v2"></tbody>
      </table>
      
      <p>end of report</p>
    </div>
  </body>
</html>
```

---

## 4. Application Navigation

The application is a FastAPI-based web interface.

### Accessing the Application

1. Start the server:
   ```bash
   python3 quokka.py
   ```

2. Open your browser at:
   ```
   http://localhost:7489
   ```

3. Log in with your user credentials.

### Searching for Reports

On the reports page, you can:

- **Search by name**: Use the search bar to filter reports by name
- **Filter by category**: Select a category from the list
- **Filter by tag**: Click tags to see only reports with those tags

### Tags and Categories

Reports can be organized using:
- **Category**: A main category for the report (e.g., "Sales", "IT", "HR")
- **Tags**: A list of keywords for flexible searching

**Example:**
```json
{
  "category": "Sales",
  "tags": ["monthly", "2024", "italy", "pdf"]
}
```

This allows you to:
- Filter by category "Sales"
- Search by tag "monthly" or "italy"

### Running a Report

To run a report:

1. From the main menu, click **"Reports"**
2. Find the desired report in the list
3. Click the **"Run"** button (or the report title)

**If the report has parameters:**
- A screen will appear to enter parameter values
- Enter the required values (dates, numbers, etc.)
- Click **"Run Report"**

### Choosing Output Formats

After execution, you can choose the output format:

| Format | Description | Button |
|--------|-------------|--------|
| **HTML** | Open report in browser | "Open HTML" |
| **PDF** | Download report as PDF | "Download PDF" |
| **Excel** | Download data in Excel | "Download Excel" |

**Notes:**
- HTML is displayed directly in the browser
- PDF requires Playwright (separate installation)
- Excel generates a multi-sheet file with each dataset in a separate sheet

---

## 5. Output Formats

### HTML

**Advantages:**
- Immediate browser viewing
- Compatible with all modern browsers
- Customizable styling with CSS

**Usage:**
- Click "Open HTML" or open the link directly
- The report is displayed with all styling applied

### PDF

**Advantages:**
- Universal compatibility
- Print-ready
- Fixed format

**Usage:**
- Click "Download PDF"
- The file is generated and downloaded automatically

**Requirements:**
- Playwright installed on the system
- Dependencies: `playwright`, `asyncio`

### Excel

**Advantages:**
- Structured data in separate sheets
- Editable in Excel
- Easy for further analysis

**Usage:**
- Click "Download Excel"
- Each dataset is inserted in a separate sheet
- Formatted headers and borders applied

**Excel file structure:**
- Sheet 1: First dataset
- Sheet 2: Second dataset
- Etc...

---

## 6. Extensions and Customization

### New Data Providers

To add a new data provider:

1. Create a file in `data_providers/provider_name.py`

2. Implement the `fetch_data()` function:

```python
def fetch_data(dataset_config, dataset_dir):
    """
    Provider implementation.
    
    Args:
        dataset_config: Dataset configuration
        dataset_dir: Dataset directory
    
    Returns:
        { 'columns': [...], 'rows': [...] }
    """
    # Your connection and query code
    # ...
    
    return {
        'columns': ['column1', 'column2'],
        'rows': [
            ['value1', 'value2'],
            ['value3', 'value4']
        ]
    }
```

3. Use the provider in `dataset.json`:
```json
{
  "database": {
    "type": "provider_name"
  }
}
```

### Custom Templates

You can create custom HTML templates:

1. Create an HTML file in the report directory
2. Use `data-id="dataset_name"` syntax for data
3. Specify the template name in `report.json`:

```json
{
  "template": "my_template.html"
}
```

---

## 7. Troubleshooting

### Error: "Report not found"
- Verify that `report.json` exists in the report directory
- Check that the `id` in `report.json` is correct

### Error: "Dataset not found"
- Verify that `dataset.json` exists in the dataset directory
- Check that the `id` in `dataset.json` matches the one used in reports

### Database connection error
- Verify credentials in `dataset.json`
- Check that the database is reachable
- Verify the SQL query syntax

### PDF not generating
- Verify that Playwright is installed: `pip install playwright`
- Run `playwright install chromium`

### Parameters not working
- Verify that parameters in `dataset.json` have correct `id` values
- Use the `${param_id}` syntax in the query (with curly braces)

---

## 📚 Useful Resources

- **Project GitHub**: [quokka-reports](https://github.com/esempio/quokka-reports)
- **License**: AGPL v3
- **Python**: 3.11+
- **FastAPI**: 0.136+

---

## 📝 Changelog

- **v1.0** — Initial documentation version

---

*Documentation generated for Quokka Reports v1.0*
