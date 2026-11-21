# HabitForge

A habit tracker with a calendar, a weekly workout plan and to-do notes.
Built with Python (Flask), HTML, CSS, JavaScript, Supabase, GitHub and Render.

It runs in **demo mode** by default (no database needed). Your data is saved in the browser.
When you add Supabase keys, it switches to real accounts and cloud storage automatically.

---

## What is inside

```
habitforge/
├── app.py              Flask server: pages + API
├── supa.py             Small Supabase helper (only used with keys)
├── schema.sql          Database table to paste into Supabase
├── requirements.txt    Python packages
├── render.yaml         Render deploy settings
├── data/exercises.py   100 exercises (10 muscle groups x 10)
├── templates/          HTML pages (Jinja)
└── static/
    ├── style.css       Dark green theme
    └── app.js          Calendar, tracker, notes, exercise library
```

---

## Step 1: Run it on your computer (demo mode)

1. Install Python 3.10+ from python.org (tick "Add Python to PATH").
2. Open the `habitforge` folder in VS Code.
3. Open the terminal (Ctrl + `) and run:

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux
pip install -r requirements.txt
python app.py
```

4. Open http://127.0.0.1:5000 and click **Try the demo**.

No Supabase keys = demo mode. Everything works and saves in your browser.

---

## Step 2: Put the code on GitHub

1. Create an account at github.com and click **New repository**. Name it `habitforge`. Leave it empty.
2. In your project terminal:

```bash
git init
git add .
git commit -m "HabitForge first version"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/habitforge.git
git push -u origin main
```

---

## Step 3: Deploy on Render (still demo mode)

1. Go to render.com and sign in with GitHub.
2. **New +** then **Web Service**, and pick your `habitforge` repo.
3. Settings:
   - Runtime: **Python 3**
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Under **Environment**, add `SECRET_KEY` with any long random text.
5. Click **Create Web Service**. After a few minutes you get a link like `https://habitforge-xxxx.onrender.com`.

Free Render services sleep when idle, so the first load can take about 50 seconds.

---

## Step 4: Add Supabase (real accounts and cloud saving)

1. Go to supabase.com, create a project, and wait until it is ready.
2. Open **SQL Editor**, then **New query**. Paste everything from `schema.sql` and click **Run**.
3. Open **Project Settings**, then **API**. Copy:
   - **Project URL**
   - **anon public** key (never use the service_role key in this app)
4. For easy testing, go to **Authentication**, then **Providers**, then **Email**, and turn off **Confirm email**. Turn it back on later for a real launch.
5. In Render, open your service, then **Environment**, and add:
   - `SUPABASE_URL` = your Project URL
   - `SUPABASE_ANON_KEY` = your anon key
6. Render redeploys. Visit `/health`: it should say `"demo_mode": false`.

To test Supabase locally, set the same two variables before `python app.py`:

```bash
set SUPABASE_URL=https://xxxx.supabase.co
set SUPABASE_ANON_KEY=your-anon-key
python app.py
```

Each user's data is stored in one row of `user_state`, protected by row level security so people only see their own data.

---

## How it works

- **Calendar**: pick any date; dots show full or partial days.
- **Habits** (the main feature): add, tick and delete daily habits and keep your streak.
- **Workout plan**: a plan for each weekday (Mon to Sun). Edit it on the tracker or add from the Exercises page.
- **Notes**: create notes, each with its own to-do list.
- **Streak**: counts consecutive days with at least one thing done.

## Ideas to add next

- Weight and reps logging per exercise
- Charts of weekly progress
- Dark/light theme toggle
- Password reset using Supabase
