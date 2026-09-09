# Xtremesilica Executive Dashboard

Single-file, self-contained executive dashboard for **Xtremesilica** — a
semiconductor-IP company with a 41-IP portfolio across AI compute, high-speed
connectivity, memory & interconnect, RISC-V CPU cores, and space / strategic
silicon.

**Live view (GitHub Pages, if enabled):**
`https://xtremesilica.github.io/xtremesilica-dashboard/`

**Repo:** https://github.com/xtremesilica/xtremesilica-dashboard

---

## What's inside

| File | Purpose |
|---|---|
| `index.html` | The dashboard — open this directly in a browser (identical to `dashboard.html`) |
| `dashboard.html` | Canonical source of the dashboard (mirrored to `index.html` at every commit) |
| `blocker-email-basheer.html` | Daily blocker digest email (B1-B6) addressed to Basheer |
| `blocker-email-girish.html` | Daily blocker digest email (B2-B3 only) addressed to Girish |
| `blocker-email-template.html` | Generic per-recipient template |
| `build-personal-emails.py` | Regenerates the two personalised digests from the blocker list |
| `model.json` / `model2.json` / `model_v3.json` / `model_v4.json` | Underlying revenue model snapshots (JSON) |
| `WORKFLOW-SETUP.md` | Setup notes for the daily digest cadence |

---

## Dashboard tabs

The dashboard is a **single self-contained HTML file** with hash-based routing.
Four tabs:

1. **Home** — executive summary, hero KPIs, blockers B1-B6, monthly cash-flow
   projection Sep-2026 → Mar-2030, revenue-per-IP table for all 41 IPs.
2. **Gantt** — 42-month development + go-to-market timeline. Diamonds mark
   FPGA-proof dates; the red line marks *today*.
3. **Marketing** — funnel model, 5 channels, recurring-revenue motions, and
   the 4-year marketing budget sized to the FY30 revenue target.
4. **Risks** — 18 risks across 3 categories (dependency, shared-engineer,
   IP-delay) with severity, revenue-at-risk, mitigation and named owner.

---

## Portfolio at a glance

- **41 IPs, all FPGA-proven today** — 26 controllers + 5 RISC-V cores
  (XR-V1..V5) + 10 space / rad-hard IPs.
- **Anchor customer:** HCL — US$400K contract + 18% annual maintenance
  (US$72K recurring) + preferential tapeout access.
- **Pipeline:** Tesolve, Quest Global, Mirafra (in discussion).
- **Bench:** 54 senior engineers — 26 RTL + 28 DV.
- **GTM go-live:** SIGPT.AI (30 Oct 2026) → Design & Reuse marketplace + global
  reseller network (Dec 2026) → first paid licenses Q1 CY2027.

---

## Running locally

The dashboard has **zero build step**. Any static file server works:

```bash
# Option 1 — direct in browser
open index.html                     # macOS
xdg-open index.html                 # Linux

# Option 2 — a lightweight local server (avoids some CORS caveats)
python3 -m http.server 8000
# then open http://localhost:8000/
```

Chart.js is loaded from a public CDN — an internet connection is required for
the charts to render on first open.

---

## Regenerating the blocker emails

```bash
python3 build-personal-emails.py
```

Reads the master blocker list embedded at the top of the script and rewrites
`blocker-email-basheer.html` (B1-B6) and `blocker-email-girish.html` (B2-B3
only). Preserves the CEO's mandated intro/footer copy verbatim:

> **Intro:** *Dear [name], following blockers are on your name, kindly check
> and do the needful on high priority*
> **Footer:** *From the Office of CEO*

---

## Design system

Colors (CSS variables in `dashboard.html`):

- `--ink:#0E1726` · `--paper:#FAFBFD`
- `--blue:#1E4FD8` · `--green:#0E7A4F` · `--copper:#C2410C`
- `--amber:#B45309` · `--red:#B91C1C` · `--violet:#5B2FB9` · `--teal:#0F766E`

Typography: **Space Grotesk** (headers), **Inter** (body), **IBM Plex Mono**
(labels & data cells).

Canvas: `max-width: 1320px`, breakpoints keep the layout comfortable down to
1366 px with no horizontal scroll.

---

## GitHub Pages (optional)

To publish the dashboard at
`https://xtremesilica.github.io/xtremesilica-dashboard/`:

1. Go to **Settings → Pages**.
2. **Source:** *Deploy from a branch*.
3. **Branch:** `main` · **Folder:** `/ (root)`.
4. Save. GitHub Pages will serve `index.html` from the repo root within ~1
   minute of every push.

---

## Publishing changes

All updates are committed through the maintaining assistant to `main` with
descriptive messages — no force-pushes, no branch deletion, no unrelated files
touched. Standard flow:

```
edit → verify (headless screenshot + understand_images) →
git add -A → git commit → git push origin main
```

---

## License

Proprietary — Xtremesilica internal use. Not for redistribution.
