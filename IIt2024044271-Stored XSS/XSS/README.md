# Stored XSS Security Lab

## Overview

Stored XSS Security Lab is an educational web application built with Python and Flask. It demonstrates Stored Cross-Site Scripting (XSS) and how output escaping helps prevent it.

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2

## Features

- Styled homepage
- Comment submission form
- SQLite database for storing comments
- Vulnerable XSS demonstration
- Secure output-escaping demonstration
- Comparison of unsafe and safe output rendering

## Project Structure

```text
Stored_XSS_Project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── index.html
│   └── results.html
└── static/
    └── style.css
```

## Installation and Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000/

## Demonstrations

### Vulnerable Demo

Visit `/vulnerable` to explore the risks of rendering stored user input without appropriate escaping.

### Secure Demo

Visit `/secure` to observe how output escaping displays user input as text instead of interpreting it as HTML or JavaScript.

## Security Note

This project is intended for educational use in a controlled local environment. Do not deploy the intentionally vulnerable demonstration publicly.

Production applications should use context-appropriate output encoding and avoid treating untrusted user input as safe HTML.

## Author

Add your name here.

## License

For educational and demonstration purposes.