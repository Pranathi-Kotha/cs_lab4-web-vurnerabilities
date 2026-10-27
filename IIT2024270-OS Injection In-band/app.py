
from flask import Flask, request, render_template
import re
import subprocess

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>OS Command Injection Lab</title>
</head>
<body>
    <h1>OS Command Injection Lab</h1>
    <p>Local coursework demonstration — Windows</p>

    <form method="post">
        <label for="mode">Mode:</label>
        <select name="mode" id="mode">
            <option value="vulnerable"
                {{ 'selected' if mode == 'vulnerable' else '' }}>
                Vulnerable
            </option>
            <option value="secure"
                {{ 'selected' if mode == 'secure' else '' }}>
                Secured
            </option>
        </select>

        <p>
            <label for="host">Hostname:</label>
            <input id="host" name="host"
                   value="{{ host }}" required>
        </p>
        <button type="submit">Run diagnostic</button>
    </form>

    {% if output is not none %}
        <h2>Result</h2>
        <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
"""


def run_diagnostic(host, mode):
    if mode == "vulnerable":
        # INTENTIONALLY VULNERABLE FOR LOCAL COURSEWORK ONLY.
        # User input is concatenated into a shell command.
        command = f"ping -n 1 -w 1000 {host}"

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=4
            )
            return (
                f"VULNERABLE MODE\n"
                f"Exit code: {result.returncode}\n\n"
                f"{result.stdout}\n{result.stderr}"
            )
        except subprocess.TimeoutExpired:
            return "Command timed out."
        except OSError as exc:
            return f"Execution error: {exc}"

    # SECURE MODE: validate input and do not invoke a shell.
    if not re.fullmatch(r"[A-Za-z0-9.-]{1,253}", host):
        return "BLOCKED: invalid hostname. Disallowed characters detected."

    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", host],
            shell=False,
            capture_output=True,
            text=True,
            timeout=4
        )
        return (
            f"SECURED MODE\n"
            f"Exit code: {result.returncode}\n\n"
            f"{result.stdout}\n{result.stderr}"
        )
    except subprocess.TimeoutExpired:
        return "Diagnostic timed out."
    except OSError as exc:
        return f"Execution error: {exc}"


@app.route("/", methods=["GET", "POST"])
def index():
    mode = "vulnerable"
    host = "127.0.0.1"
    output = None

    if request.method == "POST":
        mode = request.form.get("mode", "vulnerable")
        host = request.form.get("host", "").strip()

        if mode not in ("vulnerable", "secure"):
            mode = "secure"
            output = "Invalid mode."
        elif not host:
            output = "Please enter a hostname."
        else:
            output = run_diagnostic(host, mode)

    return render_template(
    "index.html",
    mode=mode,
    host=host,
    output=output
)


if __name__ == "__main__":
    print("Local lab: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
