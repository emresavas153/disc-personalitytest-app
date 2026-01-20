import os
import secrets

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

from db import db, init_db
from models import Host, Workshop, Participant, Question, Answer


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-later"

os.makedirs(app.instance_path, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "app.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

with app.app_context():
    db.create_all()


#Startseite
@app.route("/")
def index():
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
        code = secrets.token_hex(2).upper()  #token bzw. code für den Workshop
        if not Workshop.query.filter_by(code=code).first(): #Schleife für eindeutigen code
            break
    
    #Erstellen eines Workshops
    w = Workshop(
        code=code,
        title=title,
        status="open",
        host_id=session["host_id"],
    )
    #Anbinden an die DB
    db.session.add(w)
    db.session.commit()

    return redirect(url_for("host_dashboard", code=code))




@app.route("/workshops/<code>/host", methods=["GET"])
def host_dashboard(code):
    if not require_host_login():
        return redirect(url_for("login_get"))

    workshop = Workshop.query.filter_by(code=code, host_id=session["host_id"]).first_or_404() #Workshop des eingeloggten Hosts holen

    participants = Participant.query.filter_by(workshop_id=workshop.id).order_by(Participant.joined_at.asc()).all() #Teilnehmer des Workshops holen

    
    team_counts = {"D": 0, "I": 0, "S": 0, "C": 0}
    team_ties = 0

    
    all_answers = (
        db.session.query(Answer, Question)
        .join(Question, Answer.question_id == Question.id)
        .filter(Answer.workshop_id == workshop.id)
        .all()
    )
    #Punktesystem für die Team-Auswertung
    participant_scores = {}
    for a, q in all_answers:
        participant_scores.setdefault(
            a.participant_id,
            {"D": 0, "I": 0, "S": 0, "C": 0}
        )
        participant_scores[a.participant_id][q.dimension] += a.value

    for scores in participant_scores.values():
        dominant = dominant_types(scores)
        if len(dominant) == 1:
            team_counts[dominant[0]] += 1
        elif len(dominant) > 1:
            team_ties += 1

    return render_template(
        "host_dashboard.html",
        workshop=workshop,
        participants=participants,
        team_results=team_counts,
        team_ties=team_ties,
    )


#workshop öffnen/schließen
@app.route("/workshops/<code>/toggle", methods=["POST"])
def workshop_toggle(code):
    if not require_host_login():
        return redirect(url_for("login_get"))

    workshop = Workshop.query.filter_by(code=code, host_id=session["host_id"]).first_or_404()

    workshop.status = "closed" if workshop.status == "open" else "open"
    db.session.commit()

    return redirect(url_for("host_dashboard", code=code))


@app.route("/join", methods=["GET"])
def join_get():
    # Teilnehmende geben Name + Code ein
    return render_template("join_session.html")


from sqlalchemy import func
import secrets

def dominant_types(scores):
    if not scores:
        return []
    max_value = max(scores.values())
    return [key for key, value in scores.items() if value == max_value]

@app.route("/join", methods=["POST"])
def join_post():
    name = request.form.get("name", "").strip()
    code = request.form.get("code", "").strip().upper()

    if not name or not code:
        return render_template("join_session.html", error="Bitte Name und Code eingeben.")

    workshop = Workshop.query.filter_by(code=code).first()
    if not workshop:
        return render_template("join_session.html", error="Workshop-Code nicht gefunden.")
    if workshop.status != "open":
        return render_template("join_session.html", error="Dieser Workshop ist geschlossen.")

    # Teilnehmer anlegen und Token generieren
    participant_token = secrets.token_urlsafe(24)

    p = Participant(
        name=name,
        participant_token=participant_token,
        workshop_id=workshop.id,
    )
    db.session.add(p)
    db.session.commit()

    # Teilnehmer “einloggen”
    session["participant_id"] = p.id
    session["participant_token"] = p.participant_token
    session["workshop_id"] = workshop.id
    session["workshop_code"] = workshop.code

    return redirect(url_for("test_get", code=workshop.code))





@app.route("/workshops/<code>/test", methods=["GET"])
def test_get(code):
    workshop = Workshop.query.filter_by(code=code).first_or_404()

    
    # Teilnehmer muss aus genau diesem Workshop kommen
    if session.get("workshop_id") != workshop.id or "participant_id" not in session:
        return redirect(url_for("join_get"))

    questions = Question.query.order_by(Question.id.asc()).all()

    # Fullscreen für Quiz
    return render_template("test.html", code=code, questions=questions, fullscreen=True)





@app.route("/workshops/<code>/submit", methods=["POST"])
def test_submit(code):
    workshop = Workshop.query.filter_by(code=code).first_or_404()

    # Teilnehmer muss aus genau diesem Workshop kommen (Überprüfung)
    if session.get("workshop_id") != workshop.id or "participant_id" not in session:
        return redirect(url_for("join_get"))

    # Teilnehmer-ID aus Session holen
    participant_id = session["participant_id"]

    # falls User erneut abgibt: alte Antworten löschen
    Answer.query.filter_by(workshop_id=workshop.id, participant_id=participant_id).delete()
    db.session.commit()

    questions = Question.query.order_by(Question.id.asc()).all()

    # Antworten speichern
    for q in questions:
        val = request.form.get(f"q_{q.id}")
        if val is None:
            # fehlende Antwort, zurück zum Test (sollte eigentlich nicht passieren aberals Absicherung))
            return redirect(url_for("test_get", code=code))

        a = Answer(
            value=int(val),
            participant_id=participant_id,
            question_id=q.id,
            workshop_id=workshop.id,
        )
        db.session.add(a)

    db.session.commit()
    return redirect(url_for("results", code=code))






@app.route("/workshops/<code>/results", methods=["GET"])
def results(code):
    workshop = Workshop.query.filter_by(code=code).first_or_404()

    participant_id = session.get("participant_id")
    if not participant_id or session.get("workshop_code") != code:
        return redirect(url_for("join_get"))

    # alle Answers im Workshop + Questions joinen um Dimension zu kennen
    all_answers = (
        db.session.query(Answer, Question) #alle Antworten und Fragen holen
        .join(Question, Answer.question_id == Question.id)# Antworten mit Fragen verbinden
        .filter(Answer.workshop_id == workshop.id) #nur Antworten des aktuellen Workshops
        .all() #alle Ergebnisse holen
    )



    # Team-Auswertung
    team_counts = {"D": 0, "I": 0, "S": 0, "C": 0}
    team_ties = 0
    participant_scores = {}
    for a, q in all_answers:
        participant_scores.setdefault(
            a.participant_id,
            {"D": 0, "I": 0, "S": 0, "C": 0}
        )
        participant_scores[a.participant_id][q.dimension] += a.value

    for scores in participant_scores.values():
        dominant = dominant_types(scores)
        if len(dominant) == 1:
            team_counts[dominant[0]] += 1
        elif len(dominant) > 1:
            team_ties += 1

    # mein Ergebnis
    my_answers = (
        db.session.query(Answer, Question)
        .join(Question, Answer.question_id == Question.id)
        .filter(Answer.workshop_id == workshop.id, Answer.participant_id == participant_id)
        .all()
    )
    my_scores = {"D": 0, "I": 0, "S": 0, "C": 0}
    for a, q in my_answers:
        my_scores[q.dimension] += a.value
    my_dominant = dominant_types(my_scores)

    return render_template(
        "results.html",
        code=code,
        team_name=workshop.title,
        team_results=team_counts,
        team_ties=team_ties,
        my_dominant=my_dominant
    )



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

    # der Host muss sich nach der Registrierung nicht nochmal einloggen
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
