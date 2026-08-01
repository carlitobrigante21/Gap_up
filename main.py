"""
GapUp — IT Career Path & Skill Gap Simulator
A traditional server-side rendered (SSR) monolith built with Flask + Jinja2.

The server runs SQL queries directly against the SQLite database and passes
query results straight into Jinja2 templates to render static HTML pages.
No SPA, no REST API, no JSON endpoints, no client-side fetch()/AJAX.
"""

import math
import os
from flask import Flask, render_template, request, abort

import db

app = Flask(__name__)

# --- Force DB Initialization on Server Startup ---
# Ensure database file exists and schema is built.
try:
    if not os.path.exists(db.DB_PATH):
        db.build_database(force=True)
    else:
        db.build_database(force=False)
except Exception as e:
    print(f"Database setup error: {e}")
# --------------------------------------------------

# Weekly study paces (hours per week) for the transition timeline.
PACES = [
    {"key": "casual", "label": "Casual", "hours_per_week": 10, "blurb": "Evenings & weekends"},
    {"key": "moderate", "label": "Moderate", "hours_per_week": 20, "blurb": "Part-time study"},
    {"key": "intensive", "label": "Intensive", "hours_per_week": 40, "blurb": "Full-time bootcamp"},
]


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------
def _fetch_roles():
    conn = db.get_connection()
    try:
        cur = conn.execute("SELECT id, name FROM roles ORDER BY name ASC;")
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def _fetch_role_name(role_id):
    conn = db.get_connection()
    try:
        cur = conn.execute("SELECT name FROM roles WHERE id = ?;", (role_id,))
        row = cur.fetchone()
        return row["name"] if row else None
    finally:
        conn.close()


def _fetch_role_skills(role_id):
    conn = db.get_connection()
    try:
        cur = conn.execute(
            """
            SELECT s.id, s.name, s.estimated_hours, s.parent_skill_id,
                   p.name AS parent_name
            FROM role_skills rs
            JOIN skills s ON s.id = rs.skill_id
            LEFT JOIN skills p ON p.id = s.parent_skill_id
            WHERE rs.role_id = ?
            ORDER BY s.name ASC;
            """,
            (role_id,),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def _fetch_role_certs(role_id):
    conn = db.get_connection()
    try:
        cur = conn.execute(
            """
            SELECT c.id, c.name, c.issuer, c.estimated_hours
            FROM role_certs rc
            JOIN cert c ON c.id = rc.cert_id
            WHERE rc.role_id = ?
            ORDER BY c.name ASC;
            """,
            (role_id,),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def _fetch_all_roles_with_counts():
    """All roles plus the number of skills and certs linked to each."""
    conn = db.get_connection()
    try:
        cur = conn.execute(
            """
            SELECT r.id, r.name,
                   (SELECT COUNT(*) FROM role_skills rs WHERE rs.role_id = r.id) AS skill_count,
                   (SELECT COUNT(*) FROM role_certs rc WHERE rc.role_id = r.id) AS cert_count
            FROM roles r
            ORDER BY r.name ASC;
            """
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def _fetch_all_skills_grouped():
    """All skills grouped by parent category name."""
    conn = db.get_connection()
    try:
        cur = conn.execute(
            """
            SELECT s.id, s.name, s.estimated_hours,
                   p.name AS parent_name
            FROM skills s
            LEFT JOIN skills p ON p.id = s.parent_skill_id
            WHERE s.parent_skill_id IS NOT NULL
            ORDER BY p.name ASC, s.name ASC;
            """
        )
        rows = [dict(r) for r in cur.fetchall()]
        groups: dict[str, list] = {}
        for r in rows:
            cat = r["parent_name"] or "Other"
            groups.setdefault(cat, []).append(r)
        return groups
    finally:
        conn.close()


def _fetch_all_certs():
    conn = db.get_connection()
    try:
        cur = conn.execute(
            "SELECT id, name, issuer, estimated_hours FROM cert ORDER BY name ASC;"
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    roles = _fetch_roles()
    return render_template("index.html", roles=roles, active="home")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        current_role_id = int(request.form.get("current_role_id", ""))
        target_role_id = int(request.form.get("target_role_id", ""))
    except (TypeError, ValueError):
        abort(400, "Invalid form submission. Please select valid roles.")

    current_role_name = _fetch_role_name(current_role_id)
    target_role_name = _fetch_role_name(target_role_id)
    if current_role_name is None or target_role_name is None:
        abort(400, "Selected role does not exist.")

    current_skills = _fetch_role_skills(current_role_id)
    target_skills = _fetch_role_skills(target_role_id)
    current_certs = _fetch_role_certs(current_role_id)
    target_certs = _fetch_role_certs(target_role_id)

    current_skill_ids = {s["id"] for s in current_skills}
    current_cert_ids = {c["id"] for c in current_certs}

    covered_skills, missing_skills = [], []
    for s in target_skills:
        (covered_skills if s["id"] in current_skill_ids else missing_skills).append(s)

    covered_certs, missing_certs = [], []
    for c in target_certs:
        (covered_certs if c["id"] in current_cert_ids else missing_certs).append(c)

    missing_skill_hours = sum(s["estimated_hours"] for s in missing_skills)
    missing_cert_hours = sum(c["estimated_hours"] for c in missing_certs)
    total_hours = missing_skill_hours + missing_cert_hours

    pacing = []
    for p in PACES:
        weeks = math.ceil(total_hours / p["hours_per_week"]) if total_hours > 0 else 0
        months = round(weeks / 4.33, 1) if weeks else 0
        pacing.append({**p, "weeks": weeks, "months": months})

    context = {
        "current_role_name": current_role_name,
        "target_role_name": target_role_name,
        "total_target_skills": len(target_skills),
        "covered_count": len(covered_skills),
        "missing_count": len(missing_skills),
        "total_target_certs": len(target_certs),
        "covered_certs_count": len(covered_certs),
        "missing_certs_count": len(missing_certs),
        "missing_skill_hours": missing_skill_hours,
        "missing_cert_hours": missing_cert_hours,
        "total_hours": total_hours,
        "pacing": pacing,
        "covered_skills": covered_skills,
        "missing_skills": missing_skills,
        "covered_certs": covered_certs,
        "missing_certs": missing_certs,
        "same_role": current_role_id == target_role_id,
        "active": "",
    }
    return render_template("results.html", **context)


@app.route("/roles")
def roles():
    roles_data = _fetch_all_roles_with_counts()
    return render_template("roles.html", roles=roles_data, active="roles")


@app.route("/skills")
def skills():
    groups = _fetch_all_skills_grouped()
    return render_template("skills.html", groups=groups, active="skills")


@app.route("/certs")
def certs():
    certs_data = _fetch_all_certs()
    return render_template("certs.html", certs=certs_data, active="certs")


# ---------------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------------
@app.errorhandler(400)
def bad_request(e):
    msg = str(e.description) if hasattr(e, "description") else "Bad request."
    return render_template("error.html", message=msg), 400


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", message="An unexpected server error occurred."), 500


if __name__ == "__main__":
    if not os.path.exists(db.DB_PATH):
        db.build_database()
    app.run(host="0.0.0.0", port=8000, debug=True)