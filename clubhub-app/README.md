# ClubHub · Events Module Prototype

A lightweight starter implementation of association/club software that focuses on event logistics. It delivers a minimal-yet-extensible Flask backend plus HTML UI so we can iterate quickly toward richer membership tooling (emails, dues, roles, workflows).

## Feature Highlights
- **Event publishing** – capture title, description, location, schedule, deadline, and capacity.
- **Member sign-ups** – attendees self-register with name/email; capacity & deadline guardrails enforced server-side.
- **Dashboard view** – clean list of upcoming events with metadata summaries.
- **Detail & roster views** – track attendees and highlight seat availability in real time.
- **REST seeds** – `/api/events` returns JSON for integration or future SPA work.
- **Developer ergonomics** – SQLite persistence, configurable secrets, and a `flask seed-events` helper for demo data.

## Project Layout
```
clubhub-app/
├── app.py                # Flask entrypoint
├── requirements.txt      # App-specific dependencies
├── clubhub/
│   ├── __init__.py       # Application factory + CLI helpers
│   ├── models.py         # Event & registration ORM models
│   └── views.py          # HTTP + JSON endpoints
├── templates/            # Jinja templates (base/index/events/*)
├── static/styles.css     # Minimal design system
├── notes.md              # Running work log
└── README.md             # This document
```

## Getting Started
1. **Install dependencies**
   ```bash
   cd clubhub-app
   python3 -m venv .venv && source .venv/bin/activate  # optional but recommended
   pip install -r requirements.txt
   ```
2. **Set environment variables (optional)**
   - `CLUBHUB_SECRET_KEY` – overrides the default dev secret.
   - `CLUBHUB_DATABASE_URI` – point to a different database if needed.
3. **Initialize demo data (optional)**
   ```bash
   python3 -m flask --app app seed-events
   ```
4. **Run the dev server**
   ```bash
   python3 -m flask --app app run --debug
   ```
5. Open http://127.0.0.1:5000 to create and manage events.

## API Surface
| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/events` | `GET` | Returns JSON array of events (`id`, schedule, location, capacity metadata). |

## Next Steps & Extensions
- Add authenticated dashboards and member roles.
- Layer in outbound email workflows (e.g., reminders, recap digests).
- Build dues/subscription management plus richer membership profiles.
- Introduce event tags, RSVP approvals, waitlists, and exports.
- Wrap the REST API with a modern frontend or mobile client.

## Notes & Traceability
See `notes.md` for a chronological log of decisions, commands, and validation steps executed while building this prototype.
