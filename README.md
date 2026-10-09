# 🧭 Career Compass AI - Smart Career & Skill Development Platform

A Streamlit web app that helps university students and fresh graduates **assess their skills, compare career paths,
find skill gaps, follow a personalised learning roadmap and track progress** - with PDF and CSV exports.

> **Honest labelling:** recommendations come from a *transparent rule-based engine*, **not machine learning**.
> No suitable, documented dataset is bundled, so no ML model is claimed (see [Why no ML?](#why-no-machine-learning)).
> All demo data is **fictional**.

## Features
| Area | What it does |
|---|---|
| Dashboard | Metric cards, top careers, skill-gap summary, charts, recent activity |
| Profile | Name, education, field, technical/soft skills, interests, goal, learning areas (validated, saved in SQLite) |
| Skill Assessment | 9 skills rated 1-5, edit/re-save, reset, CSV export, strengths and improvement areas |
| Career Explorer | 5 careers with overview, required skills, gap analysis, projects, tools; search and category filter |
| Learning Roadmap | Ordered modules, exercises, mini-projects, portfolio projects; checkboxes saved in SQLite; priority flags from your gaps |
| Analytics | Plotly: skill bars, career comparison, skill gap, radar match overview, roadmap progress |
| Career Report | PDF (profile, results, careers, methodology, gaps, roadmap, next steps) + CSV exports |
| Help / About | Usage, methodology, privacy, limitations |

## Project structure
```
career_compass_ai/
├── app.py                 # entry point: sidebar, navigation, routing
├── careers.py             # editable catalogue: skills, careers, roadmaps
├── recommendations.py     # rule-based matching + skill gaps
├── assessment.py          # score validation, summaries, CSV
├── roadmap.py             # roadmap building + priority flags
├── database.py            # SQLite schema + parameterised queries
├── report_generator.py    # ReportLab PDF
├── charts.py              # Plotly figures
├── ui.py  utils.py  demo.py
├── views/                 # one module per page (see note)
├── data/sample_skills.csv # fictional demo ratings
├── models/                # reserved (no trained model is used)
├── tests/                 # pytest suite
└── requirements.txt
```
*Note:* the page modules live in `views/`, not `pages/`. Streamlit auto-creates extra sidebar entries for any folder
named `pages/` next to `app.py`, which would duplicate the navigation.

## Run locally (VS Code)
```bash
cd career_compass_ai
python -m venv .venv
.venv\Scripts\activate            # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501. Click **Profile → Load fictional demo profile** to explore instantly.
In VS Code: install the *Python* extension, press `Ctrl+Shift+P` → *Python: Select Interpreter* → pick `.venv`.

## Run the tests
```bash
pip install -r requirements-dev.txt
pytest -q
```
`test_app_smoke.py` opens every page with Streamlit's `AppTest`; it is skipped automatically if Streamlit is missing.

## How recommendations work
For each career the catalogue lists required skills, a required level (1-5) and an importance weight (1-3).
`coverage = min(your rating / required level, 1)`; the skill score is the weighted average coverage × 100. Careers you
list as interests get a flat +5 (capped at 100). This is guidance for exploration. The required levels and weights are
editorial estimates, not statistics. Edit them in `careers.py`.

### Why no machine learning?
A trustworthy model needs labelled data linking real skill profiles to real career outcomes, plus a documented source
and bias review. None is bundled, and inventing one would produce scores that look scientific but are not. If you add a
real dataset later, train it in a separate notebook, compare against the rule-based baseline, evaluate on a held-out
test set, save with Joblib in `models/`, and document its limitations before claiming ML.

## Upload to GitHub
```bash
git init
git add .
git commit -m "Career Compass AI"
git branch -M main
git remote add origin https://github.com/<your-username>/career-compass-ai.git
git push -u origin main
```
`.gitignore` already excludes local databases.

## Deploy on Streamlit Community Cloud
1. Push the repo to GitHub. 2. Go to https://share.streamlit.io → *New app* → select the repo, branch `main`, main file `app.py`.
3. Deploy. Dependencies are read from `requirements.txt`.

### Persistent storage (important)
SQLite is a **local file**. On Streamlit Community Cloud the container filesystem is not guaranteed to persist: restarts,
redeploys or inactivity can erase `data/career_compass.db`. Choose one:
- **Portfolio demo (recommended for Streamlit Cloud):** accept resets; the fictional demo profile can be reloaded in one click.
- **Persistent disk:** host on a platform with a mounted volume (e.g. Render, Railway, Fly.io, or a VPS) and set
  `CAREER_COMPASS_DB=/data/career_compass.db` to a path on that volume. Check the provider's current plan limits.
- **Hosted database:** replace `database.py` with a Postgres/Turso/Supabase implementation (all SQL is isolated in that one file).

### Shared deployments
There is no login. On a public deployment every visitor shares one database and can see all profile display names in
the selector. Do not enter real personal data on a public demo; add authentication before real use.

## Security and privacy
Parameterised SQL everywhere · input validation · user text is escaped in PDFs and in HTML cards · no passwords or ID
numbers stored · CSV cells are not formula-injected (assessment export contains only fixed skill names).

## Implemented features
Everything in the feature table above, plus profile switching and deletion, empty states, confirmation before reset/delete,
and 35+ automated tests.

## Known limitations
- Ratings are self-assessments; required levels are editorial estimates; matches are not predictions of job success.
- Five careers and nine skills (extend `careers.py`).
- No authentication or multi-user isolation; SQLite is not suited to heavy concurrent use.
- Report and roadmap content is English only.
