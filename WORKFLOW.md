# Blocker Reminder Workflow — Production

**Status:** Active (production send mode)
**Activated:** 2026-09-09 10:39 IST
**Last correction:** 2026-09-10 11:39 IST — removed any dry-run / preview language from the skill definition; workflow is confirmed to actually send real emails on every scheduled run.
**Owner:** CEO Office (`sudeep@sionsemi.com`)

## Schedule
- **Cadence:** Monday to Friday at **09:00 Asia/Kolkata (IST)**
- **Cron:** `0 9 * * 1-5`
- **Timezone:** `Asia/Kolkata (+05:30)`
- **Schedule ID:** `scheduled-skill-3f62951f9f7e6a660aa317a06b8a340acbabc3ca`

## Send mode — PRODUCTION
This is a real-send workflow. Every scheduled run calls `gsk gmail send --skip_confirmation true` and delivers the digest to the routing table below. It is not a preview and not a dry run. There is no confirmation gate, no test-preview banner, no re-routing.

## Recipients

| Owner | To | BCC (through 2026-09-16 only) |
|---|---|---|
| Mr Basheer Boddikonda | `ahmed@sionsemi.com` | `sudeep@sionsemi.com` |
| Mr Girish B V | `girish@sionsemi.com` | `sudeep@sionsemi.com` |

**BCC auto-drop:** the BCC is included on every run only when the run date (Asia/Kolkata) is <= **2026-09-16**. From 2026-09-17 onward, no BCC.

## Sending account
- **From:** `xtremesilica@gmail.com` (Genspark-connected Gmail)
- **Transport:** `gsk gmail send` with `--skip_confirmation true`
- **Subject format:** `Daily blocker digest — {N} open · {DD-Mon-YYYY}`

## Blocker filter

**INCLUDE** (send) a blocker if its status contains ANY of:
- `OPEN` · `REOPENED` · `RED` · `AMBER` · `PENDING`

**EXCLUDE** (skip) a blocker if its status contains ANY of:
- `CLOSED` · `COMPLETED` · `RESOLVED` · `DONE`

Compound statuses (e.g. `RED · REOPENED`) match on either token; case-insensitive.

## Skip-empty rule — the ONLY reason a send is skipped
If, after the include/exclude filter, an owner has zero open blockers, the workflow does NOT send an email to that owner on that run. The other owner still receives their digest if they have any open blockers. Neither owner receives a "you're clear" notification — silence indicates zero open. This is a per-owner skip, not a global skip.

## Content contract (verbatim, per CEO directive)
- **Intro:** `Dear {name}, following blockers are on your name, kindly check and do the needful on high priority.`
- **Footer:** `From the Office of CEO`
- **Dashboard URL:** intentionally omitted from the email body.

## Source of truth
- Repo: https://github.com/xtremesilica/xtremesilica-dashboard (branch: `main`)
- Machine-readable blockers: top of `build-personal-emails.py` (the `B1..B6` dicts)
- Human-readable blockers: blockers table on the Home tab of `dashboard.html`

Every run pulls latest `main` before rendering. There is no cache — a status flip in the repo is reflected in the next 09:00 IST send.

## Continuation policy
Reminders continue daily until each blocker is closed. The workflow itself remains active indefinitely — pause or cancel it from the Genspark Scheduled Skills page or via `gsk schedule cancel`.

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
- **2026-09-10 11:39 IST** — Correction. Rewrote the skill definition to remove any language that could be read as a dry-run or preview instruction. Sent today's missed reminder manually to both owners (Basheer -> ahmed@sionsemi.com; Girish -> girish@sionsemi.com; BCC sudeep@sionsemi.com). Schedule unchanged.
- **2026-09-09 10:39 IST** — Production workflow activated. Mon-Fri 09:00 IST. First-week BCC to `sudeep@sionsemi.com` (auto-drops after 2026-09-16).
