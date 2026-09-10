# Blocker Reminder Workflow — Production

**Status:** Active (production send mode)
**Activated:** 2026-09-09 10:39 IST
**Last correction:** 2026-09-10 12:06 IST — introduced `blockers.json` as the single source of truth; dashboard and Python script now both consume it; script sends via the connected Gmail on every scheduled run.
**Owner:** CEO Office (`sudeep@sionsemi.com`)

## Schedule
- **Cadence:** Monday to Friday at **09:00 Asia/Kolkata (IST)**
- **Cron:** `0 9 * * 1-5`
- **Timezone:** `Asia/Kolkata (+05:30)`
- **Schedule ID:** `scheduled-skill-3f62951f9f7e6a660aa317a06b8a340acbabc3ca`  *(unchanged)*

## Single source of truth — `blockers.json`
`blockers.json` at the repo root is the canonical list of blockers.
Both consumers read from it — there is no duplicate list anywhere:

| Consumer | How it reads |
|---|---|
| `dashboard.html` / `index.html` | Client-side `fetch('blockers.json')` on page load. The Home-tab blockers table, the "N OPEN" count-pill and the "N open" sub-headline all update from the JSON. |
| `build-personal-emails.py` | `json.load()` at the top of `main()` on every run. |

Editing `blockers.json` (adding a blocker, flipping a status to CLOSED, changing a target date, etc.) updates BOTH surfaces on the next dashboard page-load and the next 09:00 IST reminder run — no other files to edit.

## Send flow (every scheduled run)
1. Runner pulls the latest `main` of https://github.com/xtremesilica/xtremesilica-dashboard.
2. Runner executes `python3 build-personal-emails.py`.
3. The script:
   - Reads `blockers.json`.
   - Excludes any blocker whose status contains `CLOSED`, `COMPLETED`, `RESOLVED` or `DONE` (case-insensitive; compound like `RED · REOPENED` is included via the RED / REOPENED tokens).
   - Routes remaining blockers to each owner in the routing table below.
   - Skips owners with zero open blockers (per-owner, not global).
   - Sends via the connected Genspark Gmail (`gsk gmail send --from_account xtremesilica@gmail.com --skip_confirmation true`).

## Recipients

| Owner | Blocker IDs | To | BCC (through 2026-09-16 only) |
|---|---|---|---|
| Mr Basheer Boddikonda | B1, B2, B3, B4, B5, B6 | `ahmed@sionsemi.com` | `sudeep@sionsemi.com` |
| Mr Girish B V | B2, B3 | `girish@sionsemi.com` | `sudeep@sionsemi.com` |

**BCC auto-drop:** the BCC is added on every run only when the run date (Asia/Kolkata) is <= **2026-09-16**. From 2026-09-17 onward, no BCC.

## Filter — INCLUDE only these statuses
`OPEN` · `REOPENED` · `RED` · `AMBER` · `PENDING`

## Filter — EXCLUDE these statuses
`CLOSED` · `COMPLETED` · `RESOLVED` · `DONE`

## Content contract (verbatim, per CEO directive)
- **Intro:** `Dear {name}, following blockers are on your name, kindly check and do the needful on high priority.`
- **Footer:** `From the Office of CEO`
- **Dashboard URL:** intentionally omitted from the email body.
- **Preview banner:** none. Production sends never emit a preview banner.
- **Header timestamp:** computed dynamically in Asia/Kolkata at every render.

## Managing the workflow

| Action | Command |
|---|---|
| List scheduled workflows | `gsk schedule list` |
| Pause | `gsk schedule cancel scheduled-skill-3f62951f9f7e6a660aa317a06b8a340acbabc3ca --pause` |
| Resume | `gsk schedule cancel scheduled-skill-3f62951f9f7e6a660aa317a06b8a340acbabc3ca --resume` |
| Delete permanently | `gsk schedule cancel scheduled-skill-3f62951f9f7e6a660aa317a06b8a340acbabc3ca` |
| Recent runs | `gsk workflow runs --id scheduled-skill-3f62951f9f7e6a660aa317a06b8a340acbabc3ca` |
| One run's output | `gsk workflow output --id <run_id>` |

## Change log
- **2026-09-10 12:06 IST** — Introduced `blockers.json` as the single source of truth for both the dashboard and the reminder emails. Corrected the opening docstring of `build-personal-emails.py` (Basheer B1–B6). Replaced the literal `\u2192` escape with the real → character. Skill updated so every scheduled run executes `python3 build-personal-emails.py` (which does filter, render and send in one call). Schedule unchanged.
- **2026-09-10 11:39 IST** — Removed dry-run / preview language from the skill; header timestamp made dynamic; PREVIEW banner removed from production emails.
- **2026-09-09 10:39 IST** — Production workflow activated. Mon-Fri 09:00 IST. First-week BCC to `sudeep@sionsemi.com` (auto-drops after 2026-09-16).
