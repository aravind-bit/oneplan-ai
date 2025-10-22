# app.py — OnePlan AI Executive Story App (clean, with diagnostics)
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

DATA_DIR   = Path("data/processed")
ASSETS_DIR = Path("assets")
REPORTS_DIR= Path("reports")

st.set_page_config(page_title="OnePlan AI — Media Budget Optimizer", layout="wide")

st.title("OnePlan AI — Intelligent Media Budget Optimizer")
st.subheader("A concise executive story: what changed, why it changed, and the impact.")

@st.cache_data
def load_csv(p: Path):
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
        return df if len(df) > 0 else None
    except Exception:
        return None

# --- Load artifacts (non-fatal if missing) ---
# --- Load artifacts (non-fatal if missing) ---
summary = None
first_path = DATA_DIR / "part6_equal_vs_optimized_summary.csv"
fallback_path = DATA_DIR / "part5_equal_vs_optimized_summary.csv"

if (df := load_csv(first_path)) is not None:
    summary = df
elif (df := load_csv(fallback_path)) is not None:
    summary = df
else:
    summary = None
mroi    = load_csv(DATA_DIR/"marginal_roi_summary.csv")
alloc_c = load_csv(DATA_DIR/"optimal_spend_conversions.csv")
alloc_r = load_csv(DATA_DIR/"optimal_spend_reach.csv")

img_conv = ASSETS_DIR/"p6_equal_vs_opt_conversions.png"
img_rech = ASSETS_DIR/"p6_equal_vs_opt_reach.png"

# --- Diagnostics panel (collapsible) ---
with st.expander("Diagnostic status (for setup/troubleshooting)"):
    def ok(x): return "✅" if x else "❌"
    st.write("Files found:")
    st.write({
        "part6_equal_vs_optimized_summary.csv": (DATA_DIR/"part6_equal_vs_optimized_summary.csv").exists(),
        "part5_equal_vs_optimized_summary.csv": (DATA_DIR/"part5_equal_vs_optimized_summary.csv").exists(),
        "marginal_roi_summary.csv": (DATA_DIR/"marginal_roi_summary.csv").exists(),
        "optimal_spend_conversions.csv": (DATA_DIR/"optimal_spend_conversions.csv").exists(),
        "optimal_spend_reach.csv": (DATA_DIR/"optimal_spend_reach.csv").exists(),
        "assets/p6_equal_vs_opt_conversions.png": img_conv.exists(),
        "assets/p6_equal_vs_opt_reach.png": img_rech.exists(),
    })

# --- TL;DR KPIs ---
st.markdown("### Overall Impact")
if summary is None or len(summary) < 2:
    st.warning("Processed summary files not found. Please run Parts 5–6 and push the CSV outputs.")
else:
    conv = summary.iloc[0]  # conversions
    rech = summary.iloc[1]  # deduped_reach_fraction
    c1, c2, c3 = st.columns(3)
    c1.metric("Conversions Lift", f"{conv['lift_%']:.1f}%")
    c2.metric("Reach Lift", f"{rech['lift_%']:.1f}%")
    c3.metric("Optimized Conversions", f"{conv['optimized']:.1f}")
    st.caption("Optimizing for conversions can reduce reach — a deliberate efficiency trade-off.")

st.divider()

# --- Why the budget shifted ---
st.markdown("### Why the Budget Shifted")
colA, colB = st.columns(2)

with colA:
    st.markdown("Optimal Spend by Channel (Conversions Objective)")
    if alloc_c is not None and "channel" in alloc_c.columns and "optimal_spend_conversions" in alloc_c.columns:
        fig = px.bar(alloc_c.sort_values("optimal_spend_conversions", ascending=False),
                     x="channel", y="optimal_spend_conversions",
                     labels={"optimal_spend_conversions": "USD", "channel": "Channel"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Missing or malformed: data/processed/optimal_spend_conversions.csv")

with colB:
    st.markdown("Marginal ROI by Channel")
    if mroi is not None and "channel" in mroi.columns and "marginal_roi_per_dollar" in mroi.columns:
        fig = px.bar(mroi.sort_values("marginal_roi_per_dollar", ascending=False),
                     x="channel", y="marginal_roi_per_dollar",
                     labels={"marginal_roi_per_dollar": "Δ Conversions per $1", "channel": "Channel"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Missing or malformed: data/processed/marginal_roi_summary.csv")

st.divider()

# --- Equal vs Optimized (images) ---
st.markdown("### Equal vs Optimized")
col1, col2 = st.columns(2)
with col1:
    if img_conv.exists():
        st.image(str(img_conv), caption="Conversions: Equal vs Optimized")
    else:
        st.info("Missing: assets/p6_equal_vs_opt_conversions.png")
with col2:
    if img_rech.exists():
        st.image(str(img_rech), caption="Reach: Equal vs Optimized")
    else:
        st.info("Missing: assets/p6_equal_vs_opt_reach.png")

st.divider()

# --- Downloads ---
st.markdown("### Downloads")
rpt = REPORTS_DIR/"OnePlan_Executive_Summary.md"
if rpt.exists():
    st.download_button("Download Executive Summary", rpt.read_text(encoding="utf-8"),
                       file_name="OnePlan_Executive_Summary.md")
else:
    st.info("Generate reports/OnePlan_Executive_Summary.md in Part-6 to enable this download.")

if summary is not None:
    st.download_button("Download Summary CSV", summary.to_csv(index=False),
                       file_name="equal_vs_optimized_summary.csv")