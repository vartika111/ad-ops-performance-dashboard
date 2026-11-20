import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AdPulse 360 | Programmatic Ad Operations & Yield Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
    }
    .badge-critical {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-warning {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-good {
        background-color: #DCFCE7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "data", "programmatic_ad_performance.csv")
    if not os.path.exists(file_path):
        from generate_data import generate_ad_ops_dataset
        df = generate_ad_ops_dataset(output_path=file_path)
    else:
        df = pd.read_csv(file_path)
    
    df["date"] = pd.to_datetime(df["date"])
    return df

df_raw = load_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.image("https://img.icons8.com/fluency/96/bullish.png", width=64)
st.sidebar.markdown("## **AdPulse Operations**")
st.sidebar.caption("Programmatic Yield & Revenue Management")
st.sidebar.markdown("---")

# Date Filter
min_date = df_raw["date"].min().date()
max_date = df_raw["date"].max().date()
date_range = st.sidebar.date_input(
    "Select Reporting Window",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
else:
    start_d, end_d = min_date, max_date

# Multiselect Filters
publishers = st.sidebar.multiselect(
    "Publishers / Sites",
    options=sorted(df_raw["publisher"].unique()),
    default=sorted(df_raw["publisher"].unique())
)

ad_formats = st.sidebar.multiselect(
    "Ad Formats",
    options=sorted(df_raw["ad_format"].unique()),
    default=sorted(df_raw["ad_format"].unique())
)

demand_partners = st.sidebar.multiselect(
    "Demand Partners (SSPs)",
    options=sorted(df_raw["demand_partner"].unique()),
    default=sorted(df_raw["demand_partner"].unique())
)

devices = st.sidebar.multiselect(
    "Device Types",
    options=sorted(df_raw["device"].unique()),
    default=sorted(df_raw["device"].unique())
)

geos = st.sidebar.multiselect(
    "Geographic Tiers",
    options=sorted(df_raw["geo"].unique()),
    default=sorted(df_raw["geo"].unique())
)

# Apply Filters
mask = (
    (df_raw["date"].dt.date >= start_d) &
    (df_raw["date"].dt.date <= end_d) &
    (df_raw["publisher"].isin(publishers)) &
    (df_raw["ad_format"].isin(ad_formats)) &
    (df_raw["demand_partner"].isin(demand_partners)) &
    (df_raw["device"].isin(devices)) &
    (df_raw["geo"].isin(geos))
)
df = df_raw[mask].copy()

if df.empty:
    st.warning("⚠️ No data available for the chosen filters. Please expand your selections.")
    st.stop()

# --- TOP HEADER ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown('<p class="main-title">AdPulse 360° | Ad Operations & Yield Analytics</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="sub-title">Tracking programmatic monetization, bidder discrepancies & inventory yield across <b>{len(publishers)} Publishers</b> and <b>{len(demand_partners)} SSP Partners</b>.</p>',
        unsafe_allow_html=True
    )
with col_head2:
    st.markdown(
        """
        <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 10px; text-align: center;">
            <span style="font-size: 0.8rem; font-weight: 700; color: #1E40AF;">TARGET ROLE</span><br>
            <span style="font-size: 0.95rem; font-weight: 600; color: #1E3A8A;">Associate – Ad Operations</span><br>
            <span style="font-size: 0.75rem; color: #3B82F6;">VDO.AI / Z1 Tech Portfolio</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- AGGREGATED METRICS ---
total_requests = df["ad_requests"].sum()
total_ad_server_imps = df["ad_server_impressions"].sum()
total_ssp_imps = df["ssp_reported_impressions"].sum()
total_revenue = df["revenue_usd"].sum()
overall_fill_rate = (total_ad_server_imps / total_requests) * 100 if total_requests > 0 else 0
overall_ecpm = (total_revenue / total_ssp_imps) * 1000 if total_ssp_imps > 0 else 0
overall_ctr = (df["clicks"].sum() / total_ad_server_imps) * 100 if total_ad_server_imps > 0 else 0
overall_viewability = (df["viewable_impressions"].sum() / total_ad_server_imps) * 100 if total_ad_server_imps > 0 else 0
overall_discrepancy = ((total_ad_server_imps - total_ssp_imps) / total_ad_server_imps) * 100 if total_ad_server_imps > 0 else 0
total_discrepancy_loss = ((total_ad_server_imps - total_ssp_imps) * overall_ecpm) / 1000 if total_ad_server_imps > total_ssp_imps else 0

# --- TAB NAVIGATION ---
tab_exec, tab_yield, tab_discrepancy, tab_root_cause, tab_sop, tab_raw = st.tabs([
    "📈 Executive KPIs",
    "⚡ Yield & Partner Performance",
    "🔍 Discrepancy & Health Triage",
    "🤖 Root Cause & Revenue Optimizer",
    "📖 Ad Ops SOP & Knowledge Base",
    "📋 Data Explorer"
])

# ==============================================================================
# TAB 1: EXECUTIVE KPIS
# ==============================================================================
with tab_exec:
    st.subheader("Monetization & Delivery Summary")
    
    # KPI Cards Row
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)
    with kpi_col1:
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    with kpi_col2:
        st.metric(label="Ad Server Imps", value=f"{total_ad_server_imps:,.0f}")
    with kpi_col3:
        st.metric(label="Global Fill Rate", value=f"{overall_fill_rate:.1f}%")
    with kpi_col4:
        st.metric(label="Average eCPM", value=f"${overall_ecpm:.2f}")
    with kpi_col5:
        st.metric(label="CTR", value=f"{overall_ctr:.2f}%")
    with kpi_col6:
        st.metric(label="Viewability", value=f"{overall_viewability:.1f}%")

    st.markdown("---")

    # Trend Charts
    c1, c2 = st.columns([2, 1])
    with c1:
        daily_trend = df.groupby("date").agg({
            "revenue_usd": "sum",
            "ad_server_impressions": "sum",
            "ssp_reported_impressions": "sum"
        }).reset_index()
        daily_trend["daily_ecpm"] = (daily_trend["revenue_usd"] / daily_trend["ssp_reported_impressions"]) * 1000

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=daily_trend["date"],
            y=daily_trend["revenue_usd"],
            name="Daily Revenue ($)",
            marker_color="#2563EB",
            opacity=0.75,
            yaxis="y"
        ))
        fig_trend.add_trace(go.Scatter(
            x=daily_trend["date"],
            y=daily_trend["daily_ecpm"],
            name="Daily eCPM ($)",
            marker_color="#DC2626",
            mode="lines+markers",
            yaxis="y2",
            line=dict(width=2.5)
        ))
        fig_trend.update_layout(
            title="Daily Gross Revenue vs eCPM Trend",
            xaxis_title="Date",
            yaxis=dict(title="Revenue ($USD)", color="#2563EB"),
            yaxis2=dict(title="eCPM ($USD)", color="#DC2626", overlaying="y", side="right"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=40, r=40, t=50, b=40),
            height=380
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        format_rev = df.groupby("ad_format")["revenue_usd"].sum().reset_index()
        fig_pie = px.pie(
            format_rev,
            values="revenue_usd",
            names="ad_format",
            title="Revenue Share by Ad Format",
            hole=0.45,
            color_discrete_sequence=["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6"]
        )
        fig_pie.update_layout(height=380, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Publisher Breakdown Table
    st.subheader("Publisher Monetization Breakdown")
    pub_summary = df.groupby("publisher").agg({
        "ad_requests": "sum",
        "ad_server_impressions": "sum",
        "revenue_usd": "sum",
        "clicks": "sum",
        "viewable_impressions": "sum"
    }).reset_index()
    pub_summary["Fill Rate (%)"] = (pub_summary["ad_server_impressions"] / pub_summary["ad_requests"]) * 100
    pub_summary["eCPM ($)"] = (pub_summary["revenue_usd"] / pub_summary["ad_server_impressions"]) * 1000
    pub_summary["CTR (%)"] = (pub_summary["clicks"] / pub_summary["ad_server_impressions"]) * 100
    pub_summary["Viewability (%)"] = (pub_summary["viewable_impressions"] / pub_summary["ad_server_impressions"]) * 100
    pub_summary = pub_summary.rename(columns={
        "publisher": "Publisher Domain",
        "ad_requests": "Ad Requests",
        "ad_server_impressions": "Impressions",
        "revenue_usd": "Net Revenue ($)"
    })
    
    st.dataframe(
        pub_summary[[
            "Publisher Domain", "Ad Requests", "Impressions", "Fill Rate (%)",
            "eCPM ($)", "Net Revenue ($)", "CTR (%)", "Viewability (%)"
        ]].style.format({
            "Ad Requests": "{:,.0f}",
            "Impressions": "{:,.0f}",
            "Fill Rate (%)": "{:.1f}%",
            "eCPM ($)": "${:.2f}",
            "Net Revenue ($)": "${:,.2f}",
            "CTR (%)": "{:.2f}%",
            "Viewability (%)": "{:.1f}%"
        }),
        use_container_width=True
    )

# ==============================================================================
# TAB 2: YIELD & PARTNER PERFORMANCE
# ==============================================================================
with tab_yield:
    st.subheader("Demand Partner (SSP) Yield & Latency Benchmarks")

    ssp_agg = df.groupby("demand_partner").agg({
        "ad_requests": "sum",
        "ssp_reported_impressions": "sum",
        "revenue_usd": "sum",
        "bidder_latency_ms": "mean"
    }).reset_index()
    ssp_agg["Fill Rate (%)"] = (ssp_agg["ssp_reported_impressions"] / ssp_agg["ad_requests"]) * 100
    ssp_agg["eCPM ($)"] = (ssp_agg["revenue_usd"] / ssp_agg["ssp_reported_impressions"]) * 1000

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        fig_ssp_bar = px.bar(
            ssp_agg,
            x="demand_partner",
            y="revenue_usd",
            color="demand_partner",
            title="Total Revenue by SSP Partner",
            labels={"revenue_usd": "Revenue ($USD)", "demand_partner": "Demand Partner"},
            text_auto=".2s"
        )
        fig_ssp_bar.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_ssp_bar, use_container_width=True)

    with col_s2:
        fig_latency = px.scatter(
            ssp_agg,
            x="bidder_latency_ms",
            y="Fill Rate (%)",
            size="revenue_usd",
            color="demand_partner",
            hover_name="demand_partner",
            title="Bidder Latency vs. Fill Rate (Timeout Impact)",
            labels={"bidder_latency_ms": "Average Bidder Latency (ms)", "Fill Rate (%)": "Fill Rate (%)"}
        )
        fig_latency.add_vline(x=800, line_dash="dash", line_color="red", annotation_text="Prebid Timeout 800ms")
        fig_latency.update_layout(height=350)
        st.plotly_chart(fig_latency, use_container_width=True)

    # eCPM Heatmap across GEO and Ad Format
    st.subheader("eCPM Heatmap: Ad Format vs. Geography")
    pivot_ecpm = df.pivot_table(
        index="ad_format",
        columns="geo",
        values="revenue_usd",
        aggfunc=lambda x: (x.sum() / df.loc[x.index, "ssp_reported_impressions"].sum()) * 1000
    ).round(2)

    fig_heat = px.imshow(
        pivot_ecpm,
        text_auto=".2f",
        labels=dict(x="Geo Tier", y="Ad Format", color="eCPM ($)"),
        title="Average eCPM ($) Matrix across Inventory and Regions",
        color_continuous_scale="Viridis"
    )
    fig_heat.update_layout(height=320)
    st.plotly_chart(fig_heat, use_container_width=True)

# ==============================================================================
# TAB 3: DISCREPANCY & HEALTH TRIAGE
# ==============================================================================
with tab_discrepancy:
    st.subheader("Partner Discrepancy & Revenue Leakage Audit")
    st.info(
        "💡 **Ad Ops Core Workflow**: In digital advertising, discrepancies occur when the Publisher Ad Server "
        "counts an impression, but the Demand Partner (SSP) drops it due to timeouts, tracking pixel drop-offs, "
        "or anti-fraud invalid traffic filtering. **Industry Standard tolerance is < 10%**. "
        "Anything above 10% indicates lost publisher revenue and requires technical escalation."
    )

    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        st.metric(
            label="Overall Discrepancy Rate",
            value=f"{overall_discrepancy:.2f}%",
            delta="- Normal" if overall_discrepancy < 10 else "+ CRITICAL LEAKAGE",
            delta_color="inverse"
        )
    with d_col2:
        st.metric(
            label="Estimated Financial Leakage",
            value=f"${total_discrepancy_loss:,.2f}",
            help="Unbilled impressions delivered by publisher ad server that were not compensated by SSPs."
        )
    with d_col3:
        high_disc_partners = df.groupby("demand_partner").apply(
            lambda x: ((x["ad_server_impressions"].sum() - x["ssp_reported_impressions"].sum()) / x["ad_server_impressions"].sum()) * 100
        )
        critical_count = (high_disc_partners > 10).sum()
        st.metric(label="Partners in Breach (>10%)", value=f"{critical_count} / {len(demand_partners)}")

    st.markdown("---")

    # Discrepancy Trend by SSP over Time
    disc_time = df.groupby(["date", "demand_partner"]).agg({
        "ad_server_impressions": "sum",
        "ssp_reported_impressions": "sum"
    }).reset_index()
    disc_time["discrepancy_pct"] = (
        (disc_time["ad_server_impressions"] - disc_time["ssp_reported_impressions"]) / disc_time["ad_server_impressions"]
    ) * 100

    fig_disc_line = px.line(
        disc_time,
        x="date",
        y="discrepancy_pct",
        color="demand_partner",
        title="Daily Partner Discrepancy Rate (%)",
        labels={"discrepancy_pct": "Discrepancy (%)", "date": "Date"}
    )
    fig_disc_line.add_hline(y=10.0, line_dash="dash", line_color="red", annotation_text="Max 10% SLA Threshold")
    fig_disc_line.update_layout(height=400)
    st.plotly_chart(fig_disc_line, use_container_width=True)

    # Discrepancy Audit Table
    st.subheader("Partner Discrepancy Scorecard")
    disc_table = df.groupby("demand_partner").agg({
        "ad_server_impressions": "sum",
        "ssp_reported_impressions": "sum",
        "revenue_usd": "sum"
    }).reset_index()
    disc_table["Discrepancy %"] = (
        (disc_table["ad_server_impressions"] - disc_table["ssp_reported_impressions"]) / disc_table["ad_server_impressions"]
    ) * 100
    disc_table["Avg eCPM ($)"] = (disc_table["revenue_usd"] / disc_table["ssp_reported_impressions"]) * 1000
    disc_table["Est. Lost Revenue ($)"] = (
        (disc_table["ad_server_impressions"] - disc_table["ssp_reported_impressions"]) * disc_table["Avg eCPM ($)"]
    ) / 1000
    disc_table["Est. Lost Revenue ($)"] = disc_table["Est. Lost Revenue ($)"].apply(lambda x: max(x, 0))

    def style_status(row):
        val = row["Discrepancy %"]
        if val > 10.0:
            return "🔴 CRITICAL (Breach > 10%)"
        elif val >= 5.0:
            return "🟡 MODERATE (5% - 10%)"
        return "🟢 HEALTHY (< 5%)"

    disc_table["Audit Status"] = disc_table.apply(style_status, axis=1)

    st.dataframe(
        disc_table[[
            "demand_partner", "ad_server_impressions", "ssp_reported_impressions",
            "Discrepancy %", "Est. Lost Revenue ($)", "Audit Status"
        ]].rename(columns={
            "demand_partner": "Demand Partner (SSP)",
            "ad_server_impressions": "Ad Server Impressions",
            "ssp_reported_impressions": "SSP Counted Impressions"
        }).style.format({
            "Ad Server Impressions": "{:,.0f}",
            "SSP Counted Impressions": "{:,.0f}",
            "Discrepancy %": "{:.2f}%",
            "Est. Lost Revenue ($)": "${:,.2f}"
        }),
        use_container_width=True
    )

# ==============================================================================
# TAB 4: ROOT CAUSE & YIELD OPTIMIZER
# ==============================================================================
with tab_root_cause:
    st.subheader("Ad Ops Automated Anomaly & Root Cause Diagnostics")
    st.markdown("Automated algorithmic checks scanning for common programmatic failure modes:")

    # Anomaly Engine Scans
    # Scan 1: High Discrepancy
    high_disc_slices = df[df["discrepancy_pct"] > 10.0]
    if not high_disc_slices.empty:
        top_disc_partner = high_disc_slices.groupby("demand_partner")["discrepancy_loss_usd"].sum().idxmax()
        top_disc_loss = high_disc_slices.groupby("demand_partner")["discrepancy_loss_usd"].sum().max()
        st.error(
            f"🚨 **High Discrepancy Detected:** Partner **{top_disc_partner}** has sustained discrepancies above the 10% SLA threshold, "
            f"resulting in **${top_disc_loss:,.2f}** in unbilled delivery.\n\n"
            f"- **Root Cause Analysis:** Average bidder response latency is {high_disc_slices['bidder_latency_ms'].mean():.0f}ms (exceeding standard 800ms Prebid auction timeout). Video player drops creative before tracking pixel fires.\n"
            f"- **Ad Ops Action Plan:** 1. Raise Prebid auction timeout to 1200ms. 2. Contact {top_disc_partner} TAM to confirm VAST wrapper redirection limits. 3. Initiate monthly discrepancy credit reconciliation."
        )

    # Scan 2: eCPM Drops
    ecpm_by_format = df.groupby(["ad_format", "geo"]).agg({
        "revenue_usd": "sum",
        "ssp_reported_impressions": "sum"
    }).reset_index()
    ecpm_by_format["ecpm"] = (ecpm_by_format["revenue_usd"] / ecpm_by_format["ssp_reported_impressions"]) * 1000
    low_ecpm = ecpm_by_format[ecpm_by_format["ecpm"] < 1.0]
    if not low_ecpm.empty:
        st.warning(
            f"⚠️ **Low Yield Warning:** Tier 3 inventory on banner formats is yielding sub-$1.00 eCPM. "
            f"- **Ad Ops Action Plan:** Implement unified dynamic floor pricing (Unified Price Rules in GAM) to prevent floor erosion."
        )

    # Scan 3: Low Fill Rate Placements
    low_fill = df[df["fill_rate_pct"] < 40.0]
    if not low_fill.empty:
        worst_pub = low_fill.groupby("publisher")["ad_requests"].sum().idxmax()
        st.info(
            f"ℹ️ **Fill Rate Optimization Opportunity:** Publisher **{worst_pub}** has placements with fill rates below 40%. "
            f"- **Ad Ops Action Plan:** Add 2 complementary SSP bidders in Prebid header bidding config to increase bid density."
        )

    st.markdown("---")

    # Interactive Yield Simulator
    st.subheader("Simulated Yield Uplift Calculator")
    st.caption("Adjust sliders to estimate the financial impact of your Ad Ops optimization strategies:")

    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        uplift_fill = st.slider("Target Fill Rate Uplift (%)", min_value=0.0, max_value=15.0, value=3.5, step=0.5)
        reduce_disc = st.slider("Target Discrepancy Reduction (%)", min_value=0.0, max_value=8.0, value=2.0, step=0.5)

    with sim_col2:
        new_imps = total_requests * ((overall_fill_rate + uplift_fill) / 100)
        additional_imps = new_imps - total_ad_server_imps
        gain_from_fill = (additional_imps * overall_ecpm) / 1000
        gain_from_disc = total_revenue * (reduce_disc / 100)
        total_monthly_gain = gain_from_fill + gain_from_disc

        st.markdown(
            f"""
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 20px;">
                <h4 style="color: #166534; margin: 0 0 10px 0;">Projected Incremental Publisher Revenue</h4>
                <p style="font-size: 2.2rem; font-weight: 700; color: #15803D; margin: 0;">+${total_monthly_gain:,.2f}</p>
                <p style="color: #166534; font-size: 0.9rem; margin-top: 5px;">
                    • <b>${gain_from_fill:,.2f}</b> from adding demand density (+{uplift_fill}% fill rate)<br>
                    • <b>${gain_from_disc:,.2f}</b> recovered from technical discrepancy triage (-{reduce_disc}% discrepancy)
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==============================================================================
# TAB 5: SOP & KNOWLEDGE BASE
# ==============================================================================
with tab_sop:
    st.subheader("Ad Operations Standard Operating Procedures (SOP)")
    st.markdown("Documented operational workflows for publisher account management and technical troubleshooting:")

    with st.expander("📌 SOP 101: Investigating a >10% SSP Discrepancy Spike", expanded=True):
        st.markdown("""
        **Trigger:** Daily reporting indicates partner discrepancy $> 10\%$ between Ad Server impressions and SSP reports.
        
        **Standard Resolution Steps:**
        1. **Verify Timezone Alignments:** Ensure Ad Server (e.g. Google Ad Manager on EST/UTC) and Partner reporting use identical timezone boundaries.
        2. **Inspect Prebid Timeout Settings:** Compare partner bidder latency against Prebid timeout (e.g. if SSP average latency is 920ms and timeout is 800ms, the auction closes before bids return).
        3. **Check VAST Error Codes:** For video ad formats (In-stream / Outstream), inspect VAST error logs:
           - *VAST 303 (No Ad Response)*: Inventory was requested but creative was not returned.
           - *VAST 405 (MediaFile display error)*: Player cannot decode video bitrate or codec on mobile.
           - *VAST 901 (General VPAID Error)*: JavaScript VPAID wrapper timed out.
        4. **Initiate Discrepancy Dispute:** If the gap exceeds 10% for $>3$ consecutive days, pull hourly log files, attach client-side console traces, and send standard reconciliation notice to the SSP Technical Account Manager (TAM).
        """)

    with st.expander("📌 SOP 102: Triaging Sudden eCPM & Revenue Drop"):
        st.markdown("""
        **Trigger:** Overnight revenue drop $> 15\%$ on an active publisher domain.
        
        **Standard Resolution Steps:**
        1. **Isolate the Dimension:** Filter data by Ad Format, Geo, and Device to determine if the drop is systemic or localized.
        2. **Verify Floor Price Rules (UPRs):** Check Google Ad Manager Unified Pricing Rules to ensure floor prices weren't inadvertently increased or changed.
        3. **Check Ads.txt Compliance:** Run a crawl on `publisher.com/ads.txt` to confirm demand partner reseller/direct lines are valid and not flagged by buyers.
        4. **Inspect Viewability Scores:** Check if publisher layout changes pushed ad units below the fold, dropping MRC viewability below buyer threshold (50%).
        """)

    with st.expander("📌 SOP 103: Video Ad Quality & Latency Optimization"):
        st.markdown("""
        **Objective:** Maximize fill rate and user experience for high-impact outstream video placements.
        
        **Key Guidelines:**
        - **Autoplay Policies:** Ensure all mobile video tags have `muted="true"` and `playsinline="true"` attributes to adhere to Chrome/Safari autoplay policies.
        - **Lazy Loading Threshold:** Initialize video player when the container is within 250px of the viewport to optimize viewability without causing pre-render timeouts.
        - **Ad Server Priority:** Place direct video campaigns at Priority 6-8 (Sponsorship/Standard) and programmatic backfill at Priority 12 (Price Priority / Ad Exchange).
        """)

# ==============================================================================
# TAB 6: DATA EXPLORER & CSV EXPORT
# ==============================================================================
with tab_raw:
    st.subheader("Programmatic Log Data Explorer")
    st.markdown("Inspect granular records and export filtered operational logs for Excel analysis:")

    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Operational Logs (CSV for Excel)",
        data=csv_data,
        file_name=f"ad_ops_performance_{start_d}_to_{end_d}.csv",
        mime="text/csv"
    )

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>"
    "AdPulse 360° | Built with Python, Streamlit & Plotly | Designed for Ad Operations & Programmatic Monetization Roles"
    "</div>",
    unsafe_allow_html=True
)
