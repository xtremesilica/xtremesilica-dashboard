# Daily Blocker Digest — Genspark Workflow Setup

## Why a Workflow (not this sandbox)

This chat session runs in an **ephemeral sandbox** — no cron, no scheduler, and the process dies when the session recycles. A recurring "email every morning at 8" **must** live in Genspark Workflows to actually keep running.

- Workflows page: **https://www.genspark.ai/workflows**
- Trigger type you need: **Schedule** (daily / weekdays / cron)
- Steps you need: **Send Email** (Gmail — already connected)

Optional but recommended: a **Stop condition** step so the workflow auto-suspends once no blockers are OPEN.

---

## 5-minute build recipe

1. **Workflows → Create new → "Xtremesilica Daily Blocker Digest"**
2. **Trigger: Schedule**
   - Frequency: **Daily**
   - Time: **08:00 Asia/Calcutta**
   - Days: **Mon–Fri** (or Mon–Sun if you want weekends too)
3. **Step 1: Send Email (Gmail)**
   - **To:** stakeholder emails (comma-separated) — CEO, COO, Chairman, CFO, BD
   - **Subject:** `[Xtremesilica] Daily Blocker Digest — {{DATE}}`
   - **Body type:** HTML
   - **Body:** paste the entire contents of `blocker-email-template.html` (delivered alongside this doc)
   - Replace the three placeholders in the pasted HTML:
     - `{{DATE}}` → workflow date expression (e.g. `{{now.format("EEEE, dd LLLL yyyy")}}`)
     - `{{DASHBOARD_URL}}` → your permanent dashboard URL (see note below)
     - `{{OPEN_COUNT}}` → `3` for now; once you wire the data-source step, make this dynamic
4. **Save & activate.**
5. **Test:** Workflows → Run once → confirm the email lands in the CEO inbox.

---

## Stopping the workflow automatically when blockers clear

The cleanest pattern:

- Add a **precondition** step before Send Email that fetches the blocker count from your dashboard's data source (currently the values baked into `dashboard.html` — recommend moving to a small JSON at a stable URL, e.g. `blockers.json`).
- If `open_count == 0`, exit the workflow (skip the email step).
- Once all three blockers show `CLOSED · GREEN`, deactivate the workflow manually.

---

## Which dashboard URL should the email point to?

The **sandbox URL** (`https://8000-sbx-…sspark.ai`) is session-bound — it dies when this chat recycles. Do **not** use it in a recurring workflow. Options:

| Route | Effort | Stability |
|---|---|---|
| Host `dashboard.html` on `xtremesilica.com/dashboard.html` (via your team's web host) | Low — one file upload | Permanent, best option |
| Publish via Cloudflare Pages / Vercel / Netlify (free) | 15 min | Permanent |
| Attach the delivered `xtremesilica-dashboard.html` as a link to its Genspark project | Zero — already there | Permanent, but auth-gated to your Genspark account |

For the workflow: **use the xtremesilica.com URL** so stakeholders open it without login friction.

---

## Content updates

The blocker table in the email template is baked from **today's dashboard state (06-Sep-2026)**:

- **B1** — MEDIUM · AMBER · NEAR CLOSURE · 19/23 IPs resourced · 4 remain
- **B2** — HIGH · RED · SCL partnership · target 30-Sep-26
- **B3** — HIGH · RED · DLI / C-DAC funding · target 15-Oct-26

When B1 closes on 10-Sep, edit the template's B1 row (or delete it entirely) inside the workflow's Send Email body, then re-save the workflow. Same for B2 / B3 when they close.

For a fully-automated version, wire the workflow to read blockers from a JSON file the dashboard also consumes — one edit updates both.
