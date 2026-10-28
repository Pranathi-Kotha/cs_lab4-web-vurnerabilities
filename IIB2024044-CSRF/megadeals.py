
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def deals():
    return render_template("deals.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
