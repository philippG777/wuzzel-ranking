from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, \
                                LoginManager, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import config


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
        return redirect("/dashboard/")
    return render_template("login.html")

@app.route("/login/", methods=["POST"])
def login():
    username = request.form["u"]
    password = request.form["p"]

    user = load_user(username)
    if user is not None and user.check_password(password):
        login_user(user)
        return redirect(url_for("dashboard"))
    return redirect("/")

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/dashboard/")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run()
