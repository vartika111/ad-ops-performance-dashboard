"""
Programmatic Ad Operations & Revenue Optimization - Synthetic Dataset Generator
Simulates realistic daily multi-partner ad serving, header bidding, and video ad performance logs.
Includes intentional real-world Ad Ops anomalies (e.g. discrepancy spikes, eCPM drops, timeouts)
designed for triage and yield optimization analysis.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_ad_ops_dataset(
    start_date_str="2026-10-01",
    days=50,
    output_path="data/programmatic_ad_performance.csv"
):
    random.seed(42)
    np.random.seed(42)

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    dates = [start_date + timedelta(days=i) for i in range(days)]

    publishers = [
        "TechPulse_Global",
        "DailyNews_Network",
        "SportsVibe_Media",
        "GamingSphere_Live",
        "AutoTrend_Hub"
    ]

    ad_formats = {
        "In-Stream Video": {"base_eCPM_t1": 5.80, "base_fill": 0.65, "ctr_range": (0.012, 0.028), "viewability": (0.75, 0.90)},
        "Outstream Video": {"base_eCPM_t1": 3.90, "base_fill": 0.72, "ctr_range": (0.008, 0.018), "viewability": (0.62, 0.78)},
        "Sticky Banner": {"base_eCPM_t1": 1.60, "base_fill": 0.85, "ctr_range": (0.004, 0.012), "viewability": (0.70, 0.88)},
        "Interstitial": {"base_eCPM_t1": 4.20, "base_fill": 0.58, "ctr_range": (0.015, 0.035), "viewability": (0.80, 0.95)},
    }

    geo_multipliers = {
        "Tier 1 (US/UK/CA)": 1.0,
        "Tier 2 (DE/FR/AU)": 0.58,
        "Tier 3 (IN/BR/ID)": 0.28
    }

    devices = ["Mobile", "Desktop", "Tablet"]
    device_weights = [0.62, 0.31, 0.07]

    ssp_partners = ["Google AdX", "Magnite", "PubMatic", "OpenX", "Index Exchange"]
    ssp_shares = [0.38, 0.24, 0.18, 0.12, 0.08]

    records = []

    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        is_weekend = date.weekday() >= 5
        traffic_factor = 1.15 if is_weekend else 1.0

        for pub in publishers:
            pub_scale = {
                "TechPulse_Global": 1.4,
                "DailyNews_Network": 1.8,
                "SportsVibe_Media": 1.2,
                "GamingSphere_Live": 1.0,
                "AutoTrend_Hub": 0.7
            }[pub]

            for fmt_name, fmt_meta in ad_formats.items():
                for geo, geo_mult in geo_multipliers.items():
                    device = np.random.choice(devices, p=device_weights)
                    
                    # Base request volume
                    base_requests = int(np.random.uniform(4000, 18000) * pub_scale * traffic_factor)
                    if device == "Tablet":
                        base_requests = int(base_requests * 0.25)
                    elif device == "Desktop" and fmt_name == "Sticky Banner":
                        base_requests = int(base_requests * 0.6)

                    # Split requests across SSPs
                    for ssp, share in zip(ssp_partners, ssp_shares):
                        ssp_requests = int(base_requests * share * np.random.uniform(0.9, 1.1))
                        if ssp_requests < 100:
                            continue

                        # Base fill rate
                        fill_rate = fmt_meta["base_fill"] * np.random.uniform(0.92, 1.06)
                        fill_rate = min(max(fill_rate, 0.20), 0.95)

                        # Calculate Ad Server Impressions
                        ad_server_imps = int(ssp_requests * fill_rate)

                        # Base eCPM
                        ecpm = fmt_meta["base_eCPM_t1"] * geo_mult * np.random.uniform(0.88, 1.12)

                        # Discrepancy modeling: Normal is 1-4%
                        discrepancy_factor = np.random.uniform(0.015, 0.040)

                        # --- INJECT REALISTIC ANOMALY 1: PubMatic Outstream VAST Timeout ---
                        # Date >= 2026-11-08 on Mobile Outstream for PubMatic
                        if date >= datetime(2026, 11, 8) and ssp == "PubMatic" and fmt_name == "Outstream Video" and device == "Mobile":
                            discrepancy_factor = np.random.uniform(0.145, 0.175) # 15-17% discrepancy!

                        # --- INJECT REALISTIC ANOMALY 2: Google AdX Floor Price Misconfiguration ---
                        # Between 2026-11-13 and 2026-11-16, Tier 3 Desktop In-Stream Video
                        if datetime(2026, 11, 13) <= date <= datetime(2026, 11, 16) and ssp == "Google AdX" and geo == "Tier 3 (IN/BR/ID)" and fmt_name == "In-Stream Video":
                            ecpm = ecpm * 0.38  # Sudden 62% collapse in eCPM!

                        # --- INJECT REALISTIC ANOMALY 3: OpenX Match Rate Drop ---
                        if date >= datetime(2026, 11, 15) and ssp == "OpenX" and pub == "GamingSphere_Live":
                            ad_server_imps = int(ad_server_imps * 0.45) # Bidder timeout / line item halted

                        # SSP Reported impressions (Ad server usually counts slightly higher due to dropped impressions before SSP fires pixel)
                        ssp_imps = int(ad_server_imps * (1.0 - discrepancy_factor))
                        ssp_imps = max(ssp_imps, 10)

                        # Revenue
                        revenue = round((ssp_imps * ecpm) / 1000.0, 2)

                        # Clicks & Viewability
                        ctr = np.random.uniform(fmt_meta["ctr_range"][0], fmt_meta["ctr_range"][1])
                        clicks = int(ad_server_imps * ctr)

                        view_rate = np.random.uniform(fmt_meta["viewability"][0], fmt_meta["viewability"][1])
                        viewable_imps = int(ad_server_imps * view_rate)

                        # Latency in ms (SSP response time)
                        latency_ms = int(np.random.normal(320, 45))
                        if ssp == "PubMatic" and date >= datetime(2026, 11, 8) and fmt_name == "Outstream Video":
                            latency_ms = int(np.random.normal(920, 110)) # high latency causing timeouts

                        records.append({
                            "date": date_str,
                            "publisher": pub,
                            "ad_format": fmt_name,
                            "geo": geo,
                            "device": device,
                            "demand_partner": ssp,
                            "ad_requests": ssp_requests,
                            "ad_server_impressions": ad_server_imps,
                            "ssp_reported_impressions": ssp_imps,
                            "revenue_usd": revenue,
                            "clicks": clicks,
                            "viewable_impressions": viewable_imps,
                            "bidder_latency_ms": latency_ms
                        })

    df = pd.DataFrame(records)

    # Derived calculated columns
    df["fill_rate_pct"] = round((df["ad_server_impressions"] / df["ad_requests"]) * 100.0, 2)
    df["ecpm_usd"] = round((df["revenue_usd"] / df["ssp_reported_impressions"]) * 1000.0, 2)
    df["ctr_pct"] = round((df["clicks"] / df["ad_server_impressions"]) * 100.0, 3)
    df["viewability_pct"] = round((df["viewable_impressions"] / df["ad_server_impressions"]) * 100.0, 2)
    df["discrepancy_pct"] = round(
        ((df["ad_server_impressions"] - df["ssp_reported_impressions"]) / df["ad_server_impressions"]) * 100.0, 2
    )
    df["discrepancy_loss_usd"] = round(
        ((df["ad_server_impressions"] - df["ssp_reported_impressions"]) * df["ecpm_usd"]) / 1000.0, 2
    )
    # Floor negative loss at 0
    df["discrepancy_loss_usd"] = df["discrepancy_loss_usd"].apply(lambda x: max(x, 0.0))

    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset generated successfully! Shape: {df.shape}")
    print(f"Saved to: {output_path}")
    return df

if __name__ == "__main__":
    generate_ad_ops_dataset()
