from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/auth")
def auth():
    return "auth-page"


if __name__ == "__main__":
    app.run()
