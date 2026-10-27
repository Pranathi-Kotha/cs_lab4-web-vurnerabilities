# CS Lab 4 Assignment — Web Server Security

**Group:** 19  
**Course:** Cyber Security (IT-30001)  
**Semester:** Autumn Semester 2026  
**Institution:** IIIT Allahabad

## Group Members and Implementations

| Member Name | Roll Number | Category | Variant Implemented |
|---|---|---|---|
| Pranathi Kotha | IIB2024044 | Cross-Site Scripting (XSS) | Reflected XSS |
| Ramkumar | IIT2024270 | OS Command Injection | In-band Command Injection |
| Shravani Math | IIT2024216 | SQL Injection | Authentication Bypass |
| Baby Bhavya | IIT2024271 | Cross-Site Scripting (XSS) | Stored XSS |

## Project Overview

This repository contains the group's web security vulnerability demonstrations and mitigations. Each implementation demonstrates an assigned vulnerability, identifies its root cause, presents a controlled proof of concept, and implements a mitigation to prevent the demonstrated attack.

## Directory Structure

```text
Web-Server-Security/
├── README.md
│
├── IIB2024044-Reflected XSS/
│   ├── app.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       └── index.html
│
├── IIT2024270-OS Injection In-band/
│   ├── app.py
│   ├── requirements.txt
│   ├── tests.py
│   ├── static/
│   ├── templates/
│   └── evidence/
│
├── IIT2024216-SQL Injection/
│   ├── server.js
│   ├── package.json
│   ├── package-lock.json
│   └── public/
│       └── index.html
│
└── IIT2024271-Stored XSS/
    ├── app.py
    ├── requirements.txt
    ├── static/
    │   └── style.css
    └── templates/
        ├── index.html
        └── results.html
```

## 1. Reflected Cross-Site Scripting (XSS)

**Implemented by:** Pranathi Kotha (IIB2024044)  
**Directory:** `IIB2024044-Reflected XSS/`

This Flask-based student portal demonstrates Reflected XSS through user input reflected into a webpage.

- **Vulnerable implementation:** Uses Jinja2's `{{ query|safe }}`, bypassing normal HTML escaping for the value.
- **Demonstration:** A controlled JavaScript payload demonstrates script execution and webpage manipulation.
- **Root cause:** Untrusted input is rendered without appropriate output escaping.
- **Mitigation:** Uses `{{ query }}` with Jinja2 automatic escaping enabled.
- **Verification:** The same payload is tested against the vulnerable and secured versions.

## 2. OS Command Injection — In-band

**Implemented by:** Ramkumar (IIT2024270)  
**Directory:** `IIT2024270-OS Injection In-band/`

This Flask application demonstrates OS Command Injection through a hostname diagnostic feature using the Windows `ping` command.

- **Vulnerable implementation:** Constructs a shell command using user input and executes it with `shell=True`.
- **Demonstration:** A controlled payload demonstrates additional command execution, with the resulting output returned in the web response.
- **Root cause:** User input is incorporated into a shell command without safe separation.
- **Mitigation:** Uses hostname allow-list validation and argument-list execution with `shell=False`.
- **Verification:** Tests check the vulnerable and secure execution paths. The project includes automated tests and an `evidence/` directory.

## 3. SQL Injection — Authentication Bypass

**Implemented by:** Shravani Math (IIT2024216)  
**Directory:** `IIT2024216-SQL Injection/`

This Node.js and Express application uses SQLite to demonstrate authentication bypass caused by unsafe SQL query construction.

- **Vulnerable implementation:** Concatenates user-supplied credentials directly into an SQL query.
- **Demonstration:** Controlled login input demonstrates the potential to bypass authentication.
- **Root cause:** User input can alter the structure or logic of the SQL query.
- **Mitigation:** Uses parameterized SQL queries to separate SQL instructions from user-supplied values.
- **Verification:** The same injection input is tested after the fix, and legitimate dummy credentials are used to verify normal login functionality.

## 4. Stored Cross-Site Scripting (XSS)

**Implemented by:** Baby Bhavya (IIT2024271)  
**Directory:** `IIT2024271-Stored XSS/`

This Flask application uses SQLite to store user-submitted comments and demonstrate Stored XSS.

- **Vulnerable implementation:** Uses Jinja2's `safe` filter to render stored comments without normal output escaping.
- **Demonstration:** A harmless HTML test input demonstrates unsafe rendering of stored content.
- **Root cause:** Stored user input is treated as trusted HTML when displayed.
- **Mitigation:** Uses normal Jinja2 template rendering with automatic escaping enabled, avoiding the `safe` filter on untrusted content.
- **Verification:** The same HTML input is submitted to the vulnerable and secure pages to compare the results.

## Other Mitigation Techniques

In addition to their implemented mitigation, group members should understand the alternative techniques covered in the course slides.

- **SQL Injection:** Parameterized queries, allow-list input validation, least-privilege database accounts, and safe error handling.
- **OS Command Injection:** Avoiding the shell, argument-vector execution, allow-list validation, and least privilege.
- **XSS:** Context-aware output encoding, framework auto-escaping, HTML sanitization, Content Security Policy (CSP), HttpOnly cookies, and safe DOM sinks.
- **CSRF:** Anti-CSRF tokens, SameSite cookies, re-authentication for sensitive actions, and avoiding state-changing GET requests.

## Security and Testing

Each project should be tested in a controlled local environment by demonstrating the vulnerable behavior, identifying the root cause, applying the implemented mitigation, and verifying that the same test input no longer produces the demonstrated attack.

All vulnerable applications are intended for authorized coursework only and must not be deployed publicly. No passwords, API keys, or other secrets should be committed to the repository.

## Conclusion

This repository demonstrates web security vulnerabilities, their root causes, and practical mitigation techniques. The projects highlight the importance of output escaping, safe command execution, and parameterized database queries in developing secure web applications.