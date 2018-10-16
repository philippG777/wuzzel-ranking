from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, \
                                LoginManager, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import config

"""
TODO
====
* Fix user-adding
* Check if user exists at user-adding
* Refactor User-validation when adding a game
* Increment the wins and losses counters when adding a game
"""

SQLALCHEMY_DATABASE_URI = ("mysql+mysqlconnector://{username}:"
                           "{password}@{hostname}/{databasename}").format(
    username = config.db_user,
    password = config.db_password,
    hostname = config.db_hostname,
    databasename = config.db_name
)

app = Flask(__name__)
app.config["DEBUG"] = False
app.config["SECRET_KEY"] = config.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    role = db.Column(db.String(8))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    played = db.Column(db.DateTime, default=datetime.now)
    winner_front_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    winner_back_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    looser_front_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    looser_back_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    winner_front = db.relationship('User', foreign_keys=winner_front_id)
    winner_back = db.relationship('User', foreign_keys=winner_back_id)
    looser_front = db.relationship('User', foreign_keys=looser_front_id)
    looser_back = db.relationship('User', foreign_keys=looser_back_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("dashboard.html", users=User.query.all(),
                                                 games=Game.query.all())
    else:
        return redirect(url_for("login"))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["u"]
    password = request.form["p"]

    user = load_user(username)
    if user is not None and user.check_password(password):
        login_user(user)
        return redirect(url_for("index"))
    return redirect(url_for("login"))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/addgame/", methods=["GET", "POST"])
@login_required
def add_game():
    if request.method == "GET":
        return render_template("addgame.html", users=User.query.all())
    
    winner_front = request.form["wf"]
    winner_back = request.form["wb"]
    looser_front = request.form["lf"]
    looser_back = request.form["lb"]

    if winner_front is not None and winner_back is not None and \
        looser_front is not None and looser_back is not None:
        new_game = Game(
           winner_front=User.query.filter_by(username=winner_front).first(),
           winner_back=User.query.filter_by(username=winner_back).first(),
           looser_front=User.query.filter_by(username=looser_front).first(),
           looser_back=User.query.filter_by(username=looser_back).first())
        
        db.session.add(new_game)
        db.session.commit()

    return redirect(url_for("index"))

@app.route("/admin/")
@login_required
def admin():
    if current_user.role != "admin":
        return redirect(url_for("index"))
    return render_template("admin.html")

@app.route("/admin/adduser/", methods=["POST"])
@login_required
def add_user():
    if current_user.role != "admin":
        return redirect(url_for("index"))

    username = request.form["u"]
    password = request.form["p"]

    if username is not None and password is not None:
        new_user = User(username=username,
                        password_hash=generate_password_hash(password), wins=0,
                        losses=0, role="user")
        if request.form["a"] is not None:       # admin
            new_user.role = "admin"
        
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run()
