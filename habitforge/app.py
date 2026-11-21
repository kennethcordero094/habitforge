import os
from functools import wraps

from flask import (Flask, jsonify, redirect, render_template, request,
                   session, url_for)

import supa
from data.exercises import DEFAULT_HABITS, DEFAULT_PLAN, EXERCISES, MUSCLES

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# DEMO MODE = no Supabase keys. Data is saved in the browser (localStorage).
DEMO_MODE = not supa.enabled()


def default_state():
    return {
        "habits": DEFAULT_HABITS,
        "checks": {},          # {"2026-11-21": {"habits": [ids], "exercises": [ids]}}
        "plan": DEFAULT_PLAN,  # {"0": [exercise ids], ... "6": []}
        "notes": [],           # [{id, title, items: [{id, text, done}]}]
    }


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.context_processor
def inject_globals():
    return {"demo_mode": DEMO_MODE, "user_email": session.get("email")}


# ---------- Pages ----------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if "@" not in email:
            error = "Enter a valid email."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif DEMO_MODE:
            session["email"] = email
            session["user_id"] = "demo"
            return redirect(url_for("dashboard"))
        else:
            code, body = supa.sign_up(email, password)
            if code in (200, 201) and body.get("access_token"):
                session.update(email=email, user_id=body["user"]["id"],
                               token=body["access_token"])
                return redirect(url_for("dashboard"))
            if code in (200, 201):
                error = "Check your email to confirm your account, then log in."
            else:
                error = body.get("msg") or body.get("error_description") or "Sign up failed."
    return render_template("auth.html", mode="register", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if DEMO_MODE:
            if "@" in email and password:
                session["email"] = email
                session["user_id"] = "demo"
                return redirect(url_for("dashboard"))
            error = "Enter an email and password."
        else:
            code, body = supa.sign_in(email, password)
            if code == 200:
                session.update(email=email, user_id=body["user"]["id"],
                               token=body["access_token"])
                return redirect(url_for("dashboard"))
            error = "Invalid email or password."
    return render_template("auth.html", mode="login", error=error)


@app.route("/demo")
def demo():
    """One-click demo: no sign up needed."""
    session["email"] = "demo@habitforge.app"
    session["user_id"] = "demo"
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/app")
@login_required
def dashboard():
    return render_template("dashboard.html", page="dashboard")


@app.route("/notes")
@login_required
def notes():
    return render_template("notes.html", page="notes")


@app.route("/exercises")
def exercises():
    return render_template("exercises.html", page="exercises", muscles=MUSCLES)


# ---------- API ----------
@app.route("/api/exercises")
def api_exercises():
    return jsonify({"muscles": MUSCLES, "exercises": EXERCISES})


@app.route("/api/state", methods=["GET", "PUT"])
@login_required
def api_state():
    """In demo mode the browser keeps the data, so this just returns defaults.
    With Supabase, the state is stored in the user_state table."""
    if DEMO_MODE:
        return jsonify({"demo": True, "state": default_state()})

    uid, token = session.get("user_id"), session.get("token")
    if request.method == "PUT":
        ok = supa.save_state(uid, token, request.get_json(force=True))
        return jsonify({"ok": ok}), (200 if ok else 500)
    state = supa.get_state(uid, token) or default_state()
    return jsonify({"demo": False, "state": state})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "demo_mode": DEMO_MODE})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
