# 🦘 Quokka Reports - Documentazione Utente

> **Trasforma i tuoi dati in report bellissimi.**

Questo documento fornisce una guida completa all'utilizzo di Quokka Reports, una piattaforma di reporting open-source che trasforma query SQL e fonti di dati esterni in report HTML, PDF ed Excel elegantemente formattati.

---

## 📑 Indice

- [Introduzione](#-introduzione)
- [Architettura](#-architettura)
- [1. Gestione Utenti](#1-gestione-utenti)
  - [Menu principale di management.py](#menu-principale-di-managementpy)
  - [Operazioni sugli utenti](#operazioni-sugli-utenti)
  - [Esempi pratici](#esempi-pratici)
- [2. Creazione Dataset](#2-creazione-dataset)
  - [Struttura di un dataset](#struttura-di-un-dataset)
  - [Tipi di database e providers](#tipi-di-database-e-providers)
  - [Parametri dei dataset](#parametri-dei-dataset)
  - [Esempi pratici](#esempi-pratici-1)
- [3. Creazione Report](#3-creazione-report)
  - [Struttura di un report](#struttura-di-un-report)
  - [File del report: report.json, report.html, report.css](#file-del-report-reportjson-reporthtml-reportcss)
  - [Relazione con i dataset](#relazione-con-i-dataset)
  - [Esempi pratici](#esempi-pratici-2)
- [4. Navigazione nell'Applicazione](#4-navigazione-nellapplicazione)
  - [Accesso all'applicazione](#accesso-allapplicazione)
  - [Ricerca di report](#ricerca-di-report)
  - [Tags e categorie](#tags-e-categorie)
  - [Esecuzione di un report](#esecuzione-di-un-report)
  - [Scelta dei formati di output](#scelta-dei-formati-di-output)
- [5. Formati di Output](#5-formati-di-output)
  - [HTML](#html)
  - [PDF](#pdf)
  - [Excel](#excel)
- [6. Estensioni e Customizzazione](#6-estensioni-e-customizzazione)
  - [Nuovi data providers](#nuovi-data-providers)
  - [Template personalizzati](#template-personalizzati)
- [7. Risoluzione dei Problemi](#7-risoluzione-dei-problemi)
- [Risorse utili](#risorse-utili)

---

## 🚀 Introduzione

Quokka Reports è una piattaforma di reporting modulare progettata per separare la fase di acquisizione dei dati da quella di presentazione.

### Principi fondamentali

- **Separazione dei dati dalla presentazione**: I dataset gestiscono l'acquisizione dei dati, i report gestiscono la presentazione.
- **Riutilizzo dei dataset**: Un dataset può essere utilizzato da più report.
- **Template standard**: I report usano HTML e CSS standard, senza bisogno di linguaggi di templating speciali.
- **Provider pluggabili**: Supporto per PostgreSQL, Graylog e providers personalizzati.

### Panoramica del flusso di lavoro

```
1. Gestione Utenti → 2. Creazione Dataset → 3. Creazione Report → 4. Esecuzione
```

---

## 🏗 Architettura

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

## 1. Gestione Utenti

Gli utenti sono gestiti tramite lo script **`management.py`**, che fornisce un'interfaccia interattiva a riga di comando per gestire il file `users.json`.

### Menu principale di management.py

Esegui lo script con:
```bash
python3 management.py
```

Il menu principale offre queste opzioni:

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

### Operazioni sugli utenti

#### 1. List all users (Elencare tutti gli utenti)
Mostra una tabella con:
- ID
- Nome
- Username
- Email
- Status (Active/Inactive)

#### 2. Show user details (Visualizzare i dettagli di un utente)
Inserisci l'ID dell'utente per vedere tutti i suoi dati.

#### 3. Change user password (Cambiare la password)
Inserisci l'ID dell'utente, poi inserisci la nuova password due volte per conferma.

#### 4. Update user data (Aggiornare i dati di un utente)
Puoi modificare:
- Nome
- Username
- Email
- Group (gruppo di appartenenza)
- Locale (lingua, es. "it" o "en")

#### 5. Deactivate user (Disattivare un utente)
Disattiva un utente senza eliminarlo. Gli utenti disattivati non possono accedere all'applicazione.

#### 6. Create new user (Creare un nuovo utente)
Richiede:
- Nome
- Username (unico)
- Email (valida)
- Password (vista come asterischi)
- Group (opzionale)
- Locale (opzionale)

#### 7. Delete user (Eliminare un utente)
Elimina permanentemente l'utente dal sistema.

#### 8. Save changes (Salvare le modifiche)
Salva tutte le modifiche apportate nel file `users.json`.

### Esempi pratici

**Esempio 1: Creare un nuovo utente**
```bash
$ python3 management.py
========================================
   USER MANAGEMENT - MAIN MENU
========================================
...
6. Create new user
...

Seleziona: 6

Nome: Mario Rossi
Username: m.rossi
Email: mario.rossi@azienda.it
New password: ********
Confirm new password: ********
Group [default]: it_department
Locale [default]: it

Utente creato con successo!
```

**Esempio 2: Cambiare la password**
```bash
Seleziona: 3

Enter user ID: 42
Changing password for: Mario Rossi (m.rossi)
New password: ********
Confirm new password: ********

Password updated successfully!
```

**Esempio 3: Disattivare un utente**
```bash
Seleziona: 5

Enter user ID: 42
User m.rossi has been deactivated.
```

---

## 2. Creazione Dataset

Un **dataset** definisce come recuperare i dati da una fonte (database, API, ecc.) e come gestire i parametri per filtrare i risultati.

### Struttura di un dataset

Un dataset è una directory all'interno di `datasets/` contenente:
- `dataset.json` — Configurazione principale

**Esempio struttura:**
```
datasets/
├── example01.ds/
│   └── dataset.json
├── sample_v1.ds/
│   └── dataset.json
└── sample_v2.ds/
    └── dataset.json
```

### File dataset.json

Il file `dataset.json` contiene:

```json
{
  "id": "nome_identificativo_univoco",
  "name": "Nome Visualizzato del Dataset",
  "description": "Descrizione del dataset",
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "nome_database",
    "username": "utente",
    "password": "password"
  },
  "params": [
    { "id": "from_date", "type": "date", "name": "Data inizio" },
    { "id": "to_date", "type": "date", "name": "Data fine" }
  ],
  "query": "SELECT * FROM tabella WHERE data >= ${from_date} AND data <= ${to_date}"
}
```

#### Parametri obbligatori:

| Parametro | Descrizione |
|-----------|-------------|
| `id` | Identificativo univoco del dataset (usato nei report) |
| `name` | Nome visualizzato |
| `database` | Configurazione del database |
| `query` | Query SQL (può iniziare con `@` per leggere da file) |

#### Tipi di parametri supportati:
- `date` — Data
- `string` — Testo
- `number` — Numero

### Tipi di database e providers

I **data providers** sono moduli Python in `data_providers/` che implementano la funzione `fetch_data()`.

**Providers disponibili:**

| Provider | File | Descrizione |
|----------|------|-------------|
| PostgreSQL | `postgresql.py` | Connessione a database PostgreSQL |
| Graylog | `graylog.py` | Interrogazione Graylog API |
| Custom | `custom.py` | Provider personalizzati |

#### Provider PostgreSQL

Configurazione nel `dataset.json`:
```json
{
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "nome_database",
    "username": "utente",
    "password": "password"
  },
  "query": "SELECT * FROM tabella"
}
```

#### Provider Graylog

Configurazione nel `dataset.json`:
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

### Parametri dei dataset

I **parametri** permettono di rendere le query dinamiche:

```json
{
  "params": [
    { 
      "id": "from_date", 
      "type": "date", 
      "name": "Data inizio" 
    },
    { 
      "id": "to_date", 
      "type": "date", 
      "name": "Data fine" 
    }
  ]
}
```

Nella query, i parametri si usano con la sintassi `${param_id}`:

```sql
SELECT * FROM intervento 
WHERE data_inizio >= ${from_date} 
  AND data_inizio <= ${to_date}
```

### Esempi pratici

#### Esempio 1: Dataset PostgreSQL con parametri

File: `datasets/sample_v1.ds/dataset.json`
```json
{
  "id": "sample_dataset_v1",
  "name": "Interventi per periodo",
  "description": "Estrae gli interventi di manutenzione in un periodo",
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "cronoprogramma",
    "username": "cronos",
    "password": "cronos"
  },
  "params": [
    { "id": "from_date", "type": "date", "name": "Data inizio" },
    { "id": "to_date", "type": "date", "name": "Data fine" }
  ],
  "query": "SELECT id, luogo_intervento, data_inizio::date as data_inizio, descrizione_attivita from intervento where data_inizio >= ${from_date} and data_inizio <= ${to_date}"
}
```

#### Esempio 2: Dataset Graylog per log analysis

File: `datasets/example02.ds/dataset.json`
```json
{
  "id": "example_dataset_02",
  "name": "Log recenti",
  "description": "Estrae i log recenti da Graylog",
  "database": {
    "type": "graylog",
    "url": "http://graylog.example.com:8080",
    "token": "your_graylog_token"
  },
  "params": [
    { "id": "from", "type": "datetime", "name": "Da data/ora" },
    { "id": "to", "type": "datetime", "name": "A data/ora" }
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

## 3. Creazione Report

Un **report** combina uno o più dataset in un'unica visualizzazione con stile HTML/CSS.

### Struttura di un report

Un report è una directory all'interno di `reports/` contenente:

```
reports/
├── example_01.rp/
│   ├── report.json       ← Configurazione principale
│   ├── report.html       ← Template HTML
│   ├── report.css        ← Stili CSS (opzionale)
│   └── quokka-reports.jpg ← Risorse (immagini, ecc.)
└── sample_v1.rp/
    ├── report.json
    ├── report.html
    ├── report.css
    └── report2.css
```

### File del report: report.json, report.html, report.css

#### report.json

File di configurazione principale:

```json
{
  "id": "report_sample_v1",
  "name": "Report di Esempio 01",
  "description": "Questo report dimostra il funzionamento del sistema",
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

**Parametri:**

| Parametro | Obbligatorio | Descrizione |
|-----------|--------------|-------------|
| `id` | ✅ | Identificativo univoco del report |
| `name` | ✅ | Nome visualizzato |
| `description` | ✅ | Descrizione del report |
| `category` | ❌ | Categoria per organizzazione (es. "Vendite", "IT", "HR") |
| `tags` | ❌ | Array di tag per ricerca |
| `datasets` | ✅ | Array di dataset da utilizzare |
| `template` | ❌ | Nome del file HTML template (default: "report.html") |
| `active` | ❌ | `true`/`false` per abilitare/disabilitare |

#### report.html

Template HTML standard con placeholders per i dataset:

```html
<html>
  <head>
    <link rel="stylesheet" href="report.css" />
  </head>
  <body>
    <h1>Titolo del Report</h1>
    
    <table>
      <thead>
        <tr><th>Nome</th><th>Valore</th></tr>
      </thead>
      <tbody data-id="sample_dataset_v1"></tbody>
    </table>
    
    <h2>Altra tabella</h2>
    <table>
      <thead>
        <tr><th>ID</th><th>Dato</th></tr>
      </thead>
      <tbody data-id="sample_dataset_v2"></tbody>
    </table>
  </body>
</html>
```

**Importante:**
- Usa `data-id="nome_dataset"` nei tag `<tbody>` per identificare dove inserire i dati
- I percorsi CSS/JS/immagini sono relativi alla directory del report

#### report.css

File CSS opzionale per personalizzare lo stile del report.

### Relazione con i dataset

Un report fa riferimento ai dataset tramite il loro `id`:

```json
{
  "datasets": [
    { "id": "sample_dataset_v1" },
    { "id": "sample_dataset_v2" }
  ]
}
```

Il sistema:
1. Legge i dataset da `dataset.json`
2. Recupera i parametri necessari
3. Esegue le query
4. Inserisce i risultati nel template HTML nei punti marcati con `data-id`

### Esempi pratici

#### Esempio 1: Report semplice con un dataset

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
    <h1>Esempio Report</h1>
    <table>
      <thead>
        <tr><th>Nome</th><th>Valore</th></tr>
      </thead>
      <tbody data-id="example_dataset_01"></tbody>
    </table>
  </body>
</html>
```

#### Esempio 2: Report multi-dataset con più tabelle

File: `reports/sample_v1.rp/report.json`
```json
{
  "id": "report_sample_v1",
  "name": "Report di Esempio 01",
  "description": "Questo report dimostra il funzionamento del sistema",
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
      <h1>Titolo di esempio</h1>
      
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
      
      <h2>altra tabella</h2>
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
      
      <p>fine del report</p>
    </div>
  </body>
</html>
```

---

## 4. Navigazione nell'Applicazione

L'applicazione è un'interfaccia web basata su FastAPI.

### Accesso all'applicazione

1. Avvia il server:
   ```bash
   python3 quokka.py
   ```

2. Apri il browser all'indirizzo:
   ```
   http://localhost:7489
   ```

3. Accedi con le credenziali utente.

### Ricerca di report

Nella pagina dei report, puoi:

- **Cercare per nome**: Usa la barra di ricerca per filtrare i report per nome
- **Filtrare per categoria**: Seleziona una categoria dalla lista
- **Filtrare per tag**: Clicca sui tag per vedere solo i report con quei tag

### Tags e categorie

I report possono essere organizzati usando:
- **Category**: Una categoria principale per il report (es. "Vendite", "IT", "HR")
- **Tags**: Una lista di parole chiave per ricerca flessibile

**Esempio:**
```json
{
  "category": "Vendite",
  "tags": ["mensile", "2024", "italia", "pdf"]
}
```

Questo permette di:
- Filtrare per categoria "Vendite"
- Cercare per tag "mensile" oppure "italia"

### Esecuzione di un report

Per eseguire un report:

1. Dal menu principale, clicca su **"Report"**
2. Trova il report desiderato nella lista
3. Clicca sul pulsante **"Esegui"** (o il titolo del report)

**Se il report ha parametri:**
- Verrà mostrata una schermata per inserire i valori dei parametri
- Inserisci i valori richiesti (date, numeri, ecc.)
- Clicca su **"Esegui Report"**

### Scelta dei formati di output

Dopo l'esecuzione, puoi scegliere il formato di output:

| Format | Descrizione | Pulsante |
|--------|-------------|----------|
| **HTML** | Apri il report nel browser | "Apri HTML" |
| **PDF** | Scarica il report come PDF | "Scarica PDF" |
| **Excel** | Scarica i dati in Excel | "Scarica Excel" |

**Note:**
- HTML è visualizzato direttamente nel browser
- PDF richiede Playwright (installazione separata)
- Excel genera un file multi-sheet con ogni dataset in un foglio separato

---

## 5. Formati di Output

### HTML

**Vantaggi:**
- Visualizzazione immediata nel browser
- Compatibile con tutti i browser moderni
- Stile personalizzabile con CSS

**Utilizzo:**
- Clicca "Apri HTML" o apri direttamente il link
- Il report viene visualizzato con tutto lo stile applicato

### PDF

**Vantaggi:**
- Formato compatibile ovunque
- Print-ready
- Formato fisso

**Utilizzo:**
- Clicca "Scarica PDF"
- Il file viene generato e scaricato automaticamente

**Requisiti:**
- Playwright installato nel sistema
- Dipendenze: `playwright`, `asyncio`

### Excel

**Vantaggi:**
- Dati strutturati in fogli separati
- Modificabili in Excel
- Facile per analisi successive

**Utilizzo:**
- Clicca "Scarica Excel"
- Ogni dataset viene inserito in un foglio separato
- Header formattati e bordi applicati

**Struttura del file Excel:**
- Sheet 1: Primo dataset
- Sheet 2: Secondo dataset
- Etc...

---

## 6. Estensioni e Customizzazione

### Nuovi data providers

Per aggiungere un nuovo data provider:

1. Crea un file in `data_providers/nome_provider.py`

2. Implementa la funzione `fetch_data()`:

```python
def fetch_data(dataset_config, dataset_dir):
    """
    Implementazione del provider.
    
    Args:
        dataset_config: Configurazione del dataset
        dataset_dir: Directory del dataset
    
    Returns:
        { 'columns': [...], 'rows': [...] }
    """
    # Tuo codice di connessione e query
    # ...
    
    return {
        'columns': ['colonna1', 'colonna2'],
        'rows': [
            ['valore1', 'valore2'],
            ['valore3', 'valore4']
        ]
    }
```

3. Usa il provider nel `dataset.json`:
```json
{
  "database": {
    "type": "nome_provider"
  }
}
```

### Template personalizzati

Puoi creare template HTML personalizzati:

1. Crea un file HTML nella directory del report
2. Usa la sintassi `data-id="nome_dataset"` per i dati
3. Specifica il nome del template in `report.json`:

```json
{
  "template": "mio_template.html"
}
```

---

## 7. Risoluzione dei Problemi

### Errore: "Report not found"
- Verifica che `report.json` esista nella directory del report
- Controlla che l'`id` in `report.json` sia corretto

### Errore: "Dataset not found"
- Verifica che `dataset.json` esista nella directory del dataset
- Controlla che l'`id` in `dataset.json` corrisponda a quello usato nei report

### Errore di connessione database
- Verifica le credenziali in `dataset.json`
- Controlla che il database sia raggiungibile
- Verifica la syntax della query SQL

### PDF non genera
- Verifica che Playwright sia installato: `pip install playwright`
- Esegui `playwright install chromium`

### Parametri non funzionano
- Verifica che i parametri nel `dataset.json` abbiano `id` corretti
- Usa la sintassi `${param_id}` nella query (con le parentesi graffe)

---

## 📚 Risorse utili

- **Project GitHub**: [quokka-reports](https://github.com/esempio/quokka-reports)
- **Licenza**: AGPL v3
- **Python**: 3.11+
- **FastAPI**: 0.136+

---

## 📝 Changelog

- **v1.0** — Versione iniziale della documentazione

---

*Documentazione generata per Quokka Reports v1.0*
