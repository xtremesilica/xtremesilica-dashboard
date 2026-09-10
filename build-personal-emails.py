#!/usr/bin/env python3
"""Xtremesilica daily blocker reminder — generate and send.

Basheer receives B1–B6 (owner or co-owner of all six blockers).
Girish  receives B2 and B3 only (co-owner of SCL partnership and DLI funding).

`blockers.json` is the single source of truth used by dashboard.html /
index.html and this script. It provides both:
  - blockers[]   -- the current open items
  - recipients[] -- name, email, output_file for every owner who receives a
                    digest.
Blockers whose status contains CLOSED, COMPLETED, RESOLVED or DONE are
excluded automatically.

Renders one HTML digest per recipient in `recipients[]` and, unless invoked
with --dry-run, sends it via the connected Genspark Gmail account
(xtremesilica@gmail.com) using `gsk gmail send`.

Failure semantics
-----------------
Any Gmail send that returns a non-success status, no `sent_message_id`, or
raises an error causes the script to exit non-zero. This prevents the
scheduled workflow from ever reporting false success.

Usage
-----
    python3 build-personal-emails.py             # render + send  (workflow)
    python3 build-personal-emails.py --dry-run   # render only    (tests)
"""
import os
import re
import sys
import json
import subprocess
from datetime import datetime, timezone, timedelta, date

IST = timezone(timedelta(hours=5, minutes=30), name="Asia/Kolkata")
EXCLUDED_RE = re.compile(r"\b(CLOSED|COMPLETED|RESOLVED|DONE)\b", re.I)
BCC_UNTIL = date(2026, 9, 16)
BCC_ADDRESS = "sudeep@sionsemi.com"
FROM_ACCOUNT = "xtremesilica@gmail.com"


def script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def now_ist_header():
    now = datetime.now(IST)
    return now.strftime("%A, %d %B %Y") + " &middot; " + now.strftime("%H:%M") + " IST"


def load_data():
    with open(os.path.join(script_dir(), "blockers.json"), encoding="utf-8") as f:
        return json.load(f)


def open_blockers(data):
    return [b for b in data.get("blockers", []) if not EXCLUDED_RE.search(b.get("status", ""))]


def blockers_for(target_email, open_list):
    return [b for b in open_list
            if any(o.get("email") == target_email for o in b.get("owners", []))]


def render_row(b):
    return (
        "\n            <tr>"
        f'\n              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; vertical-align:top; font-family:\'IBM Plex Mono\',Consolas,monospace; font-weight:700; color:#B91C1C;">{b["id"]}</td>'
        '\n              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; vertical-align:top;">'
        f'\n                <div style="font-weight:600; color:#0E1726; margin-bottom:4px;">{b["title"]}</div>'
        f'\n                <div style="font-size:12px; color:#44506A; line-height:1.5;">{b["description"]}</div>'
        '\n              </td>'
        f'\n              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; text-align:center; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:11px; font-weight:700; color:{b["sev_color"]}; letter-spacing:.06em;">{b["sev"]}</td>'
        f'\n              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; text-align:center; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:11.5px; font-weight:600; color:#374151;">{b["target"]}</td>'
        '\n              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; text-align:center;">'
        f'\n                <span style="display:inline-block; padding:3px 8px; border-radius:10px; background:{b["status_bg"]}; color:{b["status_color"]}; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:10px; font-weight:700; letter-spacing:.05em;">{b["status_text"]}</span>'
        '\n              </td>'
        '\n            </tr>'
    )


def render_email(recipient_name, blockers, date_str):
    open_count = len(blockers)
    rows = "".join(render_row(b) for b in blockers)
    return (
        '<div style="background:#F5F7FA; padding:24px 0; font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif; color:#0E1726;">\n'
        '  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:720px; margin:0 auto; background:#FFFFFF; border:1px solid #DDE3EC; border-radius:8px; overflow:hidden;">\n'
        '    <tr>\n'
        '      <td style="background:#DC2626; color:#FFFFFF; padding:16px 24px;">\n'
        '        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">\n'
        '          <tr>\n'
        '            <td style="font-size:20px; font-weight:700; letter-spacing:-.01em;">\n'
        '              <span style="display:inline-block; width:28px; height:28px; background:#FFFFFF; color:#DC2626; text-align:center; line-height:28px; border-radius:50%; font-weight:800; margin-right:10px; vertical-align:middle;">!</span>\n'
        '              Critical Blockers &mdash; Action Required\n'
        '            </td>\n'
        '            <td style="text-align:right; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:12px; opacity:.95;">\n'
        f'              {open_count} OPEN &middot; {date_str}\n'
        '            </td>\n'
        '          </tr>\n'
        '        </table>\n'
        '      </td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <td style="background:#FEF2F2; border-bottom:1px solid #FCA5A5; padding:14px 24px; color:#7F1D1D; font-size:13.5px; line-height:1.55; font-weight:500;">\n'
        f'        Dear {recipient_name}, following blockers are on your name, kindly check and do the needful on high priority.\n'
        '      </td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <td style="padding:20px 24px 8px;">\n'
        '        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse; font-size:13px;">\n'
        '          <thead>\n'
        '            <tr>\n'
        '              <th style="text-align:left; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">#</th>\n'
        '              <th style="text-align:left; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">BLOCKER</th>\n'
        '              <th style="text-align:center; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">SEV</th>\n'
        '              <th style="text-align:center; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">TARGET</th>\n'
        '              <th style="text-align:center; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">STATUS</th>\n'
        '            </tr>\n'
        '          </thead>\n'
        f'          <tbody>{rows}\n'
        '          </tbody>\n'
        '        </table>\n'
        '      </td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <td style="padding:14px 24px 20px;">\n'
        '        <div style="background:#FEE2E2; border-left:3px solid #DC2626; padding:12px 14px; font-size:12.5px; color:#7F1D1D; line-height:1.55; border-radius:0 4px 4px 0;">\n'
        '          <strong>Immediate objective:</strong> Every day these blockers stay open delays the FY28 revenue window and pushes bookings into FY29. Please close on or before the target dates above.\n'
        '        </div>\n'
        '      </td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <td style="background:#F5F7FA; border-top:1px solid #DDE3EC; padding:14px 24px; font-family:\'IBM Plex Mono\',Consolas,monospace; font-size:11px; color:#8A94A8; line-height:1.6; text-align:center;">\n'
        '        From the Office of CEO\n'
        '      </td>\n'
        '    </tr>\n'
        '  </table>\n'
        '</div>\n'
    )


class SendError(Exception):
    """Raised when a gsk gmail send returns a non-success or missing message id."""


def send_via_gsk(to, subject, html, bcc):
    args = [
        "gsk", "gmail", "send",
        "--from_account", FROM_ACCOUNT,
        "--to", to,
        "--subject", subject,
        "--content_type", "text/html",
        "--body", html,
        "--skip_confirmation", "true",
    ]
    if bcc:
        args += ["--bcc", bcc]
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=120)
    except Exception as exc:
        raise SendError(f"gsk gmail send raised: {exc!r}")

    if proc.returncode != 0:
        raise SendError(
            f"gsk gmail send returned exit code {proc.returncode} for to={to}. "
            f"stderr={proc.stderr[:400]!r} stdout={proc.stdout[:400]!r}"
        )

    try:
        payload = json.loads(proc.stdout)
    except Exception as exc:
        raise SendError(
            f"gsk gmail send returned non-JSON stdout for to={to}: {exc!r} "
            f"raw={proc.stdout[:400]!r}"
        )

    top_status = payload.get("status")
    data = payload.get("data") or {}
    inner_status = data.get("status")
    mid = data.get("sent_message_id")

    if top_status != "ok":
        raise SendError(
            f"gsk gmail send returned status={top_status!r} for to={to}. "
            f"message={payload.get('message')!r} payload={payload}"
        )
    if inner_status not in ("success", "sent"):
        raise SendError(
            f"gsk gmail send inner status was {inner_status!r} (expected 'success') for to={to}. "
            f"payload={payload}"
        )
    if not mid:
        raise SendError(
            f"gsk gmail send returned no sent_message_id for to={to}. payload={payload}"
        )

    return {
        "status": inner_status,
        "message_id": mid,
        "thread_id": data.get("thread_id"),
        "to": data.get("to"),
        "bcc": data.get("bcc"),
    }


def main():
    argv = sys.argv[1:]
    dry_run = ("--dry-run" in argv) or ("--no-send" in argv)

    date_str = now_ist_header()
    today = datetime.now(IST).date()
    bcc = BCC_ADDRESS if today <= BCC_UNTIL else None
    subject_date = today.strftime("%d-%b-%Y")

    data = load_data()
    recipients = data.get("recipients") or []
    if not recipients:
        print("ERROR: blockers.json has no recipients[] -- refusing to run", file=sys.stderr)
        sys.exit(2)

    open_list = open_blockers(data)
    open_ids = ", ".join(b["id"] for b in open_list) or "none"
    print(f"Rendered at   : {date_str}")
    print(f"Open blockers : {len(open_list)} ({open_ids})")
    print(f"Recipients    : {len(recipients)} (from blockers.json)")
    print(f"BCC audit     : {'enabled -> ' + bcc if bcc else 'disabled (past 2026-09-16)'}")
    print(f"Mode          : {'DRY-RUN (no emails sent)' if dry_run else 'LIVE (sending via gsk gmail)'}")

    d = script_dir()
    failures = []
    sent = []

    for r in recipients:
        recipient_name = r["name"]
        target_email = r["email"]
        out_filename = r.get("output_file") or f"blocker-email-{recipient_name.split()[-1].lower()}.html"

        picked = blockers_for(target_email, open_list)
        if not picked:
            print(f"[{recipient_name}] skipped -- no open blockers")
            continue

        html = render_email(recipient_name, picked, date_str)
        with open(os.path.join(d, out_filename), "w", encoding="utf-8") as f:
            f.write(html)

        # Restored production subject format: em-dash and middle-dot
        subject = f"Daily blocker digest \u2014 {len(picked)} open \u00b7 {subject_date}"
        ids = ", ".join(b["id"] for b in picked)
        print(f"[{recipient_name}] to={target_email} bcc={bcc or 'none'} "
              f"blocker_ids=[{ids}] subject={subject!r}")

        if dry_run:
            continue

        try:
            result = send_via_gsk(target_email, subject, html, bcc)
            print(f"    -> gmail: status={result['status']} id={result['message_id']} "
                  f"to={result['to']} bcc={result['bcc']}")
            sent.append({"recipient": recipient_name, **result})
        except SendError as exc:
            print(f"    !! FAIL for {recipient_name} ({target_email}): {exc}", file=sys.stderr)
            failures.append({"recipient": recipient_name, "to": target_email, "error": str(exc)})

    if failures:
        print(f"\nFAILED sends: {len(failures)}", file=sys.stderr)
        for f in failures:
            print(f"  - {f['recipient']} <{f['to']}>: {f['error']}", file=sys.stderr)
        sys.exit(1)

    if not dry_run and not sent:
        # Zero sends AND zero failures = zero recipients had open blockers.
        # That is a legitimate no-op; log it and exit clean.
        print("No recipient had any open blockers; no emails sent.")
    print("DONE")


if __name__ == "__main__":
    main()
