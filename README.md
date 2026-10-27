# CS Lab 4 Assignment — Web Server Security

**Group:** 19  
**Course:** Cyber Security (IT-30001), Autumn Semester 2026

## Group Members and Implementations

| Member Name | Roll Number | Category | Variant Implemented |
|---|---|---|---|
| Pranathi Kotha | IIB2024044 | Cross-Site Scripting (XSS) | Reflected XSS |
| TODO | IIT2024270 | OS Command Injection | In-band Command Injection |
| TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO |

## Project Overview

This repository contains the group's web security vulnerability demonstrations and mitigations. Each implementation demonstrates the assigned vulnerability, identifies its root cause, presents a proof of concept, and verifies an implemented mitigation.

## Directory Structure

```text
Web-Server-Security/
├── README.md
├── IIB2024044-Reflected XSS/
│   ├── app.py
│   ├── static/
│   └── templates/
├── IIT2024270-OS Injection In-band/
│   ├── app.py
│   ├── requirements.txt
│   ├── tests.py
│   ├── static/
│   ├── templates/
│   └── evidence/
├── MEMBER3-VARIANT/
└── MEMBER4-VARIANT/
```

## 1. Reflected Cross-Site Scripting (XSS)

**Implemented by:** Pranathi Kotha (IIB2024044)  
**Directory:** `IIB2024044-Reflected XSS/`

This Flask-based student portal demonstrates Reflected XSS through user-supplied input reflected into the webpage.

- **Vulnerable implementation:** Uses Jinja2's `{{ query|safe }}` to render input without automatic HTML escaping.
- **Demonstration:** A JavaScript payload demonstrates script execution and webpage manipulation.
- **Mitigation:** Uses `{{ query }}` to enable Jinja2 automatic HTML escaping.
- **Verification:** The same payload is executed in the vulnerable version and displayed as text in the secured version.

## 2. OS Command Injection — In-band

**Implemented by:** TODO (IIT2024270)  
**Directory:** `IIT2024270-OS Injection In-band/`

This Flask application demonstrates OS Command Injection through a hostname diagnostic feature using the Windows `ping` command.

- **Vulnerable implementation:** Constructs a shell command using user input and executes it with `shell=True`.
- **Demonstration:** A controlled payload demonstrates command execution, with the resulting output returned in the web response.
- **Mitigation:** Uses hostname allow-list validation and argument-list execution with `shell=False`.
- **Verification:** The same payload is rejected in Secure Mode. Three automated tests verify the vulnerable and secure execution paths.
- **Evidence:** The `evidence/` directory contains screenshots of normal operation, exploitation, mitigation, tests, and relevant code.

## 3. Third Vulnerability Implementation

**Member:** TODO (TODO)  
**Category:** TODO  
**Variant:** TODO  
**Directory:** TODO  
**Vulnerability, demonstration, mitigation, and verification:** TODO

## 4. Fourth Vulnerability Implementation

**Member:** TODO (TODO)  
**Category:** TODO  
**Variant:** TODO  
**Directory:** TODO  
**Vulnerability, demonstration, mitigation, and verification:** TODO

## Testing and Security

Each implementation is demonstrated in a controlled environment, with the vulnerable code path and root cause identified, a proof of concept presented, and the implemented mitigation tested.

All vulnerable applications are intended for authorized local coursework only and must not be exposed publicly or deployed in production. No passwords, API keys, or other secrets should be committed to the repository.

## Conclusion

This repository demonstrates web security vulnerabilities, their exploitation in controlled environments, and practical mitigations to reduce the associated risks.
