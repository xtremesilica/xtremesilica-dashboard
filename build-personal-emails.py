#!/usr/bin/env python3
"""Build per-recipient blocker digest emails.
- Basheer gets B1 + B2 + B3 (owner or co-owner of all three)
- Girish gets B2 + B3 only (co-owner of SCL and DLI)
"""

# ------------------------------------------------------------------ blockers
B1 = {
    "id": "B1",
    "title": "Claude &amp; AWS Server allotment for 22 of 41 IPs",
    "detail": "<strong>19/41 done.</strong> 22 IPs remain: H.265, AMBA AXI, PCIe Gen6 Sw, CXL, UALink 2.0, Ultra Ethernet, HBM4, <strong>5 RISC-V cores</strong>, plus <strong>10 new Space IPs</strong> (V2SP, V3SP, ECC/EDAC, Memory Scrubber, Fault-Mgmt, Lockstep/TMR, SpaceWire, SpaceFibre, NoC-FT, Root of Trust) &mdash; all UNASSIGNED.",
    "sev": "HIGH", "sev_color": "#B91C1C",
    "owner": "Basheer Boddikonda", "owner_email": "ahmed@sionsemi.com",
    "target": "10-Sep-26",
    "status_text": "RED &middot; REOPENED",
    "status_bg": "#FEE2E2", "status_color": "#B91C1C",
}
B5 = {
    "id": "B5",
    "title": "RISC-V CPU family (5 cores XR-V1&hellip;V5) &mdash; entire team to build",
    "detail": "Five new RISC-V cores &mdash; <strong>XR-V1</strong> (RV32 IoT), <strong>XR-V2</strong> (RV32 automotive/robotics), <strong>XR-V3</strong> (RV64 edge-AI), <strong>XR-V4</strong> (RV64 Linux/networking), <strong>XR-V5</strong> (RV64 Vector/AI/HPC). RTL/DV UNASSIGNED across all 5. Requires a <strong>net-new CPU architecture team (5-8 engineers)</strong>. Represents <strong>$7.85M FY30 revenue</strong> (22% of the $36.20M projection).",
    "sev": "CRITICAL", "sev_color": "#B91C1C",
    "owner": "CEO + Basheer Boddikonda", "owner_email": "ahmed@sionsemi.com",
    "target": "30-Sep-26",
    "status_text": "RED &middot; OPEN",
    "status_bg": "#FEE2E2", "status_color": "#B91C1C",
}
B6 = {
    "id": "B6",
    "title": "Space IP portfolio (10 IPs) &mdash; rad-hard team + SCL/ISRO qualification path",
    "detail": "Ten new Space IPs &mdash; <strong>V2SP</strong> (16-bit RISC-V space processor), <strong>V3SP</strong> (32-bit RISC-V space processor), <strong>ECC/EDAC library</strong>, <strong>Memory Scrubber</strong>, <strong>Fault-Management Controller</strong>, <strong>Lockstep/TMR library</strong>, <strong>SpaceWire</strong> (controller/router), <strong>SpaceFibre</strong>, <strong>NoC-FT</strong> (fault-tolerant NoC), <strong>Root of Trust</strong>. RTL/DV UNASSIGNED across all 10. Needs a <strong>rad-hard/space-IP team (4-6 engineers)</strong> + <strong>SCL 180nm tape-out slot</strong> (couples with B2). Represents <strong>~$4M FY30 uplift</strong> (from $32.20M \u2192 $36.20M) and opens the ISRO/DRDO/BEL pipeline.",
    "sev": "CRITICAL", "sev_color": "#B91C1C",
    "owner": "CEO + Basheer Boddikonda", "owner_email": "ahmed@sionsemi.com",
    "target": "15-Oct-26",
    "status_text": "RED &middot; OPEN",
    "status_bg": "#FEE2E2", "status_color": "#B91C1C",
}
B4 = {
    "id": "B4",
    "title": "3 new AI/Datacenter IPs &mdash; team assignment &amp; compute",
    "detail": "Three newly added IPs &mdash; <strong>UALink 2.0</strong> (chiplet fabric, competes with UCIe/NVLink), <strong>Ultra Ethernet</strong> (AI-cluster RDMA, competes with InfiniBand), <strong>HBM4 Controller</strong> (next-gen 3D-stacked memory) &mdash; all Mar-27 GA. RTL &amp; DV owners <strong>UNASSIGNED</strong>, Claude + AWS <strong>NOT ALLOTTED</strong>. Every week unstaffed pushes Mar-27 gate to Jun-27; ~$1.6M FY30 revenue at risk.",
    "sev": "CRITICAL", "sev_color": "#B91C1C",
    "owner": "Basheer Boddikonda", "owner_email": "ahmed@sionsemi.com",
    "target": "20-Sep-26",
    "status_text": "RED &middot; OPEN",
    "status_bg": "#FEE2E2", "status_color": "#B91C1C",
}
B2 = {
    "id": "B2",
    "title": "SCL partnership for Space-IP rad-hard prototypes",
    "detail": "Sign up with <strong>SCL (Semi-Conductor Laboratory)</strong> for future Space IPs &mdash; rad-hardened prototypes on 180nm process; unlocks ISRO / DRDO / BEL pipeline.",
    "sev": "HIGH", "sev_color": "#C2410C",
    "owner": "Basheer Boddikonda + Girish B V", "owner_email": "ahmed@sionsemi.com, girish@sionsemi.com",
    "target": "30-Sep-26",
    "status_text": "RED &middot; OPEN",
    "status_bg": "#FEE2E2", "status_color": "#B91C1C",
}
B3 = {
    "id": "B3",
    "title": "DLI funding for PCIe Gen6 Switch tapeout",
    "detail": "Discuss with <strong>C-DAC / IESA</strong> for <strong>DLI (Design Linked Incentive)</strong> funding &mdash; target: PCIe Gen6 Switch fabric tapeout ($400K ASP &middot; $4.91M FY30 revenue).",
    "sev": "HIGH", "sev_color": "#C2410C",
    "owner": "Basheer Boddikonda + Girish B V", "owner_email": "ahmed@sionsemi.com, girish@sionsemi.com",
    "target": "15-Oct-26",
    "status_text": "RED &middot; OPEN",
    "status_bg": "#FEE2E2", "status_color": "#B91C1C",
}


def render_row(b):
    return f'''
            <tr>
              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; vertical-align:top; font-family:'IBM Plex Mono',Consolas,monospace; font-weight:700; color:#B91C1C;">{b["id"]}</td>
              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; vertical-align:top;">
                <div style="font-weight:600; color:#0E1726; margin-bottom:4px;">{b["title"]}</div>
                <div style="font-size:12px; color:#44506A; line-height:1.5;">{b["detail"]}</div>
              </td>
              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; text-align:center; font-family:'IBM Plex Mono',Consolas,monospace; font-size:11px; font-weight:700; color:{b["sev_color"]}; letter-spacing:.06em;">{b["sev"]}</td>
              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; text-align:center; font-family:'IBM Plex Mono',Consolas,monospace; font-size:11.5px; font-weight:600; color:#374151;">{b["target"]}</td>
              <td style="padding:12px 6px; border-bottom:1px solid #F0F2F5; text-align:center;">
                <span style="display:inline-block; padding:3px 8px; border-radius:10px; background:{b["status_bg"]}; color:{b["status_color"]}; font-family:'IBM Plex Mono',Consolas,monospace; font-size:10px; font-weight:700; letter-spacing:.05em;">{b["status_text"]}</span>
              </td>
            </tr>'''


def render_email(recipient_name, blockers, date_str, is_preview=False):
    open_count = len(blockers)
    rows = "".join(render_row(b) for b in blockers)
    preview_banner = ""
    if is_preview:
        preview_banner = f'''
  <div style="background:#0E1726; color:#FFFFFF; padding:10px 20px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; font-size:12px; text-align:center; max-width:720px; margin:0 auto 8px; border-radius:4px;">
    <strong>PREVIEW &mdash; this is exactly what {recipient_name} will receive at 09:00 IST daily until their blockers are cleared.</strong> No action required.
  </div>
'''

    return f'''<div style="background:#F5F7FA; padding:24px 0; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; color:#0E1726;">
{preview_banner}
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:720px; margin:0 auto; background:#FFFFFF; border:1px solid #DDE3EC; border-radius:8px; overflow:hidden;">
    <tr>
      <td style="background:#DC2626; color:#FFFFFF; padding:16px 24px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
          <tr>
            <td style="font-size:20px; font-weight:700; letter-spacing:-.01em;">
              <span style="display:inline-block; width:28px; height:28px; background:#FFFFFF; color:#DC2626; text-align:center; line-height:28px; border-radius:50%; font-weight:800; margin-right:10px; vertical-align:middle;">!</span>
              Critical Blockers &mdash; Action Required
            </td>
            <td style="text-align:right; font-family:'IBM Plex Mono',Consolas,monospace; font-size:12px; opacity:.95;">
              {open_count} OPEN &middot; {date_str}
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <tr>
      <td style="background:#FEF2F2; border-bottom:1px solid #FCA5A5; padding:14px 24px; color:#7F1D1D; font-size:13.5px; line-height:1.55; font-weight:500;">
        Dear {recipient_name}, following blockers are on your name, kindly check and do the needful on high priority.
      </td>
    </tr>

    <tr>
      <td style="padding:20px 24px 8px;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse; font-size:13px;">
          <thead>
            <tr>
              <th style="text-align:left; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:'IBM Plex Mono',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">#</th>
              <th style="text-align:left; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:'IBM Plex Mono',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">BLOCKER</th>
              <th style="text-align:center; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:'IBM Plex Mono',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">SEV</th>
              <th style="text-align:center; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:'IBM Plex Mono',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">TARGET</th>
              <th style="text-align:center; padding:8px 6px; border-bottom:2px solid #0E1726; color:#0E1726; font-family:'IBM Plex Mono',Consolas,monospace; font-size:10.5px; letter-spacing:.08em;">STATUS</th>
            </tr>
          </thead>
          <tbody>{rows}
          </tbody>
        </table>
      </td>
    </tr>

    <tr>
      <td style="padding:14px 24px 20px;">
        <div style="background:#FEE2E2; border-left:3px solid #DC2626; padding:12px 14px; font-size:12.5px; color:#7F1D1D; line-height:1.55; border-radius:0 4px 4px 0;">
          <strong>Immediate objective:</strong> Every day these blockers stay open delays the FY28 revenue window and pushes bookings into FY29. Please close on or before the target dates above.
        </div>
      </td>
    </tr>

    <tr>
      <td style="background:#F5F7FA; border-top:1px solid #DDE3EC; padding:14px 24px; font-family:'IBM Plex Mono',Consolas,monospace; font-size:11px; color:#8A94A8; line-height:1.6; text-align:center;">
        From the Office of CEO
      </td>
    </tr>
  </table>
</div>
'''


DATE = "Monday, 07 September 2026 &middot; 06:56 IST"

# ------------------------------------------------------------------ Basheer (all 6)
open("/home/user/workspace/xtremesilica/blocker-email-basheer.html", "w", encoding="utf-8").write(
    render_email("Mr Basheer Boddikonda", [B1, B2, B3, B4, B5, B6], DATE, is_preview=True))
open("/tmp/email_basheer_live.html", "w", encoding="utf-8").write(
    render_email("Mr Basheer Boddikonda", [B1, B2, B3, B4, B5, B6], DATE, is_preview=False))

# ------------------------------------------------------------------ Girish (B2, B3 only)
open("/home/user/workspace/xtremesilica/blocker-email-girish.html", "w", encoding="utf-8").write(
    render_email("Mr Girish B V", [B2, B3], DATE, is_preview=True))
open("/tmp/email_girish_live.html", "w", encoding="utf-8").write(
    render_email("Mr Girish B V", [B2, B3], DATE, is_preview=False))

print("Basheer template: 6 rows")
print("Girish template: 2 rows")
