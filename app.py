import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Ad Revenue & Performance Tracker",
    page_icon="📊",
    layout="wide"
)

# --- 2. SAMPLE DATA ---
# This simulates daily ad performance data across websites and ad formats
@st.cache_data
def get_sample_data():
    raw_data = [
        {"Date": "2026-11-10", "Website": "TechDaily.com", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 15000, "Clicks": 320, "Revenue_USD": 65.50},
        {"Date": "2026-11-10", "Website": "TechDaily.com", "Ad_Format": "Banner Ad", "Device": "Desktop", "Impressions": 28000, "Clicks": 180, "Revenue_USD": 28.00},
        {"Date": "2026-11-10", "Website": "NewsPulse.in", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 22000, "Clicks": 450, "Revenue_USD": 88.00},
        {"Date": "2026-11-10", "Website": "NewsPulse.in", "Ad_Format": "Banner Ad", "Device": "Mobile", "Impressions": 35000, "Clicks": 210, "Revenue_USD": 35.00},
        {"Date": "2026-11-10", "Website": "GamingZone.com", "Ad_Format": "Video Ad", "Device": "Desktop", "Impressions": 18000, "Clicks": 390, "Revenue_USD": 75.00},
        
        {"Date": "2026-11-11", "Website": "TechDaily.com", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 16500, "Clicks": 340, "Revenue_USD": 72.00},
        {"Date": "2026-11-11", "Website": "TechDaily.com", "Ad_Format": "Banner Ad", "Device": "Desktop", "Impressions": 26000, "Clicks": 160, "Revenue_USD": 26.00},
        {"Date": "2026-11-11", "Website": "NewsPulse.in", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 24000, "Clicks": 490, "Revenue_USD": 96.00},
        {"Date": "2026-11-11", "Website": "NewsPulse.in", "Ad_Format": "Banner Ad", "Device": "Mobile", "Impressions": 33000, "Clicks": 190, "Revenue_USD": 33.00},
        {"Date": "2026-11-11", "Website": "GamingZone.com", "Ad_Format": "Video Ad", "Device": "Desktop", "Impressions": 19500, "Clicks": 410, "Revenue_USD": 82.00},
        
        {"Date": "2026-11-12", "Website": "TechDaily.com", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 14000, "Clicks": 290, "Revenue_USD": 60.00},
        {"Date": "2026-11-12", "Website": "TechDaily.com", "Ad_Format": "Banner Ad", "Device": "Desktop", "Impressions": 29000, "Clicks": 175, "Revenue_USD": 29.00},
        {"Date": "2026-11-12", "Website": "NewsPulse.in", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 21000, "Clicks": 430, "Revenue_USD": 84.00},
        {"Date": "2026-11-12", "Website": "NewsPulse.in", "Ad_Format": "Banner Ad", "Device": "Mobile", "Impressions": 36000, "Clicks": 220, "Revenue_USD": 36.00},
        {"Date": "2026-11-12", "Website": "GamingZone.com", "Ad_Format": "Video Ad", "Device": "Desktop", "Impressions": 17000, "Clicks": 350, "Revenue_USD": 70.00},
        
        {"Date": "2026-11-13", "Website": "TechDaily.com", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 17500, "Clicks": 370, "Revenue_USD": 78.00},
        {"Date": "2026-11-13", "Website": "TechDaily.com", "Ad_Format": "Banner Ad", "Device": "Desktop", "Impressions": 27500, "Clicks": 190, "Revenue_USD": 27.50},
        {"Date": "2026-11-13", "Website": "NewsPulse.in", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 26000, "Clicks": 520, "Revenue_USD": 104.00},
        {"Date": "2026-11-13", "Website": "NewsPulse.in", "Ad_Format": "Banner Ad", "Device": "Mobile", "Impressions": 38000, "Clicks": 240, "Revenue_USD": 38.00},
        {"Date": "2026-11-13", "Website": "GamingZone.com", "Ad_Format": "Video Ad", "Device": "Desktop", "Impressions": 21000, "Clicks": 460, "Revenue_USD": 90.00},
        
        {"Date": "2026-11-14", "Website": "TechDaily.com", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 18000, "Clicks": 390, "Revenue_USD": 81.00},
        {"Date": "2026-11-14", "Website": "TechDaily.com", "Ad_Format": "Banner Ad", "Device": "Desktop", "Impressions": 31000, "Clicks": 210, "Revenue_USD": 31.00},
        {"Date": "2026-11-14", "Website": "NewsPulse.in", "Ad_Format": "Video Ad", "Device": "Mobile", "Impressions": 28000, "Clicks": 580, "Revenue_USD": 115.00},
        {"Date": "2026-11-14", "Website": "NewsPulse.in", "Ad_Format": "Banner Ad", "Device": "Mobile", "Impressions": 40000, "Clicks": 260, "Revenue_USD": 40.00},
        {"Date": "2026-11-14", "Website": "GamingZone.com", "Ad_Format": "Video Ad", "Device": "Desktop", "Impressions": 23000, "Clicks": 500, "Revenue_USD": 102.00},
    ]
    df = pd.DataFrame(raw_data)
    
    # Calculate key ad metrics
    # CTR (%) = (Clicks / Impressions) * 100
    df["CTR_%"] = round((df["Clicks"] / df["Impressions"]) * 100, 2)
    # eCPM ($) = (Revenue / Impressions) * 1000
    df["eCPM_$"] = round((df["Revenue_USD"] / df["Impressions"]) * 1000, 2)
    
    return df

df_all = get_sample_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")

selected_websites = st.sidebar.multiselect(
    "Select Websites:",
    options=sorted(df_all["Website"].unique()),
    default=sorted(df_all["Website"].unique())
)

selected_formats = st.sidebar.multiselect(
    "Select Ad Formats:",
    options=sorted(df_all["Ad_Format"].unique()),
    default=sorted(df_all["Ad_Format"].unique())
)

# Apply filters
filtered_df = df_all[
    (df_all["Website"].isin(selected_websites)) &
    (df_all["Ad_Format"].isin(selected_formats))
]

# --- 4. HEADER ---
st.title("📊 Daily Ad Revenue & Performance Tracker")
st.write("A clean, interactive dashboard to monitor daily advertising revenue, impressions, and engagement metrics.")

st.divider()

if filtered_df.empty:
    st.warning("Please select at least one website and one ad format from the sidebar.")
    st.stop()

# --- 5. TOP METRICS ROW ---
total_revenue = filtered_df["Revenue_USD"].sum()
total_impressions = filtered_df["Impressions"].sum()
total_clicks = filtered_df["Clicks"].sum()
avg_ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
avg_ecpm = (total_revenue / total_impressions) * 1000 if total_impressions > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("👁️ Total Impressions", f"{total_impressions:,.0f}")
col3.metric("🖱️ Total Clicks", f"{total_clicks:,.0f}")
col4.metric("📈 Overall CTR", f"{avg_ctr:.2f}%")
col5.metric("🏷️ Overall eCPM", f"${avg_ecpm:.2f}")

st.divider()

# --- 6. VISUAL CHARTS ---
col_left, col_right = st.columns(2)

with col_left:
    daily_rev = filtered_df.groupby(["Date", "Ad_Format"])["Revenue_USD"].sum().reset_index()
    fig_daily = px.bar(
        daily_rev,
        x="Date",
        y="Revenue_USD",
        color="Ad_Format",
        title="Daily Revenue Trend by Ad Format ($)",
        barmode="group",
        labels={"Revenue_USD": "Revenue ($)", "Date": "Date"}
    )
    fig_daily.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_daily, use_container_width=True)

with col_right:
    format_share = filtered_df.groupby("Ad_Format")["Revenue_USD"].sum().reset_index()
    fig_pie = px.pie(
        format_share,
        names="Ad_Format",
        values="Revenue_USD",
        title="Revenue Share by Ad Format",
        hole=0.4,
        color_discrete_sequence=["#2563EB", "#10B981"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Top website revenue
st.subheader("🌐 Revenue by Website")
site_rev = filtered_df.groupby("Website")["Revenue_USD"].sum().reset_index().sort_values(by="Revenue_USD", ascending=True)
fig_site = px.bar(
    site_rev,
    x="Revenue_USD",
    y="Website",
    orientation="h",
    title="Total Earnings per Website ($)",
    labels={"Revenue_USD": "Revenue ($)", "Website": "Website"},
    color="Revenue_USD",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_site, use_container_width=True)

st.divider()

# --- 7. DATA TABLE & CSV EXPORT ---
st.subheader("📋 Granular Performance Data")
st.dataframe(filtered_df, use_container_width=True)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV (for Excel)",
    data=csv_data,
    file_name="ad_performance_report.csv",
    mime="text/csv"
)

# --- 8. PROJECT EXPLANATION / METRIC GUIDE ---
with st.expander("ℹ️ About This Project & Metrics Explained"):
    st.markdown("""
    **Core Ad Operations Formulas Used in This App:**
    * **Impressions:** The number of times an advertisement was loaded and shown to a user.
    * **Clicks:** The number of times users clicked on the ad.
    * **CTR (Click-Through Rate):** $\\text{CTR (\\%)} = \\frac{\\text{Clicks}}{\\text{Impressions}} \\times 100$
    * **eCPM (Effective Cost Per Mille):** The estimated revenue earned per 1,000 ad impressions:
      $$\\text{eCPM (\\$)} = \\frac{\\text{Revenue}}{\\text{Impressions}} \\times 1000$$
    * **Business Value:** Helps publisher ad operations teams easily monitor which websites and ad formats (e.g. Video vs Banner) drive the highest revenue.
    """)
