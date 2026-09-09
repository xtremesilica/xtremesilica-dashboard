# Blocker Reminder Workflow — Production

**Status:** Active
**Activated:** 2026-09-09 10:39 IST
**Owner:** CEO Office (`sudeep@sionsemi.com`)

## Schedule
- **Cadence:** Monday to Friday at **09:00 Asia/Kolkata (IST)**
- **Cron:** `0 9 * * 1-5` (5-field, minute-hour-DoM-month-DoW)
- **Weekends:** excluded (no Sat/Sun runs)
- **Timezone:** `Asia/Kolkata (+05:30)`

## Recipients (production routing)

| Owner | Email | Blockers |
|---|---|---|
| Mr Basheer Boddikonda | `ahmed@sionsemi.com` | B1, B2, B3, B4, B5, B6 (owner or co-owner) |
| Mr Girish B V | `girish@sionsemi.com` | B2, B3 (co-owner) |

**BCC (first week only, until 2026-09-16):** `sudeep@sionsemi.com` — auto-dropped after that date.

## Sending account
- **From:** `xtremesilica@gmail.com` (Genspark-connected Gmail)
- **Transport:** `gsk gmail send` (headless, `--skip_confirmation true`)
- **Subject format:** `Daily blocker digest — {N} open · {DD-Mon-YYYY}`

## Blocker filter — CRITICAL

**INCLUDE** (send) a blocker if its status contains ANY of:
- `OPEN` · `REOPENED` · `RED` · `AMBER` · `PENDING`

**EXCLUDE** (skip) a blocker if its status contains ANY of:
- `CLOSED` · `COMPLETED` · `RESOLVED` · `DONE`

Compound statuses (e.g. `RED · REOPENED`) match on either word and are **included**.

## Skip-empty rule
If, after filtering, an owner has **zero open blockers**, the workflow does NOT send an email to that owner on that run. This means:
- Basheer receives an email until his last blocker among B1-B6 is closed.
- Girish receives an email until BOTH B2 and B3 are closed.
- Neither owner receives a "you're clear" notification — silence indicates zero open.

## Content contract (verbatim, per CEO directive)
- **Intro:** *Dear {name}, following blockers are on your name, kindly check and do the needful on high priority.*
- **Footer:** *From the Office of CEO*
- **Dashboard URL:** intentionally omitted from email body.

## Source of truth
- Repo: https://github.com/xtremesilica/xtremesilica-dashboard (branch: `main`)
- Machine-readable blockers: top of `build-personal-emails.py` (the `B1..B6` dicts)
- Human-readable blockers: blockers table on the Home tab of `dashboard.html`

Every run pulls latest `main` before rendering. There is NO cache — a status flip in the repo is reflected in the next 09:00 IST send.

## Continuation policy
Reminders continue **daily until each blocker is closed**. The workflow itself remains active indefinitely — pause or cancel it from the Genspark Scheduled Skills page.

## Managing the workflow

| Action | Command |
|---|---|
| List scheduled workflows | `gsk schedule list` |
| Pause | `gsk schedule cancel <id> --pause` |
| Resume | `gsk schedule cancel <id> --resume` |
| Delete permanently | `gsk schedule cancel <id>` |
| Recent runs | `gsk workflow runs --id <id>` |
| One run's output | `gsk workflow output --id <run_id>` |

## Test-preview cadence (superseded)
Test previews were routed to `sudeep@sionsemi.com` on 2026-09-09 09:19 IST (Gmail message IDs `1a08485473245f27` and `1a084854af82333d`) and approved on 2026-09-09 10:39 IST. The test route is now retired; production routing is live.

## Change log
- **2026-09-09 10:39 IST** — Production workflow activated. Mon-Fri 09:00 IST. First-week BCC to `sudeep@sionsemi.com` (auto-drops 2026-09-16).
