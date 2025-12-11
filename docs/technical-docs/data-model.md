---
title: Data Model
parent: Technical Docs
nav_order: 2
---

# Data model
![ER Diagram](..assets/images/erd_personalitytest.png)

<details open markdown="block">
{: .text-delta }


Das Datenmodell der DISC-Workshop-App besteht aus vier zentralen Entitäten: **Workshop**, **Participant**, **Question** und **Answer**.  
Diese Struktur ermöglicht es, Teilnehmer in Workshops zu organisieren, DISC-Fragen zu stellen und alle Antworten eindeutig zu speichern und auszuwerten.



## Workshop

**Attribute:**

- `id` – eindeutige Workshop-ID  
- `code` – öffentlicher Beitrittscode  
- `title` – Name des Workshops  
- `created_at` – Zeitpunkt der Erstellung  

**Beziehungen:**

- Ein Workshop hat mehrere Participants


## Participant

**Attribute:**

- `id` – eindeutige Teilnehmer-ID  
- `name` – Name der Person  
- `joined_at` – Zeitpunkt des Beitritts  

**Beziehungen:**

- Ein Participant gehört zu einem Workshop
- Ein Participant hat mehrere Answers

---

## Question

**Attribute:**

- `id` – eindeutige Frage-ID  
- `text` – Inhalt der Frage  
- `dimension` – DISC-Kategorie (D, I, S oder C)

**Beziehungen:**

- Eine Question hat mehrere Answers

---

## Answer

**Attribute:**

- `id` – eindeutige Antwort-ID  
- `value` – numerischer Antwortwert (z. B. Skala 1–5)

**Beziehungen:**

- Ein Answer gehört zu einem Participant
- Ein Answer gehört zu einer Question



