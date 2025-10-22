# app.py — OnePlan AI Story App (Streamlit)
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR   = Path("data/processed")
ASSETS_DIR = Path("assets")
REPORTS_DIR= Path("reports")

st.set_page_config(page_title="OnePlan AI — Media Budget Optimizer", page_icon="🧠", layout="wide")
st.title("🧠 OnePlan AI — Intelligent Media Budget Optimizer")
st.subheader("What changed, why it changed, and the impact — in one page.")

@st.cache_data
def load_csv(p: Path):
    if not p.exists(): return None
    try: return pd.read_csv(p)
    except Exception: return None

# Load artifacts
summary = load_csv(DATA_DIR/"part6_equal_vs_optimized_summary.csv") or load_csv(DATA_DIR/"part5_equal_vs_optimized_summary.csv")
mroi    = load_csv(DATA_DIR/"marginal_roi_summary.csv")
alloc_c = load_csv(DATA_DIR/"optimal_spend_conversions.csv")
alloc_r = load_csv(DATA_DIR/"optimal_spend_reach.csv")

# TL;DR KPIs
st.markdown("### TL;DR: Impact")
if summary is None or len(summary) < 2:
    st.info("Run Part-5 and Part-6 to generate summary CSVs.")
else:
    conv = summary.iloc[0]  # conversions
    rech = summary.iloc[1]  # deduped_reach_fraction
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Conversions (Equal)",     f"{conv['equal_split']:.1f}")
    c2.metric("Conversions (Optimized)", f"{conv['optimized']:.1f}", delta=f"{conv['lift_%']:.1f}%")
    c3.metric("Conversion Lift",         f"{conv['lift_%']:.1f}%")
    c4.metric("Reach (Equal)",           f"{100*rech['equal_split']:.1f}%")
    c5.metric("Reach (Optimized)",       f"{100*rech['optimized']:.1f}%",  delta=f"{rech['lift_%']:.1f}%")
    c6.metric("Reach Lift",              f"{rech['lift_%']:.1f}%")
    st.caption("Note: When optimizing for conversions, reach can decrease — that trade-off is explicit.")

st.divider()

# Why the budget moved
st.markdown("### Why the Budget Moved")
colA, colB = st.columns(2)
with colA:
    st.markdown("**Optimal Spend by Channel (Conversions objective)**")
    if alloc_c is not None and len(alloc_c):
        fig = px.bar(alloc_c.sort_values("optimal_spend_conversions", ascending=False),
                     x="channel", y="optimal_spend_conversions",
                     labels={"optimal_spend_conversions":"USD", "channel":"Channel"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Missing `data/processed/optimal_spend_conversions.csv`")

with colB:
    st.markdown("**Marginal ROI at Optimum (Δ conversions per $1)**")
    if mroi is not None and len(mroi):
        fig = px.bar(mroi.sort_values("marginal_roi_per_dollar", ascending=False),
                     x="channel", y="marginal_roi_per_dollar",
                     labels={"marginal_roi_per_dollar":"Δ Conversions / $1", "channel":"Channel"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Missing `data/processed/marginal_roi_summary.csv`")

st.caption("Budget flows toward channels with higher marginal ROI until curves saturate or constraints bind.")
st.divider()

# Equal vs Optimized (pre-rendered images from Part-6)
st.markdown("### Equal vs Optimized")
c1, c2 = st.columns(2)
img1 = ASSETS_DIR/"p6_equal_vs_opt_conversions.png"
img2 = ASSETS_DIR/"p6_equal_vs_opt_reach.png"
with c1:
    if img1.exists(): st.image(str(img1), caption="Conversions: Equal vs Optimized")
    else: st.info("Missing `assets/p6_equal_vs_opt_conversions.png`")
with c2:
    if img2.exists(): st.image(str(img2), caption="Deduped Reach (% Audience): Equal vs Optimized")
    else: st.info("Missing `assets/p6_equal_vs_opt_reach.png`")

st.divider()

# Downloads
st.markdown("### Downloads")
rpt = REPORTS_DIR/"OnePlan_Executive_Summary.md"
if rpt.exists():
    st.download_button("Download Executive Summary (Markdown)", data=rpt.read_text(encoding="utf-8"),
                       file_name="OnePlan_Executive_Summary.md")
else:
    st.info("Generate `reports/OnePlan_Executive_Summary.md` in Part-6 to enable download.")
if summary is not None:
    st.download_button("Download Equal vs Optimized Summary (CSV)",
                       data=summary.to_csv(index=False), file_name="equal_vs_optimized_summary.csv")

