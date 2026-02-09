# 🧪 Chemical Equipment Parameter Visualizer
## FOSSEE Semester-Long Internship 2026 – Screening Task
A full-stack application that enables users to upload, analyze, and visualize chemical equipment data across web and desktop platforms.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage Guide](#usage-guide)

---

## Overview

The Chemical Equipment Parameter Visualizer is a unified platform with three components:

1. **Django REST Backend** — Handles authentication, CSV processing, PDF generation, and history management
2. **React Web Frontend** — Interactive dashboard with real-time charts and file uploads
3. **PyQt5 Desktop Frontend** — Native desktop application with embedded visualizations

All three components share a single Django API backend, ensuring data consistency across platforms.

---

## Features

### Core Functionality
- **CSV File Upload** — Upload chemical equipment data files
- **Automatic Analysis** — Parse data and calculate statistics:
  - Total equipment count
  - Average flowrate, pressure, temperature
  - Equipment type distribution
- **Data Visualization** — Bar charts, pie charts, and data tables
- **CSV Data Viewing** — View uploaded CSV files in interactive tables
- **PDF Report Generation** — Generate and download analysis reports
- **History Tracking** — View and manage last 5 uploads with options to view CSV or download PDF
- **User Authentication** — Secure JWT-based login and registration

### Web Dashboard (React)
- Interactive charts using Chart.js
- Responsive grid layout
- Equipment data table preview
- History sidebar with action buttons (View CSV & Download PDF)
- Distribution pie chart
- CSV modal viewer — View uploaded CSV files in modal tables

### Desktop Application (PyQt5)
- Native desktop UI with modern styling
- Embedded Matplotlib charts
- File browser integration
- Real-time stats cards with hover effects
- Clickable stat cards for detailed distribution views
- Context menu on history items — Click to view CSV or download PDF

### Backend API (Django)
- RESTful endpoints for all operations
- Token-based JWT authentication
- Pandas-powered data analysis
- PDF report generation with xhtml2pdf
- SQLite database for persistence

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9+, Django 4.0+, Django REST Framework |
| **Database** | SQLite3 |
| **Data Processing** | Pandas, NumPy |
| **Web Frontend** | React.js, Chart.js, Axios, CSS3 |
| **Desktop Frontend** | PyQt5, Matplotlib, Requests |
| **Security** | JWT (Simple JWT) |
| **Reports** | xhtml2pdf |

---

## Project Structure

```
FOSSEE_Project/
├── backend/                          # Django backend
│   ├── manage.py
│   ├── db.sqlite3
│   ├── chemical_visualizer/          # Main project settings
│   │   ├── settings.py
│   │   └── urls.py
│   ├── core/                         # Core app with business logic
│   │   ├── models.py                 # EquipmentHistory model
│   │   ├── views.py                  # API endpoints
│   │   ├── serializers.py            # DRF serializers
│   │   ├── utils.py                  # Data processing helpers
│   │   └── migrations/
│   └── uploads/                      # Uploaded CSV files storage
│
├── web_frontend/                     # React frontend
│   ├── package.json
│   ├── src/
│   │   ├── App.js                    # Main component
│   │   ├── App.css                   # Styling
│   │   ├── api.js                    # Backend API calls
│   │   └── AppLogic.js               # State management
│   └── public/
│
├── desktop_frontend/                 # PyQt5 desktop app
│   ├── main.py                       # Entry point
│   ├── authentication.py             # Login/Register UI
│   ├── dashboard.py                  # Main dashboard
│   ├── api.py                        # Backend API client
│   ├── helper.py                     # UI helpers
│   └── reports/                      # Downloaded PDFs storage
│
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── sample_equipment_data.csv         # Example CSV file
```

---

## Installation

### Prerequisites
- Python 3.9+
- Node.js 14+ (for web frontend)
- pip / npm package managers

### Backend Setup

```bash
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Or on macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate
```

### Web Frontend Setup

```bash
cd web_frontend

# Install dependencies
npm install
```

### Desktop Frontend Setup

```bash
cd desktop_frontend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Or on macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Dependency Structure
Dependencies are kept separate by component for cleaner environments:
- **`backend/requirements.txt`** — Django, DRF, data processing (pandas, numpy), PDF generation
- **`desktop_frontend/requirements.txt`** — PyQt5, Matplotlib, and API client dependencies
- **`web_frontend/package.json`** — React and npm dependencies

---

## Running the Application

You need **three separate terminals** to run all components:

### Terminal 1: Django Backend

```bash
cd backend
# Activate venv first
python manage.py runserver
```

Backend starts at `http://127.0.0.1:8000`

### Terminal 2: React Web Frontend

```bash
cd web_frontend
npm start
```

Web app opens at `http://localhost:3000`

### Terminal 3: PyQt5 Desktop Application

```bash
cd desktop_frontend
# Activate venv first
python main.py
```

Desktop app launches as a native window.

---

## API Endpoints

All endpoints require JWT authentication (except registration and login).

### Authentication
- **POST** `/api/register/` — Register new user
- **POST** `/api/token/` — Get JWT access token

### Equipment Operations
- **POST** `/api/equipment/` — Upload CSV file for analysis
- **GET** `/api/equipment/` — Retrieve upload history (last 5)

### Reports & Data Download
- **GET** `/api/report/<id>/` — Download PDF report for upload
- **GET** `/api/csv/<id>/` — Download original CSV file

---

## Usage Guide

### Uploading Data

1. Log in with username and password
2. Click "Browse" and select a CSV file with columns:
   - `type` (equipment type)
   - `flowrate` (numeric)
   - `pressure` (numeric)
   - `temperature` (numeric)
3. Click "Analyze CSV File"
4. View results in the dashboard

### Viewing Results

- **Summary Cards** — Total count and average values
- **Bar Chart** — Equipment type distribution
- **Data Table** — Preview of first 10 rows
- **History Management** — Recent uploads with dual action buttons:
  - **📊 View CSV** — Opens CSV file in modal/dialog table viewer
  - **📑 PDF** — Downloads analysis report as PDF

### Desktop Features

- Right-click history items to access **context menu**:
  - **📊 View CSV** — Display CSV data in popup table
  - **📑 Download PDF** — Download report to `desktop_frontend/reports/`
- Click **Total stat card** (with ★) to view pie chart
- Hover over cards for interactive effects
- Data syncs across both platforms

### Web Features

- Click **📊 View CSV** to preview uploaded data in modal table
- Click **📑 PDF** to download report
- Responsive design works on all screen sizes

---

## Notes

- **SQLite3 Database** — Stores all user data locally  
- **File Storage** — CSV uploads stored in `backend/uploads/`
- **Desktop Reports** — PDF reports downloaded via PyQt5 saved to `desktop_frontend/reports/`
- **History Limit** — App keeps only last 5 uploads per user (older files auto-deleted)
- **Authentication** — JWT tokens used for session management with 15-minute expiration
- **CSV Viewing** — Both web (modal) and desktop (popup table) support inline CSV data viewing without requiring file download
- **Cross-Platform** — Same API backend serves both web React frontend and desktop PyQt5 frontend

---

## 🧠 Key Learnings & Challenges
- Hybrid Architecture: Gained Experience in building a unified Django Rest API that serves two completely different frontend environments simultaneously.
- Asynchronous UI Management: Solved challenges regarding thread safety, ensuring that the dashboard remains responsive while it waits for the API data.
State Consistency: Implemented Json Web tokens authentication across two platforms to ensure a secure and smooth user experience.

---

## License

This project is licensed under the **MIT License**. 

This application was developed as part of the **FOSSEE Semester-Long Internship 2026 Screening Task** for the "Chemical Equipment Parameter Visualizer" project. 