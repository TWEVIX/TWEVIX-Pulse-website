import hashlib
from datetime import datetime, timezone
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TWEVIX Pulse™ | Solutions, Impact Telemetry & Verified Talent SaaS",
    page_icon=":material/monitoring:",
    layout="wide",
)

# --- HELPER: COMPUTE SENIORITY TIER FROM STACKED 3-MONTH CYCLES ---
def get_tenure_tier(cycle_count: int):
    months = cycle_count * 3
    if cycle_count == 1:
        return f"{months} Months (1 Cycle)", "Associate Decision Analyst"
    elif cycle_count == 2:
        return f"{months} Months (2 Cycles)", "Applied Decision-Intelligence Specialist"
    else:
        return f"{months} Months ({cycle_count} Cycles)", "Lead Operational Data Architect"

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
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f7fa; margin: 0; padding: 32px; color: #0f172a; }}
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
        "institution": "University of Rwanda (Data Science)",
        "location": "Kigali, Rwanda (Remote / Hybrid)",
        "availability": "Open to Full-Time & Remote Contract",
        "linkedin": "https://linkedin.com",
        "cycle_number": "Cycle 01 (3 Months)",
        "credential_id": "TVX-8F4A2C91E0B7",
        "product_vertical": "TechYatch Lab™ • SME Diagnostic OS",
        "client_sector": "Food & Hospitality SME",
        "deployment_title": "Perishable Waste & RFM Retention Engine for Kigali Artisan Bakery",
        "problem_solved": "High daily unsold pastry waste and unmonitored drop-off among repeat weekend buyers.",
        "verified_outcome": "Audited 90 days of POS & stock CSVs; isolated 22% afternoon perishable waste and engineered an RFM loyalty bundle recovering 14% monthly margin.",
        "stack": "TechYatch Diagnostic OS™ | Python | RFM Segmentation",
        "issue_date": "2026-08-15",
    },
    {
        "analyst_id": "TVX-001",
        "name": "Jean-Paul Mugisha",
        "institution": "University of Rwanda (Data Science)",
        "location": "Kigali, Rwanda (Remote / Hybrid)",
        "availability": "Open to Full-Time & Remote Contract",
        "linkedin": "https://linkedin.com",
        "cycle_number": "Cycle 02 (3 Months)",
        "credential_id": "TVX-4B9E10D7C3A2",
        "product_vertical": "Global Cross-Border Social-Impact Sprint",
        "client_sector": "Agri-Supply Chain & NGO",
        "deployment_title": "East African Agricultural Supply-Chain Price Volatility Forecaster",
        "problem_solved": "Unpredictable staple commodity price swings disrupting regional procurement budgets.",
        "verified_outcome": "Co-built time-series forecasting pipelines across 12,000+ regional market records with international peer reviewers.",
        "stack": "Holt-Winters Forecasting | Pandas | Cross-Border Sprint",
        "issue_date": "2026-11-15",
    },
    {
        "analyst_id": "TVX-002",
        "name": "Aline Uwase",
        "institution": "African Leadership University (ALU)",
        "location": "Kigali, Rwanda (Remote / On-Site)",
        "availability": "Open to Paid Internship & Junior Analyst Roles",
        "linkedin": "https://linkedin.com",
        "cycle_number": "Cycle 01 (3 Months)",
        "credential_id": "TVX-3D91B7E4A205",
        "product_vertical": "TWEVIX CARE™ • Clinical & Cold-Chain Governance AI",
        "client_sector": "Healthcare & Cold-Chain Operations",
        "deployment_title": "Cold-Chain Drift Audit & 14-Day Roster Modeling for Outpatient Clinic",
        "problem_solved": "Manual fridge temperature logs missing early compressor drift and reactive weekend nurse overtime.",
        "verified_outcome": "Processed 2,160 hourly refrigeration logs via IsolationForest anomaly detection; flagged 2 early compressor drift events and balanced weekend shift coverage.",
        "stack": "TWEVIX CARE™ Engine | IsolationForest | Shift Telemetry",
        "issue_date": "2026-11-15",
    },
]

@st.cache_data(ttl=300)
def load_pulse_ledger():
    sheet_url = st.secrets.get("PULSE_SHEET_CSV_URL", "")
    if sheet_url:
        try:
            df = pd.read_csv(sheet_url)
            return df.fillna("").to_dict(orient="records")
        except Exception:
            pass
    return DEFAULT_RECORDS

records = load_pulse_ledger()

# Group cycles by analyst_id for HR-Tech view
grouped_analysts = {}
for row in records:
    aid = str(row.get("analyst_id", ""))
    if aid not in grouped_analysts:
        grouped_analysts[aid] = {
            "name": row.get("name", ""),
            "institution": row.get("institution", ""),
            "location": row.get("location", "Africa / Global Remote"),
            "availability": row.get("availability", "Open to Opportunities"),
            "linkedin": row.get("linkedin", "https://linkedin.com"),
            "cycles": [],
        }
    grouped_analysts[aid]["cycles"].append(row)

# --- HEADER & EXECUTIVE KPI BAR ---
st.title("TWEVIX Pulse™ | Solutions, Impact Telemetry & Talent SaaS")
st.markdown(
    "By **TWEVIX™** • Explore audited real-world deployments across **TechYatch Lab™** and **TWEVIX CARE™**, "
    "subscribe to on-demand problem-solving plans, or recruit **SHA-256 verified analysts**."
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Audited Deployments", f"{len(records)} Live Cases")
k2.metric("Verified Analysts", f"{len(grouped_analysts)} Active")
k3.metric("Stackable Tenure Model", "3 to 12+ Months")
k4.metric("Verification Standard", "SHA-256 Cryptographic")

st.divider()

# --- MAIN NAVIGATION TABS (MATERIAL VECTOR ICONS) ---
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/monitoring: Audited Solutions & Impact",
    ":material/layers: Subscribe & Solve Your Problem",
    ":material/person_search: Hire Verified Analysts",
    ":material/verified_user: SHA-256 Audit & Minting",
])

# ==============================================================================
# TAB 1: AUDITED SOLUTIONS & IMPACT TELEMETRY
# ==============================================================================
with tab1:
    st.subheader(":material/analytics: Real-World Problems Solved & Verified Impact Telemetry")
    st.caption("Inspect anonymized deployments executed by TWEVIX™ engines and supervised analyst pods.")

    sector_options = ["All Sectors"] + sorted(list({r.get("client_sector", "General") for r in records if r.get("client_sector")}))
    selected_sector = st.selectbox("Filter Solutions by Industry Sector", sector_options)

    for row in records:
        if selected_sector != "All Sectors" and row.get("client_sector") != selected_sector:
            continue
