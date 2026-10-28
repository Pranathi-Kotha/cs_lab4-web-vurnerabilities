
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
    make_response,
)
from functools import wraps
import secrets
import hmac
import os

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "local-csrf-classroom-demo-change-before-deployment"
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # Local HTTP demonstration only
)

# One shared fictional profile for both modes.
INITIAL_PROFILE = {
    "name": "Demo Customer",
    "email": "customer@example.com",
    "phone": "+91 90000 00000",
    "address": "12 College Road, Prayagraj",
}

customer = INITIAL_PROFILE.copy()


def get_csrf_token():
    """Create a session-bound token when one does not exist."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


@app.context_processor
def inject_csrf_token():
    return {"csrf_token": get_csrf_token}


def require_login(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def valid_csrf_token():
    submitted = request.form.get("csrf_token", "")
    expected = session.get("csrf_token", "")
    return bool(submitted and expected and hmac.compare_digest(
        submitted, expected
    ))


@app.route("/")
def index():
    if session.get("logged_in"):
        return redirect(url_for("profile"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == "customer" and password == "demo123":
            session.clear()
            session["logged_in"] = True
            session["mode"] = "vulnerable"
            get_csrf_token()
            return redirect(url_for("profile"))

        error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/profile")
@require_login
def profile():
    mode = session.get("mode", "vulnerable")
    return render_template(
        "profile.html",
        customer=customer,
        mode=mode,
    )


@app.route("/profile/update", methods=["POST"])
@require_login
def update_profile():
    mode = session.get("mode", "vulnerable")

    # Secure mode requires a valid session-bound CSRF token.
    if mode == "secure" and not valid_csrf_token():
        return make_response(
            """
            <!DOCTYPE html>
            <html lang="en">
            <head><meta charset="UTF-8"><title>Request Rejected</title></head>
            <body><p>Request rejected: missing or invalid CSRF token.</p></body>
            </html>
            """,
            403,
        )

    address = request.form.get("address", "").strip()

    if not address or len(address) > 200:
        return "Invalid delivery address.", 400

    # The same profile is updated in either mode when accepted.
    customer["address"] = address

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="UTF-8"><title>Update Result</title></head>
    <body><p>Request processed.</p></body>
    </html>
    """


@app.route("/mode/<mode_name>", methods=["POST"])
@require_login
def set_mode(mode_name):
    if mode_name not in ("vulnerable", "secure"):
        abort(400, description="Invalid mode.")

    if not valid_csrf_token():
        abort(403, description="Invalid CSRF token.")

    session["mode"] = mode_name
    return redirect(url_for("profile"))


@app.route("/reset-demo", methods=["POST"])
@require_login
def reset_demo():
    if not valid_csrf_token():
        abort(403, description="Invalid CSRF token.")

    # Restore the original profile without creating another profile.
    customer.update(INITIAL_PROFILE)
    return redirect(url_for("profile"))


@app.route("/logout", methods=["POST"])
@require_login
def logout():
    if not valid_csrf_token():
        abort(403, description="Invalid CSRF token.")

    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
