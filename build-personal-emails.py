#!/usr/bin/env python3
"""Xtremesilica daily blocker reminder — generate and send.

Basheer receives B1-B6 (owner or co-owner of all six blockers).
Girish  receives B2 and B3 only (co-owner of SCL partnership and DLI funding).

Reads blockers.json (single source of truth used by dashboard.html /
index.html and this script). Blockers whose status contains CLOSED,
COMPLETED, RESOLVED or DONE are excluded automatically.

Renders one HTML digest per recipient and, unless invoked with
--dry-run, sends it via the connected Genspark Gmail account
(xtremesilica@gmail.com) using `gsk gmail send`.

Usage:
    python3 build-personal-emails.py             # render + send
    python3 build-personal-emails.py --dry-run   # render only
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

TARGETS = [
    ("Mr Basheer Boddikonda", "ahmed@sionsemi.com",  "blocker-email-basheer.html"),
    ("Mr Girish B V",         "girish@sionsemi.com", "blocker-email-girish.html"),
]


def script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def now_ist_header():
    now = datetime.now(IST)
    return now.strftime("%A, %d %B %Y") + " &middot; " + now.strftime("%H:%M") + " IST"


def load_open_blockers():
    with open(os.path.join(script_dir(), "blockers.json"), encoding="utf-8") as f:
        data = json.load(f)
    return [b for b in data.get("blockers", []) if not EXCLUDED_RE.search(b.get("status", ""))]


def blockers_for(target_email, open_blockers):
    return [b for b in open_blockers
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
    proc = subprocess.run(args, capture_output=True, text=True)
    try:
        d = json.loads(proc.stdout)
        data = d.get("data") or {}
        return {
            "status": data.get("status") or d.get("status") or "unknown",
            "message_id": data.get("sent_message_id"),
            "to": data.get("to"),
            "bcc": data.get("bcc"),
        }
    except Exception as exc:
        return {"status": "failed", "error": f"{exc} | stderr={proc.stderr[:200]}"}


def main():
    argv = sys.argv[1:]
    dry_run = ("--dry-run" in argv) or ("--no-send" in argv)

    date_str = now_ist_header()
    today = datetime.now(IST).date()
    bcc = BCC_ADDRESS if today <= BCC_UNTIL else None

    open_blockers = load_open_blockers()
    open_ids = ", ".join(b["id"] for b in open_blockers) or "none"
    print(f"Rendered at   : {date_str}")
    print(f"Open blockers : {len(open_blockers)} ({open_ids})")
    print(f"BCC audit     : {'enabled -> ' + bcc if bcc else 'disabled (past 2026-09-16)'}")
    print(f"Mode          : {'DRY-RUN (no emails sent)' if dry_run else 'LIVE (sending via gsk gmail)'}")

    d = script_dir()
    for recipient_name, target_email, out_filename in TARGETS:
        picked = blockers_for(target_email, open_blockers)
        if not picked:
            print(f"[{recipient_name}] skipped -- no open blockers")
            continue

        html = render_email(recipient_name, picked, date_str)
        with open(os.path.join(d, out_filename), "w", encoding="utf-8") as f:
            f.write(html)

        subject = f"Daily blocker digest -- {len(picked)} open . {today.strftime('%d-%b-%Y')}"
        ids = ", ".join(b["id"] for b in picked)
        print(f"[{recipient_name}] to={target_email} bcc={bcc or 'none'} blocker_ids=[{ids}] subject={subject!r}")

        if dry_run:
            continue

        result = send_via_gsk(target_email, subject, html, bcc)
        print(f"    -> gmail: {result}")


if __name__ == "__main__":
    main()
