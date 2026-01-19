import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from db import init_db, db
from models import Host, Workshop, Participant, Question, Answer

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-later"

# SQLite lokal im instance-Ordner (prof-style)
os.makedirs(app.instance_path, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "app.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

def seed_questions():
    if Question.query.first():
        return
    demo = [
        ("Ich treffe Entscheidungen schnell.", "D"),
        ("Ich bin kontaktfreudig.", "I"),
        ("Ich bin geduldig.", "S"),
        ("Ich arbeite gern strukturiert.", "C"),
    ]
    for text, dim in demo:
        db.session.add(Question(text=text, dimension=dim))
    db.session.commit()

with app.app_context():
    db.create_all()
    seed_questions()
app.secret_key = "dev-secret-change-later"

#Testdaten
FAKE_HOST = {
    "email": "host@example.com",
    "password": "pass123",
    "name": "Demo Host"
}

QUESTIONS = [
    {"id": 1, "text": "Ich treffe Entscheidungen schnell.", "dimension": "D"},
    {"id": 2, "text": "Ich bin kontaktfreudig.", "dimension": "I"},
    {"id": 3, "text": "Ich arbeite gern strukturiert.", "dimension": "C"},
    {"id": 4, "text": "Ich bin geduldig.", "dimension": "S"},
]


@app.route("/")
def index():
    # Startseite: Rolle wählen
    return render_template("index.html")


@app.route("/workshops/new", methods=["GET"])
def workshop_new():
    # Host legt einen neuen Workshop an (Formular)
    return render_template("host_create.html")


@app.route("/workshops", methods=["POST"])
def workshop_create():
    if not require_host_login():
        return redirect(url_for("login_get"))

    title = request.form.get("title", "").strip() or "Neuer Workshop"

    # kurzer Code, eindeutig halten
    while True:
        code = secrets.token_hex(2).upper()  # z.B. 'A1B2'
        if not Workshop.query.filter_by(code=code).first():
            break

    w = Workshop(
        code=code,
        title=title,
        status="open",
        host_id=session["host_id"],
    )
    db.session.add(w)
    db.session.commit()

    return redirect(url_for("host_dashboard", code=code))




@app.route("/workshops/<code>/host", methods=["GET"])
def host_dashboard(code):
    # Host-Ansicht (Übersicht über Teilnehmer & Ergebnisse)
    return render_template("host_dashboard.html", code=code, questions=QUESTIONS)


@app.route("/join", methods=["GET"])
def join_get():
    # Teilnehmende geben Name + Code ein
    return render_template("join_session.html")


@app.route("/join", methods=["POST"])
def join_post():
    name = request.form.get("name")
    code = request.form.get("code")
    # Später: Teilnehmer speichern
    # Jetzt: direkt zum Test weiterleiten
    return redirect(url_for("test_get", code=code))


@app.route("/workshops/<code>/test", methods=["GET"])
def test_get(code):
    # Später: Fragen laden
    # Jetzt: Platzhalter-Testseite
    return render_template("test.html", code=code, questions=QUESTIONS)

@app.route("/workshops/<code>/submit", methods=["POST"])
def test_submit(code):
    # Später: Antworten auswerten
    # Jetzt: einfach Dummy-Ergebnis anzeigen
    return redirect(url_for("results", code=code))


@app.route("/workshops/<code>/results", methods=["GET"])
def results(code):
    dummy_results = {
        "team_name": f"Workshop {code}",
        "d": 10,
        "i": 7,
        "s": 5,
        "c": 3,
    }
    return render_template("results.html", results=dummy_results, code=code)


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    host = Host.query.filter_by(email=email).first()
    if not host or not check_password_hash(host.password_hash, password):
        return render_template("login.html", error="Login fehlgeschlagen (falsche Daten).")

    session["host_id"] = host.id
    session["host_name"] = host.name
    return redirect(url_for("dashboard"))


    return render_template("login.html", error="Login fehlgeschlagen (falsche Daten).")


@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template("register.html", error="Bitte alle Felder ausfüllen.")

    existing = Host.query.filter_by(email=email).first()
    if existing:
        return render_template("register.html", error="Diese E-Mail ist bereits registriert.")

    host = Host(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(host)
    db.session.commit()

    # direkt einloggen
    session["host_id"] = host.id
    session["host_name"] = host.name
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_get"))

def require_host_login():
    return "host_id" in session


@app.route("/dashboard")
def dashboard():
    if not require_host_login():
        return redirect(url_for("login_get"))

    host_id = session["host_id"]
    workshops = Workshop.query.filter_by(host_id=host_id).order_by(Workshop.created_at.desc()).all()
    return render_template("host_home.html", workshops=workshops)




if __name__ == "__main__":
    app.run(debug=True)
