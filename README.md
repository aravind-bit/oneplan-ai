{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 LucidaGrande;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww33400\viewh21000\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # OnePlan AI \'97 Intelligent Media Budget Optimizer\
*A machine-learning\'96powered simulation of how media companies like NBCUniversal or Warner Bros. Discovery could optimize cross-channel advertising budgets.*\
\
---\
\
##  Overview\
OnePlan AI models how different media channels (TV, Streaming, YouTube, Display, Social) respond to ad spend and uses machine learning + mathematical optimization to recommend the most efficient cross-channel allocation.\
\
It replicates the principles behind NBCUniversal\'92s **One Platform Total Audience** system\'97bringing together data science, optimization, and explainability.\
\
---\
\
## Business Problem\
Media planners struggle to understand **where each marketing dollar delivers the most conversions or reach**.  \
This project answers one key question:\
\
> **\'93Where should the next dollar go to maximize ROI?\'94**\
\
---\
\
## Solution Architecture\
\
| Layer | Description | Notebook |\
|:--|:--|:--|\
| **1. Synthetic Data Generator** | Creates realistic cross-channel campaign data (spend, impressions, conversions). | `01_synthetic_data_generator.ipynb` |\
| **2. EDA & Media Math** | Validates channel behavior, CPM logic, and correlation between spend & performance. | `02_eda_and_media_math.ipynb` |\
| **3. ML Modeling (Linear & XGBoost)** | Fits non-linear response curves with Savitzky\'96Golay smoothing to reduce noise. | `03_model_response_curves.ipynb` |\
| **4. Reach Overlap Simulation** | Models audience duplication across channels for deduped reach metrics. | `04_reach_overlap_simulation.ipynb` |\
| **5. Budget Optimization** | Solves constrained optimization to maximize conversions or deduped reach. | `05_budget_optimizer.ipynb` |\
| **6. Explainability & Summary** | Visualizes allocation shifts, marginal ROI, and produces an executive summary. | `06_explainability_and_summary.ipynb` |\
\
---\
\
## Key Outputs & Visuals\
\
### Response Curves (from Part 3)\
> File: `assets/response_curves_overlay.png`  \
Shows **spend 
\f1 \uc0\u8594 
\f0  predicted conversions** per channel.  \
- Steeper slopes 
\f1 \uc0\u8594 
\f0  more efficient channels (YouTube, Social).  \
- Flattened curves 
\f1 \uc0\u8594 
\f0  saturation (Linear TV).\
\
![Response Curves](assets/response_curves_overlay.png)\
\
---\
\
###  Optimal Spend Allocation (from Part 5)\
> File: `assets/p6_opt_spend_conversions.png`  \
Bar chart of **budget by channel** for the conversions objective.\
\
![Optimal Spend](assets/p6_opt_spend_conversions.png)\
\
---\
\
###  Marginal ROI by Channel (from Part 6)\
> File: `assets/p6_marginal_roi.png`  \
Shows the **extra conversions per $1** at optimized allocation.  \
High marginal ROI 
\f1 \uc0\u8594 
\f0  channel still has growth potential.\
\
![Marginal ROI](assets/p6_marginal_roi.png)\
\
---\
\
### \uc0\u55357 \u56520  Equal vs Optimized Performance\
> Files:  \
> - `assets/p6_equal_vs_opt_conversions.png`  \
> - `assets/p6_equal_vs_opt_reach.png`  \
Side-by-side comparison demonstrating how **OnePlan AI** reallocates budget for performance.\
\
| Metric | Equal Split | Optimized | Lift % |\
|:--|--:|--:|--:|\
| Conversions | 111.9 | 121.4 | **+8.5 %** |\
| Deduped Reach | 61.1 % | 45.8 % | **\uc0\u8722 25.0 %** |\
\
> \uc0\u9878 \u65039  The optimizer increased total conversions by **+8.5 %** by shifting spend toward high-ROI digital channels, \
> even though total deduplicated reach decreased by about **25 %** \'97 a realistic efficiency-vs-reach trade-off.\
\
---\
\
## Reports\
\
-  **Executive Summary:** [`reports/OnePlan_Executive_Summary.md`](reports/OnePlan_Executive_Summary.md)  \
  > A non-technical, management-friendly overview explaining *what changed*, *why the optimizer reallocated spend*, and *how much lift it produced*.\
\
-  **Model Performance:** `data/processed/model_response_summary.csv`  \
  > RMSE/MAE/R\'b2 per channel (Linear Regression vs XGBoost).\
\
---\
\
##  Key Insights\
\
- **Digital channels** (Social & YouTube) deliver higher marginal ROI at lower CPMs.  \
- **Linear TV** saturates quickly \'97 still valuable for reach but inefficient for conversions.  \
- **Optimizer recommends** shifting 15\'9620 % budget from TV to digital, improving total conversions by ~12 %.  \
- **Explainability layer** quantifies *why* these shifts occur, not just *what* the AI predicts.\
\
---\
\
## Tech Stack\
Python 3.11 \'b7 Pandas \'b7 Scikit-learn \'b7 XGBoost \'b7 SciPy \'b7 Matplotlib  \
Deployed via Jupyter Notebooks on macOS (venv)  \
Data versioning through Git\
\
---\
\
## Folder Map\
\
notebooks/       \uc0\u8594  Jupyter analysis parts 1\'966 (+ verify notebook)\
data/raw/        \uc0\u8594  synthetic data + overlap matrix\
data/processed/  \uc0\u8594  response curves, optimizer outputs, metrics\
assets/          \uc0\u8594  plots used in README and reports\
reports/         \uc0\u8594  OnePlan_Executive_Summary.md (+ optional HTML)\
README.md        \uc0\u8594  this file\
LICENSE          \uc0\u8594  (added in next step)\
requirements.txt \uc0\u8594  pinned dependencies (optional)\
\'97\
\
##  License & Attribution\
This project was independently created for educational and portfolio demonstration purposes.\
\
**Inspirations:**\
- NBCUniversal \'97 *One Platform Total Audience* (media planning & reach analytics)\
- Nielsen & Comscore public documentation on audience modeling\
- SciPy, Scikit-learn, and XGBoost open-source projects\
\
\'a9 2025 Aravind Anisetti. All rights reserved.\
}