# GapUp - IT Career Path Simulator

GapUp is a lightweight, high-performance Server-Side Rendered (SSR) web application built to help aspiring IT professionals analyze skill gaps, calculate required learning hours, and visualize clear learning paths toward target technical roles.

---

## Tech Stack

* **Backend**: Python 3, Flask
* **Templating**: Jinja2 (SSR)
* **Database**: SQLite3
* **Styling**: Tailwind CSS (via CDN)

---

## Key Features

* **Dynamic Gap Analysis**: Compares a user's current skill set with the requirements of a target role.
* **Effort and Pace Estimation**: Calculates missing study hours and suggests realistic schedules for Casual, Moderate, and Intensive plans.
* **Automatic Database Setup**: Seeds and initializes the SQLite database when needed on first launch.
* **Structured Data Access**: Uses a dedicated database layer to keep role, skill, and certification data organized.

---

##  Quickstart Guide

### 1. Local Setup
1. Define dependencies in `requirements.txt` (`Flask`, `gunicorn`).
2. Run `main.py` — it automatically initializes the SQLite database (`gap_up.db`) and creates required tables.
3. Commit and push your changes to the GitHub `main` branch.

### 2. Deployment (Render.com)
1. Connect your GitHub repository as a new **Web Service** on Render.com.
2. Set **Build Command**: `pip install -r requirements.txt`
3. Set **Start Command**: `gunicorn main:app`
4. Deploy the application and access it via the public URL.
