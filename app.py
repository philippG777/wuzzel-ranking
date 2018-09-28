from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# for testing
def generate_test_user():
    return User(0, "test", generate_password_hash("test"))


def query_user_by_id(id):
    if id == 0:
        return generate_test_user()
    return None


def query_user_by_name(name):
    if name == "test":
        return generate_test_user()
    return None


class User(object):
    @staticmethod
    def get(user_id):
        return query_user_by_id(user_id)
    
    @staticmethod
    def get_by_name(name):
        return query_user_by_name(name)

    def __init__(self, id, name, password_hash):
        self.id = id
        self.name = name
        self.hash = password_hash

        self.is_authenticated = False
        self.is_active = True
        self.is_anonymus = False
    
    def get_id(self):
        return u"%d" % self.id

    def check_password(self, password):
        return check_password_hash(self.hash, password)


login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["u"]
    password = request.form["p"]

    user = User.get_by_name(username)
    if user is not None and user.check_password(password):
        login_user(user)
        return redirect("/dashboard")
    return "Login failed"

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run()
