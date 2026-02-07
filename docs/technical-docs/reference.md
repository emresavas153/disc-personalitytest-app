---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Reference documentation


<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Home

**Route:** `/`

**Methods:** `GET`

**Purpose:** Homescreen; der Nutzer gibt an ob er Host oder Teilnehmer ist

**Sample output:**

![index](../assets/images/index.png)

---
# Host-Screens


## Host Login

**Route:** `/login`

**Methods:** `GET`

**Purpose:** Login für den Host; Weiterleitung auf Registrierung falls kein Account aneglegt

**Sample output:**

![host_login](../assets/images/host_login.png)

---

## Host Register

**Route:** `/register`

**Methods:** `GET`

**Purpose:** Registrierung für einen neuen Host Account

**Sample output:**

![host_register](../assets/images/host_regsiter.png)

---

## Host Dashboard

**Route:** `/dashboard`

**Methods:** `GET`

**Purpose:** Liste mit allen erstellten Workshops; Weiterleiten zum erstellen eines neuen

**Sample output:** ![host_dashboard](../assets/images/host_dashboard)

---

## Create Workshop

**Route:** `/workshops/new`

**Methods:** `GET`

**Purpose:** Registrierung für einen neuen Host Account

**Sample output:**

![create_workshop](../assets/images/create_workshop.png)

---

## Overview Workshop

**Route:** `/workshops/<code>/new`

**Methods:** `GET`

**Purpose:** Der Host hat eine Übersicht über den erstellten Workshop und sieht: code, status, Team Ergebnisse und die Teilnehmer

**Sample output:**

![create_workshop](../assets/images/create_workshop.png)

---

# Teilnehmer-Screens

## Join Workshop

**Route:** `/join`

**Methods:** `GET`

**Purpose:** Der Teilnehmer gibt seinen Namen und den Workshop Code ein

**Sample output:**

![join](../assets/images/join.png)

---

## Test

**Route:** `/workshops/<code>/test`

**Methods:** `GET`

**Purpose:** Der Teilnehmer beantwortet die Fragen(1(trifft gar nicht zu) bis 5(trifft voll und gaz zu))

**Sample output:**

![user_test](../assets/images/user_test.png)

---

## Ergebnisse

**Route:** `/workshops/<code>/test`

**Methods:** `GET`

**Purpose:** Der Teilnehmer sieht seine eigenen Ergebnisse, die Ergebnisse des Teams und einen Informationstext zu den unterschiedlichen Typen

**Sample output:**

![results](../assets/images/results.png)
![results2](../assets/images/results2.png)

