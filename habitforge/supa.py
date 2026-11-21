"""Tiny Supabase client using plain HTTP (no extra SDK needed).

Only used when SUPABASE_URL and SUPABASE_ANON_KEY are set.
If they are missing, the app runs in DEMO MODE and this file is never called.
"""
import os
import requests

URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
KEY = os.environ.get("SUPABASE_ANON_KEY", "")


def enabled():
    return bool(URL and KEY)


def _headers(token=None):
    return {
        "apikey": KEY,
        "Authorization": f"Bearer {token or KEY}",
        "Content-Type": "application/json",
    }


def sign_up(email, password):
    r = requests.post(f"{URL}/auth/v1/signup", json={"email": email, "password": password},
                      headers=_headers(), timeout=15)
    return r.status_code, r.json()


def sign_in(email, password):
    r = requests.post(f"{URL}/auth/v1/token?grant_type=password",
                      json={"email": email, "password": password},
                      headers=_headers(), timeout=15)
    return r.status_code, r.json()


def get_state(user_id, token):
    r = requests.get(f"{URL}/rest/v1/user_state",
                     params={"user_id": f"eq.{user_id}", "select": "data"},
                     headers=_headers(token), timeout=15)
    if r.status_code == 200 and r.json():
        return r.json()[0]["data"]
    return None


def save_state(user_id, token, data):
    headers = _headers(token)
    headers["Prefer"] = "resolution=merge-duplicates"
    r = requests.post(f"{URL}/rest/v1/user_state",
                      json={"user_id": user_id, "data": data},
                      headers=headers, timeout=15)
    return r.status_code in (200, 201, 204)
