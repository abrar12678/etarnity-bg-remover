# Etarnity Background Remover

A Flask-based web tool designed to process signature images by removing white backgrounds, making them transparent, and resizing them for professional use. Deployed and accessible as a live web application.

## Overview

Etarnity Background Remover is a lightweight yet powerful image processing tool built with Python and Flask. It allows users to upload signature images, automatically removes the white background to create transparent PNGs, resizes them to a standard dimension, and provides a quick download option. The tool is ideal for professionals who need clean, transparent signatures for documents, forms, and digital workflows.

## Tech Stack

| Category | Technology |
|----------|-----------|
| Backend | Flask (Python) |
| Image Processing | Pillow (PIL) |
| Styling | Tailwind CSS |
| Frontend | HTML, JavaScript |
| Deployment | Gunicorn, Vercel |

## Core Features

- **White Background Removal** — Automatically detects and removes white backgrounds from uploaded images, producing clean transparent PNGs
- **Signature Resizing** — Resizes processed signatures to a standard, document-friendly dimension
- **Real-time Preview** — Instantly preview the processed transparent signature before downloading
- **One-Click Download** — Download the processed transparent PNG with a single click
- **Clean & Simple UI** — Minimalist interface built with Tailwind CSS for a distraction-free experience
- **Lightweight & Fast** — Server-side processing with Pillow ensures quick results

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `Flask` | 3.0.3 | Web framework for routing and request handling |
| `Pillow` | 10.4.0 | Image processing (background removal, resizing) |
| `requests` | 2.32.3 | HTTP library for external API calls |
| `gunicorn` | 22.0.0 | Production WSGI HTTP server |

## Getting Started

### Prerequisites

- Python 3.9+ installed
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/abrar12678/etarnity-bg-remover.git
cd etarnity-bg-remover

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
python app.py
```

The application will start running at [http://127.0.0.1:5000](http://127.0.0.1:5000). Open it in your browser to use the tool.

### Deploy for Production

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Live Demo

Try the tool live: [etarnity-bg-remover.vercel.app](https://etarnity-bg-remover.vercel.app](https://etarnity-bg-remover.onrender.com))

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pillow Documentation](https://pillow.readthedocs.io/)

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.0.3-000000?style=flat-square&logo=flask" alt="Flask" />
  <img src="https://img.shields.io/badge/Pillow-10.4.0-8B5CF6?style=flat-square" alt="Pillow" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-CSS-06B6D4?style=flat-square&logo=tailwindcss" alt="Tailwind CSS" />
</p>
