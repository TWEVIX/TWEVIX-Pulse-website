import hashlib
from datetime import datetime, timezone
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TWEVIX Pulse™ | Solutions, Impact Telemetry & Verified Talent SaaS",
    page_icon=":material/monitoring:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CSS MATCHING TWEVIX.COM LIGHT ENTERPRISE DESIGN ---
st.markdown(
    """
    <style>
    /* Clean Light Enterprise Canvas matching twevix.com */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    .block-container {
        padding-top: 1.5rem !important;
        max-width: 1200px !important;
    }

    /* Top Brand Bar */
    .brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }
    .brand-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.01em;
    }
    .brand-tagline {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: #0284c7;
        text-transform: uppercase;
    }

    /* Hero Banner matching twevix.com */
    .hero-box {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 55%, #ecfdf5 100%);
        border: 1px solid #bae6fd;
        border-radius: 18px;
        padding: 36px 40px;
        margin-bottom: 24px;
        box-shadow: 0 10px 28px rgba(2, 132, 199, 0.08);
    }
    .hero-eyebrow {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 5px 14px;
        border-radius: 999px;
        margin-bottom: 14px;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1.18;
        color: #0f172a;
        margin: 0 0 12px 0;
    }
    .hero-accent {
        color: #0284c7;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #334155;
        max-width: 820px;
        line-height: 1.65;
        margin: 0;
    }

    /* Elevated White KPI Cards */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #0284c7;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }
    .kpi-card.teal { border-top-color: #0d9488; }
    .kpi-card.indigo { border-top-color: #4f46e5; }
    .kpi-card.amber { border-top-color: #d97706; }
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #64748b;
        font-weight: 700;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
        margin: 4px 0 2px 0;
    }
    .kpi-delta {
        font-size: 0.82rem;
        color: #0284c7;
        font-weight: 600;
    }

    /* Elevated White Solution & Talent Cards */
    .saas-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 14px;
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.05);
        transition: all 0.2s ease;
    }
    .saas-card:hover {
        border-color: #38bdf8;
        box-shadow: 0 8px 24px rgba(2, 132, 199, 0.1);
    }
    .skill-pill {
        display: inline-block;
        background: #f0f9ff;
        color: #0369a1;
        border: 1px solid #bae6fd;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px 6px 3px 0;
    }
    .impact-pill {
        display: inline-block;
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .product-tag {
        display: inline-block;
        background: #eef2ff;
        color: #4338ca;
        border: 1px solid #c7d2fe;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .passport-img {
        width: 96px;
        height: 96px;
        border-radius: 14px;
        object-fit: cover;
        border: 2px solid #0284c7;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.18);
    }

    /* Crisp Corporate Buttons matching twevix.com */
    .stButton > button, .stLinkButton > a {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.15rem !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.22) !important;
    }
    .stButton > button:hover, .stLinkButton > a:hover {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%) !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HELPER: COMPUTE SENIORITY TIER FROM STACKED 3-MONTH CYCLES ---
def get_tenure_tier(cycle_count: int):
    months = cycle_count * 3
    if cycle_count == 1:
        return f"{months} Months Verified (1 Cycle)", "Associate Decision Analyst"
    elif cycle_count == 2:
        return f"{months} Months Verified (2 Cycles)", "Applied Decision-Intelligence Specialist"
    else:
        return f"{months} Months Verified ({cycle_count} Cycles)", "Lead Operational Data Architect"

# --- HELPER: GENERATE PRINTABLE HTML/PDF CERTIFICATE ---
def build_certificate_html(
    name: str,
    institution: str,
    cycle: str,
    vertical: str,
    issue_date: str,
    cred_id: str,
    sha256_hash: str,
) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TWEVIX Pulse Verified Certificate - {name}</title>
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f8fafc; margin: 0; padding: 32px; color: #0f172a; }}
  .cert-frame {{
    max-width: 960px; margin: 0 auto; background: #ffffff;
    border: 10px solid #0f2942; outline: 3px solid #0284c7; outline-offset: -18px;
    padding: 48px 56px; box-shadow: 0 12px 30px rgba(0,0,0,0.08);
  }}
  .top-tag {{ font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #0284c7; }}
  h1 {{ font-size: 32px; margin: 10px 0 6px 0; color: #0f2942; }}
  .subtitle {{ font-size: 15px; color: #475569; margin-bottom: 24px; }}
  .recipient {{ font-size: 30px; font-weight: 700; color: #0f172a; border-bottom: 2px solid #cbd5e1; display: inline-block; padding-bottom: 6px; margin: 8px 0; }}
  .institution {{ font-size: 16px; font-weight: 600; color: #334155; margin-bottom: 20px; }}
  .body-text {{ font-size: 15px; line-height: 1.6; color: #1e293b; max-width: 780px; }}
  .track-box {{ background: #f0f9ff; border-left: 5px solid #0284c7; padding: 14px 20px; margin: 20px 0; font-size: 17px; font-weight: 700; color: #0f2942; }}
  .footer-grid {{ display: flex; justify-content: space-between; align-items: flex-end; margin-top: 32px; padding-top: 18px; border-top: 1px solid #e2e8f0; }}
  .sig-line {{ border-top: 1.5px solid #0f2942; width: 270px; padding-top: 6px; font-size: 13px; }}
  .hash-box {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 14px; font-family: monospace; font-size: 11px; color: #334155; max-width: 460px; word-break: break-all; }}
  @media print {{ body {{ background: #ffffff; padding: 0; }} .cert-frame {{ box-shadow: none; }} }}
</style>
</head>
<body>
  <div class="cert-frame">
    <div class="top-tag">TWEVIX™ • TWEVIX Pulse™ • TechYatch Lab™ • TWEVIX CARE™</div>
    <h1>Certificate of Audited Operational Proof-of-Work</h1>
    <div class="subtitle">Cryptographically Verified 12-Week (3-Month) Industry Deployment Credential</div>
    <div>This certifies that</div>
    <div class="recipient">{name}</div>
    <div class="institution">{institution}</div>
    <div class="body-text">
      Has successfully executed applied data diagnostics, decision-intelligence engineering, and quality-assured operational delivery under the supervision of <strong>TWEVIX™</strong> in the following verified deployment cycle:
    </div>
    <div class="track-box">{cycle} — {vertical}</div>
    <div class="footer-grid">
      <div class="sig-line">
        <strong>Willa Abraham</strong><br>
        MSc Data Science for Business (University of Stirling)<br>
        Founder &amp; Lead Product Architect, TWEVIX™
      </div>
      <div class="hash-box">
        <strong>CREDENTIAL ID:</strong> {cred_id} &nbsp;|&nbsp; <strong>ISSUED:</strong> {issue_date} UTC<br>
        <strong>SHA-256 FINGERPRINT:</strong><br>{sha256_hash}
      </div>
    </div>
  </div>
</body>
</html>"""

# --- DEFAULT VERIFIED DEPLOYMENTS & TALENT LEDGER ---
DEFAULT_RECORDS = [
    {
        "analyst_id": "TVX-001",
        "name": "Jean-Paul Mugisha",
        "photo_url": "https://ui-avatars.com",
        "institution": "University of Rwanda (BSc Data Science)",
        "location": "Kigali, Rwanda (Remote / Hybrid)",
        "availability": "Open to Full-Time & Remote Contract",
        "skills_with_years": "Python (2.5 Yrs) | SQL & Pandas (2 Yrs) | TechYatch Diagnostic OS™ (6 Mos) | RFM Segmentation (1 Yr)",
        "linkedin": "https://linkedin.com",
        "cycle_number": "Cycle 01 (3 Months)",
        "credential_id": "TVX-8F4A2C91E0B7",
