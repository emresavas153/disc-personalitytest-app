---
title: Design Decisions
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Datenbank

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: Datenbank (SQLite + SQLAlchemy):

### Meta

Status
: Decided

Updated
: 31-01-2026

### Problem statement

Wir benötigen eine Datenbank, die lokal ohne zusätzliche Infrastruktur läuft und sich unkompliziert in unsere Flask-App integrieren lässt. Außerdem soll die Lösung später erweiterbar bleiben.

### Decision

Wir nutzen SQLite als lokale Datenbank und greifen über SQLAlchemy darauf zu. So bleiben Setup und Deployment einfach, während das ORM eine spätere Migration auf ein anderes Datenbanksystem ermöglicht.

### Regarded options

- SQLite + SQLAlchemy ✔️
- nur direktes SQL

---

## 02: UI-Design mit CSS und eigenen Templates

### Meta

Status
: Decided

Updated
: 30-Jun-2024

### Problem statement

Wir wollen ein ansprechendes, konsistentes Design bei vertretbarem Aufwand. Gleichzeitig soll das Team die HTML-Struktur selbst verstehen und anpassen können.


### Decision

Das Styling (style.css) wurde mit Unterstützung von KI (ChatGPT) erstellt, um schnell eine moderne Optik zu erreichen. Die HTML-Templates wurden von uns selbst erstellt und angepasst, damit wir die Struktur vollständig kontrollieren können


### Regarded options

- KI-unterstütztes CSS + eigene HTML-Templates ✔️
- Komplettes Design vollständig manuell
- Fertiges UI-Framework (z. B. Bootstrap)

---

## 03: Rollenmodell mit Host und Teilnehmenden

### Meta

Status
: Decided

Updated
: 30-Jun-2024

### Problem statement

Im Workshop-Kontext benötigen wir unterschiedliche Funktionen: Hosts erstellen und steuern Workshops, Teilnehmende sollen schnell ohne Registrierung starten können.



### Decision

Wir trennen klar zwischen Host und Teilnehmenden. So bleibt die Bedienung für beide Rollen klar und sicher.

#### Host-Featuress:
- Login & Register
- Workshops erstellen
- Liste aller erstellten Workshops
- Workshops schließen und öffnen
- Einsehen auf: Namen der Teilnehmenden & Teamergebnisse, jedoch nicht die Ergebnisse der einzelnen Teilnehmer

#### Teilnehmer-Features:
- Workshop beitreten
- Fragen beantworten und Fragebogen absolvieren
- Einsehen auf: eigenes Ergebnis und Teamergebnis

### Regarded options

- Host- und Teilnehmendenrollen ✔️
- Ein gemeinsamer Nutzer-Typ für alle
- Vollständige Registrierung für alle Teilnehmenden

---
## 04: Workshop-Zugang über Codes

### Meta

Status
: Decided

Updated
: 30-Jun-2024

### Problem statement

Teilnehmende sollen schnell in einen Workshop einsteigen können, ohne dass sie ein Konto anlegen müssen. Gleichzeitig müssen Hosts ihren Workshop gezielt öffnen und schließen können.

### Decision

Wir verwenden Workshop-Codes, die Hosts erstellen und teilen. Teilnehmende geben nur Name und Code ein. Das hält den Einstieg niedrigschwellig und ermöglicht dennoch Kontrolle über den Zugang.

### Regarded options

- Workshop-Code (gewählt) ✔️
- Öffentlicher Link ohne Steuerung
- Teilnahme nur mit registriertem Nutzerkonto
