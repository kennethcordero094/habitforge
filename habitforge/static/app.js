/* HabitForge front-end. One file, three sections:
   1) helpers  2) Store (saves data)  3) one init function per page */

// ---------- 1) Helpers ----------
const $ = (sel, el = document) => el.querySelector(sel);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const uid = () => Math.random().toString(36).slice(2, 9);
const pad = (n) => String(n).padStart(2, "0");
const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const parseIso = (s) => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
const weekdayIdx = (d) => (d.getDay() + 6) % 7; // Monday = 0
const DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

const body = document.body;
const IS_DEMO = body.dataset.demo === "1";
const IS_AUTH = body.dataset.auth === "1";

// ---------- 2) Store ----------
const Store = {
  state: null,
  exercises: [],
  muscles: [],
  _timer: null,

  get key() { return "habitforge:" + body.dataset.email; },

  async init() {
    const ex = await (await fetch("/api/exercises")).json();
    this.exercises = ex.exercises;
    this.muscles = ex.muscles;
    if (!IS_AUTH) return;

    // Demo mode: data lives in this browser. Otherwise it comes from Supabase via Flask.
    if (IS_DEMO) {
      try { this.state = JSON.parse(localStorage.getItem(this.key)); } catch (e) { this.state = null; }
    }
    if (!this.state) {
      const res = await (await fetch("/api/state")).json();
      this.state = res.state;
    }
    this.state.checks = this.state.checks || {};
    this.state.notes = this.state.notes || [];
  },

  save() {
    if (IS_DEMO) {
      try { localStorage.setItem(this.key, JSON.stringify(this.state)); } catch (e) { /* storage full or blocked */ }
      return;
    }
    clearTimeout(this._timer);
    this._timer = setTimeout(() => {
      fetch("/api/state", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.state),
      });
    }, 400);
  },

  exercise(id) { return this.exercises.find((e) => e.id === id); },
  planFor(date) { return (this.state.plan[String(weekdayIdx(date))] || []).filter((id) => this.exercise(id)); },
  check(dateStr) {
    if (!this.state.checks[dateStr]) this.state.checks[dateStr] = { habits: [], exercises: [] };
    return this.state.checks[dateStr];
  },

  // How much of a day is finished: {done, total}
  progress(date) {
    const c = this.state.checks[iso(date)] || { habits: [], exercises: [] };
    const habitIds = this.state.habits.map((h) => h.id);
    const planIds = this.planFor(date);
    const done = c.habits.filter((id) => habitIds.includes(id)).length +
                 c.exercises.filter((id) => planIds.includes(id)).length;
    return { done, total: habitIds.length + planIds.length };
  },
};

// ---------- 3a) Dashboard ----------
function initDashboard() {
  const today = new Date();
  let selected = iso(today);
  let view = new Date(today.getFullYear(), today.getMonth(), 1);
  let editing = false;

  const renderCalendar = () => {
    $("#month-label").textContent = view.toLocaleString("en-US", { month: "long", year: "numeric" });
    const first = new Date(view.getFullYear(), view.getMonth(), 1);
    const daysInMonth = new Date(view.getFullYear(), view.getMonth() + 1, 0).getDate();
    let html = "";
    for (let i = 0; i < weekdayIdx(first); i++) html += `<span class="cal-day blank"></span>`;
    for (let d = 1; d <= daysInMonth; d++) {
      const date = new Date(view.getFullYear(), view.getMonth(), d);
      const ds = iso(date);
      const p = Store.progress(date);
      let dot = "";
      if (p.total && p.done >= p.total) dot = `<i class="dot dot-full"></i>`;
      else if (p.done > 0) dot = `<i class="dot dot-part"></i>`;
      const cls = ["cal-day", ds === iso(today) ? "today" : "", ds === selected ? "selected" : ""].join(" ");
      html += `<button class="${cls}" data-date="${ds}">${d}${dot}</button>`;
    }
    $("#cal-days").innerHTML = html;
  };

  const renderStats = () => {
    // Streak: consecutive days (ending today or yesterday) with at least one thing done
    let streak = 0;
    const cursor = new Date(today);
    if (Store.progress(cursor).done === 0) cursor.setDate(cursor.getDate() - 1);
    while (Store.progress(cursor).done > 0) { streak++; cursor.setDate(cursor.getDate() - 1); }

    // Workouts finished this week (Mon-Sun)
    const monday = new Date(today); monday.setDate(today.getDate() - weekdayIdx(today));
    let workouts = 0;
    for (let i = 0; i < 7; i++) {
      const d = new Date(monday); d.setDate(monday.getDate() + i);
      const planIds = Store.planFor(d);
      const c = Store.state.checks[iso(d)];
      if (planIds.length && c && planIds.every((id) => c.exercises.includes(id))) workouts++;
    }
    const tp = Store.progress(today);
    const pct = tp.total ? Math.round((tp.done / tp.total) * 100) : 0;
    $("#stats").innerHTML = `
      <div class="stat"><b>${streak}</b><span>Day streak</span></div>
      <div class="stat"><b>${pct}%</b><span>Today complete</span></div>
      <div class="stat"><b>${workouts}</b><span>Workouts finished this week</span></div>`;
  };

  const renderDay = () => {
    const date = parseIso(selected);
    const c = Store.check(selected);
    const planIds = Store.planFor(date);
    const dayName = DAY_NAMES[weekdayIdx(date)];

    $("#day-title").textContent = date.toLocaleString("en-US", { month: "long", day: "numeric", year: "numeric" });
    $("#day-sub").textContent = dayName + (selected === iso(today) ? " (today)" : "");

    const p = Store.progress(date);
    const pct = p.total ? Math.round((p.done / p.total) * 100) : 0;
    $("#day-bar").style.width = pct + "%";
    $("#day-ring").style.background = `conic-gradient(var(--accent) ${pct * 3.6}deg, var(--panel-2) 0)`;
    $("#day-ring").innerHTML = `<span>${pct}%</span>`;

    // Habits
    $("#habit-list").innerHTML = Store.state.habits.length
      ? Store.state.habits.map((h) => `
        <li class="${c.habits.includes(h.id) ? "done" : ""}">
          <input type="checkbox" data-habit="${h.id}" ${c.habits.includes(h.id) ? "checked" : ""}>
          <span class="label">${esc(h.name)}</span>
          <button class="x-btn" data-del-habit="${h.id}" aria-label="Delete habit">&times;</button>
        </li>`).join("")
      : `<li class="empty">No habits yet. Add one below.</li>`;

    // Workout
    $("#workout-title").textContent = `${dayName} workout`;
    $("#workout-list").innerHTML = planIds.length
      ? planIds.map((id) => {
          const e = Store.exercise(id);
          const done = c.exercises.includes(id);
          return `<li class="${done ? "done" : ""}">
            <input type="checkbox" data-ex="${id}" ${done ? "checked" : ""}>
            <span class="label">${esc(e.name)}<small>${esc(e.muscle)} &middot; ${esc(e.scheme)}</small></span>
            ${editing ? `<button class="x-btn" data-del-ex="${id}" aria-label="Remove">&times;</button>` : ""}
          </li>`;
        }).join("")
      : `<li class="empty">Rest day. Use "Edit plan" to add exercises for ${dayName}s.</li>`;

    $("#plan-editor").hidden = !editing;
    $("#edit-plan-btn").textContent = editing ? "Done" : "Edit plan";
    $("#plan-hint").textContent = `Changes apply to every ${dayName}.`;
  };

  const renderAll = () => { renderCalendar(); renderStats(); renderDay(); };

  // Calendar interactions
  $("#cal-days").addEventListener("click", (e) => {
    const b = e.target.closest("[data-date]");
    if (b) { selected = b.dataset.date; renderAll(); }
  });
  $("#prev-month").onclick = () => { view = new Date(view.getFullYear(), view.getMonth() - 1, 1); renderCalendar(); };
  $("#next-month").onclick = () => { view = new Date(view.getFullYear(), view.getMonth() + 1, 1); renderCalendar(); };
  $("#go-today").onclick = () => {
    selected = iso(today);
    view = new Date(today.getFullYear(), today.getMonth(), 1);
    renderAll();
  };

  // Toggle habits / exercises
  const toggle = (arr, id) => { const i = arr.indexOf(id); i >= 0 ? arr.splice(i, 1) : arr.push(id); };
  document.addEventListener("change", (e) => {
    const c = Store.check(selected);
    if (e.target.dataset.habit) toggle(c.habits, e.target.dataset.habit);
    else if (e.target.dataset.ex) toggle(c.exercises, e.target.dataset.ex);
    else return;
    Store.save(); renderAll();
  });

  // Delete habit / remove exercise from plan
  document.addEventListener("click", (e) => {
    const h = e.target.closest("[data-del-habit]");
    if (h) {
      Store.state.habits = Store.state.habits.filter((x) => x.id !== h.dataset.delHabit);
      Store.save(); renderAll();
    }
    const x = e.target.closest("[data-del-ex]");
    if (x) {
      const key = String(weekdayIdx(parseIso(selected)));
      Store.state.plan[key] = (Store.state.plan[key] || []).filter((id) => id !== x.dataset.delEx);
      Store.save(); renderAll();
    }
  });

  // Add habit
  $("#habit-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const name = $("#habit-input").value.trim();
    if (!name) return;
    Store.state.habits.push({ id: uid(), name });
    $("#habit-input").value = "";
    Store.save(); renderAll();
  });

  // Plan editor
  $("#plan-muscle").innerHTML = Store.muscles.map((m) => `<option>${esc(m)}</option>`).join("");
  const fillExercises = () => {
    const m = $("#plan-muscle").value;
    $("#plan-exercise").innerHTML = Store.exercises.filter((x) => x.muscle === m)
      .map((x) => `<option value="${x.id}">${esc(x.name)}</option>`).join("");
  };
  $("#plan-muscle").onchange = fillExercises;
  fillExercises();
  $("#edit-plan-btn").onclick = () => { editing = !editing; renderDay(); };
  $("#plan-add").onclick = () => {
    const id = $("#plan-exercise").value;
    const key = String(weekdayIdx(parseIso(selected)));
    Store.state.plan[key] = Store.state.plan[key] || [];
    if (!Store.state.plan[key].includes(id)) Store.state.plan[key].push(id);
    Store.save(); renderAll();
  };

  renderAll();
}

// ---------- 3b) Notes ----------
function initNotes() {
  const render = () => {
    const notes = Store.state.notes;
    $("#notes-empty").hidden = notes.length > 0;
    $("#notes-grid").innerHTML = notes.map((n) => {
      const done = n.items.filter((i) => i.done).length;
      return `<section class="card note" data-note="${n.id}">
        <h3>${esc(n.title)}<button class="x-btn" data-del-note="${n.id}" aria-label="Delete note">&times;</button></h3>
        <div class="progress">${done} of ${n.items.length} done</div>
        <ul class="checklist">
          ${n.items.map((i) => `<li class="${i.done ? "done" : ""}">
            <input type="checkbox" data-item="${i.id}" ${i.done ? "checked" : ""}>
            <span class="label">${esc(i.text)}</span>
            <button class="x-btn" data-del-item="${i.id}" aria-label="Delete item">&times;</button>
          </li>`).join("") || `<li class="empty">No items yet.</li>`}
        </ul>
        <form class="inline-form" data-add-item="${n.id}">
          <input placeholder="Add a to-do..." maxlength="120" required>
          <button class="btn btn-small" type="submit">Add</button>
        </form>
      </section>`;
    }).join("");
  };

  const findNote = (el) => Store.state.notes.find((n) => n.id === el.closest("[data-note]").dataset.note);

  $("#note-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const title = $("#note-title").value.trim();
    if (!title) return;
    Store.state.notes.unshift({ id: uid(), title, items: [] });
    $("#note-title").value = "";
    Store.save(); render();
  });

  $("#notes-grid").addEventListener("submit", (e) => {
    const form = e.target.closest("[data-add-item]");
    if (!form) return;
    e.preventDefault();
    const input = form.querySelector("input");
    const text = input.value.trim();
    if (!text) return;
    findNote(form).items.push({ id: uid(), text, done: false });
    Store.save(); render();
  });

  $("#notes-grid").addEventListener("change", (e) => {
    if (!e.target.dataset.item) return;
    const item = findNote(e.target).items.find((i) => i.id === e.target.dataset.item);
    item.done = e.target.checked;
    Store.save(); render();
  });

  $("#notes-grid").addEventListener("click", (e) => {
    const delItem = e.target.closest("[data-del-item]");
    if (delItem) {
      const note = findNote(delItem);
      note.items = note.items.filter((i) => i.id !== delItem.dataset.delItem);
      Store.save(); render(); return;
    }
    const delNote = e.target.closest("[data-del-note]");
    if (delNote && confirm("Delete this note?")) {
      Store.state.notes = Store.state.notes.filter((n) => n.id !== delNote.dataset.delNote);
      Store.save(); render();
    }
  });

  render();
}

// ---------- 3c) Exercises library ----------
function initExercises() {
  let muscle = "All";
  let query = "";

  $("#chips").innerHTML = ["All", ...Store.muscles]
    .map((m) => `<button class="chip ${m === "All" ? "active" : ""}" data-muscle="${esc(m)}">${esc(m)}</button>`).join("");

  const render = () => {
    const list = Store.exercises.filter((e) =>
      (muscle === "All" || e.muscle === muscle) &&
      (e.name + " " + e.muscle + " " + e.equipment).toLowerCase().includes(query));

    $("#ex-grid").innerHTML = list.map((e) => `
      <article class="card ex">
        <span class="tag">${esc(e.muscle)}</span>
        <h3>${esc(e.name)}</h3>
        <div class="scheme">${esc(e.scheme)}</div>
        <div class="muted">${esc(e.equipment)}</div>
        <p class="muted">${esc(e.tip)}</p>
        ${IS_AUTH ? `<form class="inline-form" data-add="${e.id}">
          <select>${DAY_NAMES.map((d, i) => `<option value="${i}">${d}</option>`).join("")}</select>
          <button class="btn btn-small" type="submit">Add to plan</button>
        </form>` : ""}
      </article>`).join("") || `<p class="muted">No exercises match.</p>`;
  };

  $("#chips").addEventListener("click", (e) => {
    const b = e.target.closest("[data-muscle]");
    if (!b) return;
    muscle = b.dataset.muscle;
    document.querySelectorAll(".chip").forEach((c) => c.classList.toggle("active", c === b));
    render();
  });
  $("#ex-search").addEventListener("input", (e) => { query = e.target.value.trim().toLowerCase(); render(); });

  $("#ex-grid").addEventListener("submit", (e) => {
    const form = e.target.closest("[data-add]");
    if (!form) return;
    e.preventDefault();
    const day = form.querySelector("select").value;
    const plan = Store.state.plan[day] = Store.state.plan[day] || [];
    const btn = form.querySelector("button");
    if (!plan.includes(form.dataset.add)) plan.push(form.dataset.add);
    Store.save();
    btn.textContent = "Added!";
    setTimeout(() => (btn.textContent = "Add to plan"), 1200);
  });

  render();
}

// ---------- Start ----------
(async function () {
  const page = body.dataset.page;
  if (!page) return;
  await Store.init();
  if (page === "dashboard") initDashboard();
  if (page === "notes") initNotes();
  if (page === "exercises") initExercises();
})();
