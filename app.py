# app.py — OnePlan AI: Executive Story App (tabs, no icons, with references)
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# ------------ Paths ------------
DATA_DIR   = Path("data/processed")
ASSETS_DIR = Path("assets")
REPORTS_DIR= Path("reports")

st.set_page_config(page_title="OnePlan AI — Media Budget Optimizer", layout="wide")

# ------------ Helpers ------------
@st.cache_data
def load_csv(p: Path):
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
        return df if len(df) > 0 else None
    except Exception:
        return None

def file_exists(p: Path) -> bool:
    return p.exists() and p.is_file()

# Primary artifacts (with safe fallback for summary)
summary = None
first_path   = DATA_DIR / "part6_equal_vs_optimized_summary.csv"
fallback_path= DATA_DIR / "part5_equal_vs_optimized_summary.csv"
if (df := load_csv(first_path)) is not None:
    summary = df
elif (df := load_csv(fallback_path)) is not None:
    summary = df

mroi    = load_csv(DATA_DIR/"marginal_roi_summary.csv")
alloc_c = load_csv(DATA_DIR/"optimal_spend_conversions.csv")
alloc_r = load_csv(DATA_DIR/"optimal_spend_reach.csv")

img_conv = ASSETS_DIR/"p6_equal_vs_opt_conversions.png"
img_rech = ASSETS_DIR/"p6_equal_vs_opt_reach.png"
img_mroi = ASSETS_DIR/"p6_marginal_roi.png"

# ------------ Page Header ------------
st.title("OnePlan AI — Intelligent Media Budget Optimizer")
st.write(
    "A concise narrative for leadership: what changed, why it changed, and the business impact. "
    "This simulation mirrors how modern media orgs plan cross-platform budgets with AI: "
    "learn response curves, estimate deduplicated reach, and optimize allocation under constraints."
)

# ------------ Tabs ------------
tabs = st.tabs([
    "Overview", "Impact", "Allocation & ROI", "How it works", "References", "Diagnostics"
])

# ========== Overview ==========
with tabs[0]:
    st.subheader("What this delivers")
    st.write(
        "- A single, explainable recommendation for reallocating media budget across TV, Streaming, YouTube, Display, and Social.\n"
        "- Transparent trade-offs: optimize conversions while monitoring deduplicated reach.\n"
        "- Reproducible artifacts (CSVs/plots) suitable for review with finance, marketing, and data leadership."
    )
    st.markdown("#### Executive summary file")
    rpt = REPORTS_DIR/"OnePlan_Executive_Summary.md"
    if file_exists(rpt):
        st.download_button("Download the executive summary (Markdown)", rpt.read_text(encoding="utf-8"),
                           file_name="OnePlan_Executive_Summary.md")
    else:
        st.info("Generate `reports/OnePlan_Executive_Summary.md` in Part-6 to enable this download.")

# ========== Impact ==========
with tabs[1]:
    st.subheader("Overall impact")
    if summary is None or len(summary) < 2:
        st.warning("Processed summary files not found. Run Parts 5–6 and push CSV outputs.")
    else:
        conv = summary.iloc[0]  # conversions
        rech = summary.iloc[1]  # deduped_reach_fraction
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Conversions (equal)", f"{conv['equal_split']:.1f}")
        c2.metric("Conversions (optimized)", f"{conv['optimized']:.1f}")
        c3.metric("Conversion lift", f"{conv['lift_%']:.1f}%")
        c4.metric("Reach lift", f"{rech['lift_%']:.1f}%")
        st.caption("Optimizing for conversions can reduce reach—this makes the efficiency trade-off explicit.")

    st.markdown("#### Equal vs optimized visuals")
    col1, col2 = st.columns(2)
    with col1:
        if file_exists(img_conv):
            st.image(str(img_conv), caption="Conversions: equal vs optimized")
        else:
            st.info("Missing: assets/p6_equal_vs_opt_conversions.png")
    with col2:
        if file_exists(img_rech):
            st.image(str(img_rech), caption="Deduplicated reach: equal vs optimized")
        else:
            st.info("Missing: assets/p6_equal_vs_opt_reach.png")

# ========== Allocation & ROI ==========
with tabs[2]:
    st.subheader("Why the recommendation changed")
    left, right = st.columns(2)

    with left:
        st.markdown("**Optimal spend by channel (conversions objective)**")
        if alloc_c is not None and {"channel","optimal_spend_conversions"}.issubset(alloc_c.columns):
            fig = px.bar(
                alloc_c.sort_values("optimal_spend_conversions", ascending=False),
                x="channel", y="optimal_spend_conversions",
                labels={"channel":"Channel", "optimal_spend_conversions":"USD"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Missing or malformed: data/processed/optimal_spend_conversions.csv")

    with right:
        st.markdown("**Marginal ROI at the optimum (Δ conversions per $1)**")
        if mroi is not None and {"channel","marginal_roi_per_dollar"}.issubset(mroi.columns):
            fig = px.bar(
                mroi.sort_values("marginal_roi_per_dollar", ascending=False),
                x="channel", y="marginal_roi_per_dollar",
                labels={"channel":"Channel", "marginal_roi_per_dollar":"Δ Conversions per $1"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Missing or malformed: data/processed/marginal_roi_summary.csv")

    st.markdown("#### Interpretation")
    st.write(
        "Budget moves toward channels with higher marginal ROI until curves saturate or constraints bind. "
        "This is consistent with how advanced MMM/optimizer systems reallocate spend under fixed budgets."
    )
    if file_exists(img_mroi):
        st.image(str(img_mroi), caption="Marginal ROI by channel (from Part-6)")

# ========== How it works ==========
with tabs[3]:
    st.subheader("Methodology in brief")
    st.markdown(
        "- **Response curves**: Learn non-linear spend→conversions relationships per channel, then smooth to reduce noise.\n"
        "- **Deduplicated reach**: Estimate unique audience across channels using overlap parameters and reach curves.\n"
        "- **Optimization**: Solve a constrained allocation to maximize conversions (or reach) under per-channel bounds.\n"
        "- **Explainability**: Report marginal ROI at the solution and show equal vs optimized deltas."
    )
    st.markdown("#### Files this app reads")
    st.code(
        "data/processed/\n"
        "  ├─ part6_equal_vs_optimized_summary.csv (fallback: part5_...)\n"
        "  ├─ marginal_roi_summary.csv\n"
        "  ├─ optimal_spend_conversions.csv\n"
        "  └─ optimal_spend_reach.csv\n"
        "assets/\n"
        "  ├─ p6_equal_vs_opt_conversions.png\n"
        "  ├─ p6_equal_vs_opt_reach.png\n"
        "  └─ p6_marginal_roi.png\n",
        language="text"
    )

# ========== References ==========
with tabs[4]:
    st.subheader("Industry context & references")
    st.markdown(
        "- NBCUniversal **One Platform Total Audience**: AI-driven planning for unduplicated reach across linear and streaming. "
        "[NBCU article] " +
        "(https://www.nbcuniversal.com/article/nbcuniversal-redefines-cross-platform-advertising-industry-one-platform-total-audience) • "  # Jan 8, 2024
        "[StreamTV Insider coverage]" +
        "(https://www.streamtvinsider.com/advertising/nbcuniversal-launches-advertising-platform-bridges-linear-streaming-audiences)"
    )
    st.markdown(
        "- **Deduplicated reach** background from measurement leaders: "
        "[Nielsen ONE] (https://www.nielsen.com/solutions/audience-measurement/nielsen-one/) • "
        "[Nielsen four-screen dedup for YouTube] (https://www.prnewswire.com/news-releases/nielsen-launches-four-screen-ad-deduplication-its-methodology-which-will-be-used-for-youtube-301591075.html) • "
        "[Comscore cross-platform] (https://www.comscore.com/Products/Digital/Multi-Platform-Content-Measurement)"
    )
    st.markdown(
        "- Open-source **MMM** tools that inspire response-curve and budget-allocation methods: "
        "[Meta Robyn] (https://github.com/facebookexperimental/Robyn) • "
        "[Robyn docs] (https://facebookexperimental.github.io/Robyn/) • "
        "[Google LightweightMMM] (https://github.com/google/lightweight_mmm) / "
        "[docs] (https://lightweight-mmm.readthedocs.io/) "
        "(Google now points to **Meridian** as a successor)."
    )
    st.caption(
        "This demo is educational and synthetic, but the workflow reflects modern cross-media planning systems."
    )

# ========== Diagnostics ==========
with tabs[5]:
    st.subheader("Setup diagnostics")
    st.write({
        "part6_equal_vs_optimized_summary.csv": (DATA_DIR/"part6_equal_vs_optimized_summary.csv").exists(),
        "part5_equal_vs_optimized_summary.csv": (DATA_DIR/"part5_equal_vs_optimized_summary.csv").exists(),
        "marginal_roi_summary.csv": (DATA_DIR/"marginal_roi_summary.csv").exists(),
        "optimal_spend_conversions.csv": (DATA_DIR/"optimal_spend_conversions.csv").exists(),
        "optimal_spend_reach.csv": (DATA_DIR/"optimal_spend_reach.csv").exists(),
        "assets/p6_equal_vs_opt_conversions.png": file_exists(img_conv),
        "assets/p6_equal_vs_opt_reach.png": file_exists(img_rech),
        "assets/p6_marginal_roi.png": file_exists(img_mroi),
    })
    st.caption("If a value is False, re-run Part-5/6 locally, commit the artifacts, and push.")