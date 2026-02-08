---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
Patman Safi; Emre Savas

{: .no_toc }
# Architecture

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

Unsere Anwendung ist eine Flask‑basierte Web‑App für DISC‑Workshops: Hosts erstellen Workshops mit Code, Teilnehmende treten mit Name+Code bei und beantworten Fragen; das System speichert Antworten und berechnet daraus individuelle sowie Team‑Ergebnisse pro DISC‑Dimension (D, I, S, C). Die gesamte Fachlogik läuft im Backend (Session‑basierte Auth für Hosts/Teilnehmende, Workshop‑Status „open/closed“, Quiz‑Ablauf und Ergebnisberechnung), während die UI per Templates gerendert wird und über definierte Routen interagiert.

## Codemap

+ app.py (Flask‑App & Routen): Zentraler Einstieg, Konfiguration (SQLite in instance/), Session‑Handling sowie alle HTTP‑Routen für Host (Login/Registrierung, Workshop anlegen, Host‑Dashboard, Workshop öffnen/schließen) und Teilnehmer (Join, Test‑Navigation, Ergebnisse). Die Auswertung der DISC‑Scores geschieht beim Host‑Dashboard und in der Ergebnisansicht, indem Antworten mit Fragen (Dimension) gejoint und aggregiert werden.
+ models.py & db.py (Datenmodell und DB-Initialisierung): SQLAlchemy‑Modelle für Hosts, Workshops, Teilnehmer, Fragen und Antworten (models.py) und Einfache SQLAlchemy‑Initialisierung, die in app.py gebunden wird.(db.py)
+ Templates (templates/): Hier liegen die HTML‑Dateien für die Seiten (z. B. Startseite, Login, Workshop‑Ansicht, Test und Ergebnisse). Die Routen in app.py rendern diese Templates direkt.
+ style.css (Design): Enthält die grundlegenden Styles für Layout, Farben, Buttons und Abstände, damit die Seiten einheitlich aussehen.

## Cross-cutting concerns

+ Session‑basierte Zugriffslogik: Host‑Zugriffe werden über host_id in der Session abgesichert (z. B. Workshop‑Erstellung und Dashboard). Teilnehmer müssen zu genau dem Workshop gehören, dessen Test/Resultate sie sehen; das wird über participant_id, workshop_id und workshop_code in der Session geprüft.
+ DISC‑Score‑Berechnung: Jede Frage ist einer Dimension zugeteilt. Je nach Antwort des Teilnehmers, wird der zugehörigen Dimension der Score, welcher sich aus der Antwort der Frage erschließen lässt hinzugefügt. Die Score‑Logik sammelt Antworten pro Teilnehmer, summiert je Dimension und ermittelt anschließend den dominanten Typen bzw. die Dimension mit dem höchsten Score.
+ Datenmodell‑Konsistenz: Fragen sind über die dimension‑Spalte an DISC‑Dimensionen gebunden; Antworten referenzieren sowohl Frage als auch Workshop und Teilnehmer. Dadurch lassen sich Auswertungen immer workshop‑bezogen durchführen und gleichzeitig für Team‑ und Einzel‑Views verwenden.
