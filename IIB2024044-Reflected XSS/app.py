from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Harmless JavaScript payload for demonstrating reflected XSS.
# The alert appears if the browser executes the injected script.
DEMO_PAYLOAD = "<script>alert('Reflected XSS Demonstration')</script>"

#<script>
#document.querySelector('.results').innerHTML =
#'<h3>Hostel Fee Payment</h3><p>Your hostel account has an outstanding balance of ₹2,000.</p><p style="color:red">Pay today to avoid account restrictions.</p><button onclick="alert(\'Demo only: payment was not made\')">Pay Now</button>';
#</script>


@app.route("/")
def home():
    # Redirect the homepage to the vulnerable version.
    return redirect(url_for("vulnerable"))


@app.route("/vulnerable", methods=["GET"])
def vulnerable():
    # Read the search query from the URL parameter named q.
    query = request.args.get("q", "")

    # Render the shared HTML page in vulnerable mode.
    # The template uses the |safe filter to demonstrate
    # what happens when untrusted input is not escaped.
    return render_template(
        "index.html",
        mode="vulnerable",
        query=query,

        # Generate a link containing the demonstration payload.
        demo_link=url_for("vulnerable", q=DEMO_PAYLOAD)
    )


@app.route("/secure", methods=["GET"])
def secure():
    # Read the search query from the URL parameter named q.
    query = request.args.get("q", "")

    # Render the same HTML page in secure mode.
    # The template uses Jinja2's automatic HTML escaping
    # when displaying the search query.
    return render_template(
        "index.html",
        mode="secure",
        query=query,

        # Generate the equivalent link for testing the mitigation.
        demo_link=url_for("secure", q=DEMO_PAYLOAD)
    )


if __name__ == "__main__":
    # Start the Flask development server for local testing.
    app.run(debug=True)
