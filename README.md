# AdPulse 360° | Programmatic Ad Operations & Yield Optimization Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.20+-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive, production-grade Ad Operations analytics and yield optimization dashboard tailored for digital advertising technology (AdTech) teams. Built specifically to demonstrate hands-on programmatic expertise, multi-partner yield tracking, bidder discrepancy triage, and revenue leak detection.

Targeted for roles such as **Associate – Ad Operations** at **VDO.AI (Z1 Tech)**, digital publishers, SSPs, and AdTech networks.

---

## 📌 Executive Summary & JD Alignment

This project directly fulfills the core competencies requested in the **Associate – Ad Operations** Job Description:

| Job Description Requirement | How This Project Delivers |
| :--- | :--- |
| **"Handle day-to-day programmatic advertising operations"** | Tracks multi-SSP header bidding operations across Google AdX, Magnite, PubMatic, OpenX, and Index Exchange. |
| **"Track daily revenue & monitor ad performance"** | Interactive time-series tracking of Gross Revenue, Impressions, Fill Rates, eCPM, CTR, and Viewability. |
| **"Spot areas for improvement & identify trends"** | Evaluates bidder latency impact, geo/format yield matrices, and root causes behind underperforming ad units. |
| **"Ensure ads meet quality standards"** | Audits VAST video rendering errors (VAST 303, 405, 901) and mobile video latency benchmarks. |
| **"Create process documents & knowledge base"** | Includes complete operational Standard Operating Procedures ([ad_ops_sop.md](ad_ops_sop.md)) for discrepancy disputes & triage. |
| **"CS/Engineering Degree + Data Analysis & Excel"** | Combines algorithmic data simulation, Pandas analytics, Plotly data visualizations, and one-click Excel CSV export. |

---

## 📊 Core AdTech Metrics & Business Logic

| Metric | Calculation / Formula | Ad Ops Significance |
| :--- | :--- | :--- |
| **Ad Requests** | Count of ad opportunities initiated by publisher page | Base supply volume |
| **Ad Server Impressions** | Impressions rendered according to publisher ad server (GAM) | Primary delivery benchmark |
| **SSP Impressions** | Impressions billed and acknowledged by Demand Partner | Billable transaction volume |
| **Fill Rate (%)** | `(Ad Server Impressions / Ad Requests) * 100` | Inventory monetization efficiency |
| **eCPM ($USD)** | `(Net Revenue / SSP Impressions) * 1000` | Effective Cost Per Thousand Impressions |
| **Partner Discrepancy (%)**| `((Ad Server Imps - SSP Imps) / Ad Server Imps) * 100` | SLA tolerance threshold is `< 10%`. Gaps $>10\%$ represent unbilled delivery. |
| **Discrepancy Loss ($)** | `((Ad Server Imps - SSP Imps) * eCPM) / 1000` | Dollar value of publisher inventory rendered for free. |

---

## 🚀 Key Dashboard Features (6 Functional Tabs)

1. **Executive Revenue & Delivery KPIs:** High-level metric cards, dual-axis daily revenue vs. eCPM trends, ad format revenue share (Outstream, In-Stream, Sticky Banner, Interstitial), and publisher-level delivery scorecards.
2. **Yield & Partner Performance:** SSP revenue contribution bar charts, interactive scatter plot analyzing **Bidder Latency vs. Fill Rate**, and eCPM heatmaps comparing Ad Formats vs. Geographic Tiers.
3. **Discrepancy & Health Triage:** Dedicated auditing engine color-coding demand partners into Safe ($<5\%$), Moderate ($5\% - 10\%$), and Critical ($>10\%$) discrepancy categories, along with financial loss estimations.
4. **Automated Root Cause Diagnostics & Yield Optimizer:** Rule-based detection alerting engineers to bidder timeout spikes, floor price misconfigurations, and an interactive **Simulated Yield Uplift Calculator**.
5. **Ad Ops SOP & Knowledge Base:** Built-in standard operational handbook for discrepancy dispute resolution, eCPM crash troubleshooting, and VAST error diagnostics.
6. **Data Explorer & Excel Export:** Granular record inspection with dynamic column filtering and one-click CSV export for Excel reporting.

---

## 🛠️ Tech Stack & Directory Structure

* **Language:** Python 3.11+
* **Framework:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly Express & Plotly Graph Objects

```text
ad-ops-performance-dashboard/
├── app.py                            # Main Streamlit web application
├── generate_data.py                  # Synthetic programmatic log generator with anomaly injection
├── ad_ops_sop.md                     # Complete Ad Ops Troubleshooting SOP & Knowledge Base
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore file
├── README.md                         # Project documentation & hosting guide
└── data/
    └── programmatic_ad_performance.csv  # Realistic pre-generated multi-SSP dataset
```

---

## 💻 Local Quickstart Guide

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ad-ops-performance-dashboard.git
cd ad-ops-performance-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate dataset (optional, pre-generated file included)
```bash
python generate_data.py
```

### 4. Launch the dashboard locally
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🌐 How to Host for Free on Streamlit Community Cloud (Step-by-Step)

Hosting this dashboard online allows recruiters and hiring managers at VDO.AI to click a live link directly from your resume!

### Step 1: Initialize Git and Push to GitHub
1. Create a new repository on [GitHub](https://github.com/new) named `ad-ops-performance-dashboard` (set it to **Public**).
2. In your local project folder terminal, run:
```bash
git init
git add .
git commit -m "feat: initial commit of programmatic ad ops dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ad-ops-performance-dashboard.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Community Cloud (100% Free)
1. Go to [share.streamlit.io](https://share.streamlit.io/) and click **Sign in with GitHub**.
2. Click **New app**.
3. Select your repository: `YOUR_GITHUB_USERNAME/ad-ops-performance-dashboard`.
4. Set branch: `main`.
5. Set Main file path: `app.py`.
6. Click **Deploy!**

In ~2 minutes, your live web application will be live at:
`https://ad-ops-performance-dashboard-YOUR_USERNAME.streamlit.app`

---

## 🎯 Talking Points for Your Interview at VDO.AI

During an interview, you can directly showcase this project to answer common Ad Ops questions:
* **"How do you monitor daily revenue and identify performance drops?"**  
  * *"In my project, I built a dual-axis monitoring pipeline tracking daily revenue alongside eCPM. When looking at Tab 1 and Tab 4, the dashboard flags isolated dips—for instance, distinguishing between a site-wide traffic drop versus an eCPM collapse caused by a floor price adjustment."*
* **"What is partner discrepancy, and how do you resolve it?"**  
  * *"Discrepancy is the delta between what our ad server logs and what the demand partner acknowledges. In Tab 3 of my project, I implemented an automated audit engine that flags any partner exceeding the 10% SLA threshold. For example, my dataset models a scenario where PubMatic's latency exceeded the 800ms Prebid timeout, leading to unbilled impressions. I also authored an SOP guide covering VAST error codes (303, 405, 901) and dispute reconciliation."*
* **"How can you improve ad revenue?"**  
  * *"Through yield optimization: analyzing bidder latency to reduce dropped impressions, testing dynamic floor prices, and increasing bid density by integrating complementary SSPs for low-fill formats."*

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
