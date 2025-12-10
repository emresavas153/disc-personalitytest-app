from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
    # Später: Workshop speichern, Code generieren
    # Jetzt: tun wir so als wäre der Code "ABCD"
    code = "ABCD"
    return redirect(url_for("host_dashboard", code=code))


@app.route("/workshops/<code>/host", methods=["GET"])
def host_dashboard(code):
    # Host-Ansicht (Übersicht über Teilnehmer & Ergebnisse)
    return render_template("host_dashboard.html", code=code, questions=questions)


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
    return render_template("test.html", code=code)


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


if __name__ == "__main__":
    app.run(debug=True)