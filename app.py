# =========================================================
# Olist Brazilian E-commerce Analytics Dashboard
# =========================================================
# Author  : Raghav Bhardwaj
# Stack   : Streamlit · Plotly · Pandas · NumPy
# Dataset : Olist Brazilian E-commerce (Kaggle)
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Olist Analytics · Raghav Bhardwaj",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# GLOBAL CSS
# IMPORTANT: inline style="" attributes cannot use CSS variables
# (var(--x)) — they are parsed before Streamlit injects :root.
# All inline styles below use literal hex values.
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Syne:wght@700;800&display=swap');

/* ── tokens ── */
:root {
    --bg:     #0A0D14;
    --surf:   #111520;
    --surf2:  #161B2C;
    --bdr:    rgba(255,255,255,0.07);
    --green:  #00E5A0;
    --blue:   #4F8EF7;
    --red:    #FF6B6B;
    --amber:  #FFB347;
    --text:   #E8EDF5;
    --muted:  #94A3B8;
    --r:      14px;
}
            
/* ── base ── */            
html, body, .stApp {
    background-color: #0A0D14;
    color: #E8EDF5;
}
            
# header[data-testid="stHeader"] {
#     display: none;
# }
            
header[data-testid="stHeader"] {
    background: transparent;
    height: 0rem;
}
            
/* ─────────────────────────────
   SIDEBAR TOGGLE BUTTON ONLY
───────────────────────────── */

[data-testid="collapsedControl"] {
    position: fixed !important;

    top: 14px !important;
    left: 14px !important;

    width: 44px !important;
    height: 44px !important;

    border-radius: 12px !important;

    background: rgba(17,21,32,0.96) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    z-index: 999999 !important;

    opacity: 1 !important;
    visibility: visible !important;

    box-shadow: 0 0 16px rgba(0,229,160,0.18) !important;

    transition: all 0.2s ease !important;
}

/* ICON */
[data-testid="collapsedControl"] svg {
    width: 19px !important;
    height: 19px !important;

    stroke: #E8EDF5 !important;
    fill: #E8EDF5 !important;

    opacity: 1 !important;
}

/* HOVER */
[data-testid="collapsedControl"]:hover {
    border-color: rgba(0,229,160,0.45) !important;

    box-shadow:
        0 0 18px rgba(0,229,160,0.28),
        0 0 4px rgba(0,229,160,0.20) inset !important;

    transform: translateY(-1px);
}

/* FORCE SIDEBAR CHEVRON VISIBILITY */
[data-testid="collapsedControl"] * {
    color: #E8EDF5 !important;
    fill: #E8EDF5 !important;
    stroke: #E8EDF5 !important;
    opacity: 1 !important;
}

/* TARGET THE DOUBLE ARROW DIRECTLY */
[data-testid="collapsedControl"] span {
    color: #E8EDF5 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    line-height: 1 !important;
}

/* MAKE BUTTON BACKGROUND ACTUALLY VISIBLE */
[data-testid="collapsedControl"] {
    background-color: rgba(17,21,32,0.96) !important;
    backdrop-filter: blur(10px) !important;
}
            
.main { background-color: #0A0D14; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 1380px; }
# .block-container {
#     padding: 1.2rem 2rem 3rem;
#     max-width: 95%;
# }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #111520 !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] * { color: #E8EDF5 !important; }
# [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
#     background: #00E5A0 !important;
#     color: #000 !important;
#     border-radius: 6px;
# }
            
[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div {
    background-color: #161B2C !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #E8EDF5 !important;
}

[data-testid="stSidebar"] .stMultiSelect span {
    color: #E8EDF5 !important;
}

/* ── hero banner ── */
.hero {
    display: flex; align-items: flex-start; gap: 1.2rem;
    padding: 1.8rem 2rem;
    background: linear-gradient(135deg,#0d1a2d 0%,#0A0D14 55%,#0d1a2d 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero::before {
    content:''; position:absolute; top:-50px; right:-50px;
    width:200px; height:200px;
    background:radial-gradient(circle,rgba(0,229,160,0.10) 0%,transparent 70%);
    border-radius:50%; pointer-events:none;
}
.hero-logo {
    width:50px; height:50px; flex-shrink:0;
    background:#00E5A0; border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    font-size:26px; box-shadow:0 0 20px rgba(0,229,160,0.28);
}
.hero-text h1 {
    font-family:'Syne',sans-serif;
    font-size:clamp(1.4rem,2.5vw,2rem); font-weight:800;
    color:#E8EDF5; margin:0 0 3px; letter-spacing:-0.4px;
}
.hero-text h1 em { font-style:normal; color:#00E5A0; }
.hero-text p  { color:#94A3B8; font-size:0.88rem; margin:0; line-height:1.5; }
.hero-badges  { display:flex; gap:7px; flex-wrap:wrap; margin-top:9px; }
.badge {
    border-radius:20px; padding:2px 11px; font-size:0.73rem;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.07); color:#94A3B8;
}
.badge-g { border-color:rgba(0,229,160,0.30)!important; color:#00E5A0!important; }
.badge-b { border-color:rgba(79,142,247,0.30)!important; color:#4F8EF7!important; }

/* ── section heading ── */
.sec-head { display:flex; align-items:center; gap:10px; margin:2rem 0 0.9rem; }
.sec-pill  {
    width:4px; height:26px; flex-shrink:0; border-radius:4px;
    background:linear-gradient(180deg,#00E5A0,#4F8EF7);
}
.sec-head h3 {
    font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700;
    color:#E8EDF5; margin:0; letter-spacing:-0.2px;
}
.sec-head small { color:#94A3B8; font-size:0.79rem; margin-left:5px; }
# .sec-head small {
#     color:#94A3B8;
# }

/* ── KPI grid ── */
.kpi-grid {
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(155px,1fr));
    gap:12px; margin-bottom:1.8rem;
}
.kpi-card {
    background:#111520; border:1px solid rgba(255,255,255,0.07);
    border-radius:14px; padding:1.1rem 1.3rem;
    position:relative; overflow:hidden;
}
.kpi-card::after {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,#00E5A0,transparent);
}
.kpi-icon { font-size:1.25rem; margin-bottom:7px; display:block; }
.kpi-val  {
    font-family:'Syne',sans-serif; font-size:1.45rem; font-weight:800;
    color:#E8EDF5; line-height:1; margin-bottom:4px;
}
# .kpi-val  {
#     font-family:'DM Sans', sans-serif; font-size:1.45rem; font-weight:800;
#     color:#E8EDF5; line-height:1; margin-bottom:4px;
# }
.kpi-lbl  { font-size:0.72rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.8px; }
.kpi-tag  {
    position:absolute; top:12px; right:12px;
    font-size:0.70rem; font-weight:600; padding:2px 7px; border-radius:20px;
}
.tag-g { background:rgba(0,229,160,0.12); color:#00E5A0; }
.tag-m { background:rgba(255,255,255,0.05); color:#94A3B8; }

/* ── insight box ── */
.insight-box {
    background:#161B2C; border:1px solid rgba(255,255,255,0.07);
    border-left:3px solid #00E5A0; border-radius:14px;
    padding:0.95rem 1.2rem; margin:0.6rem 0 1.4rem;
    font-size:0.86rem; color:#9BAFC7; line-height:1.65;
}
.insight-box b { color:#00E5A0; }

/* ── recommendation cards ── */
.rec-card {
    background:#111520; border:1px solid rgba(255,255,255,0.07);
    border-top:3px solid #00E5A0; border-radius:14px;
    padding:1rem; height:100%;
}
.rec-icon  { font-size:1.5rem; margin-bottom:7px; }
.rec-title {
    font-family:'Syne',sans-serif; font-size:0.88rem; font-weight:700;
    color:#E8EDF5; margin-bottom:5px;
}
.rec-body  { font-size:0.78rem; color:#94A3B8; line-height:1.6; }

/* ── footer ── */
.dash-footer {
    text-align:center; color:#94A3B8; font-size:0.76rem;
    margin-top:3rem; padding-top:1.2rem;
    border-top:1px solid rgba(255,255,255,0.07); line-height:1.85;
}
.dash-footer a { color:#00E5A0; text-decoration:none; }

/* ── tab bar ── */
[data-testid="stTabs"] [role="tablist"] {
    background:#111520; border:1px solid rgba(255,255,255,0.07);
    border-radius:10px; padding:4px; gap:3px; margin-bottom:1.2rem;
}
[data-testid="stTabs"] button[role="tab"] {
    color:#94A3B8 !important; font-family:'DM Sans',sans-serif;
    font-size:0.84rem; font-weight:500; border-radius:7px; padding:5px 15px;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    background:rgba(0,229,160,0.10) !important; color:#E8EDF5 !important;
}

[data-testid="stDataFrame"] {
    background-color: #111520 !important;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    overflow: hidden;
}

/* ─────────────────────────────
   PLOTLY FULLSCREEN DARK MODE
───────────────────────────── */

/* Plotly modebar */
.js-plotly-plot .plotly .modebar {
    background: rgba(17,21,32,0.88) !important;
}

/* Expanded fullscreen background */
.fullscreen {
    background-color: #0A0D14 !important;
}

/* Plotly fullscreen popup container */
div[role="dialog"] {
    background-color: #0A0D14 !important;
}

/* Plot area */
# .js-plotly-plot,
# .plot-container,
# .svg-container,
# # .main-svg {
# #     background: #0A0D14 !important;
# # }

.js-plotly-plot,
.plot-container,
.svg-container {
    background: transparent !important;
}

/* Modebar icons */
.modebar-btn svg {
    fill: #E8EDF5 !important;
}

/* Plotly notifications */
.plotly-notifier {
    color: #E8EDF5 !important;
}
            
/* hide default Streamlit metric widgets (we use custom HTML) */
[data-testid="metric-container"] { display:none; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# PLOTLY HELPERS
# ─────────────────────────────────────────────────────────
# base_layout() builds a fresh dict every call — no shared mutable
# dict means no "multiple values for keyword argument" conflicts.
# Axis config is always passed inline, never pre-stored.

C_GREEN = "#00E5A0"
C_BLUE  = "#4F8EF7"
C_RED   = "#FF6B6B"
C_AMBER = "#FFB347"
# C_MUTED = "#6B7A99"
C_MUTED = "#94A3B8"

# _GRID = dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False, tickfont=dict(size=11))
# _GRID = dict(
#     gridcolor="rgba(255,255,255,0.06)",
#     zeroline=False,
#     tickfont=dict(
#         size=11,
#         color="#B8C5D6"
#     ),
#     title=dict(
#         color="#E2E8F0"
#     )
# )

_GRID = dict(
    gridcolor="rgba(255,255,255,0.06)",
    zeroline=False,
    tickfont=dict(
        size=11,
        color="#B8C5D6"
    ),
    title=dict(
        font=dict(
            color="#E2E8F0"
        )
    )
)

# _GRID = dict(
#     gridcolor="rgba(255,255,255,0.06)",
#     zeroline=False,
#     tickfont=dict(
#         size=11,
#         color="#B8C5D6"
#     )
# )


def _ax(**kw):
    """Return a grid-styled axis dict with optional overrides."""
    d = dict(_GRID)
    d.update(kw)
    return d


def base_layout(**kw):
    """
    Return a complete plotly layout dict.
    Caller passes xaxis / yaxis as keyword args directly here.
    This avoids the double-key error that occurs when spreading
    a pre-built dict that already contains those keys.
    """
    # layout = dict(
    #     paper_bgcolor="rgba(0,0,0,0)",
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     # font=dict(family="DM Sans, sans-serif", color="#9BAFC7", size=12),
    #     font=dict(family="DM Sans, sans-serif", color="#C7D2E3", size=12),
    #     # title_font=dict(family="Syne, sans-serif", color="#E8EDF5", size=14),
    #     title_font=dict(family="Syne, sans-serif", color="#F8FAFC", size=15),
    #     margin=dict(t=44, b=20, l=6, r=6),
    #     legend=dict(
    #         bgcolor="rgba(255,255,255,0.04)",
    #         bordercolor="rgba(255,255,255,0.07)",
    #         borderwidth=1, font_size=11,
    #     ),
    #     hovermode="closest",
    # )

    layout = dict(
        # paper_bgcolor="rgba(0,0,0,0)",
        # plot_bgcolor="rgba(0,0,0,0)",

        paper_bgcolor="#0A0D14",
        plot_bgcolor="#0A0D14",

        font=dict(
            family="DM Sans, sans-serif",
            color="#E2E8F0",
            size=12
        ),

        title_font=dict(
            family="Syne, sans-serif",
            color="#F8FAFC",
            size=16
        ),

        legend=dict(
            bgcolor="rgba(17,21,32,0.88)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,

            font=dict(
                family="DM Sans, sans-serif",
                color="#E2E8F0",
                size=11
            )
        ),

        hoverlabel=dict(
            bgcolor="#111520",
            font_size=12,
            font_family="DM Sans"
        ),

        margin=dict(t=50, b=20, l=6, r=6),
        hovermode="closest",
    )

    layout.update(kw)   # caller's axis / height / title / etc.
    return layout

def force_chart_theme(fig):
    """
    Force all chart text elements to use visible colors
    for dark dashboard rendering.
    """

    fig.update_layout(

        font=dict(
            family="DM Sans, sans-serif",
            color="#E2E8F0",
            size=12
        ),

        title_font=dict(
            family="Syne, sans-serif",
            color="#F8FAFC",
            size=16
        ),

        legend=dict(
            font=dict(
                color="#E2E8F0",
                size=11
            ),
            bgcolor="rgba(17,21,32,0.88)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1
        )
    )

    fig.update_xaxes(
        title_font=dict(color="#E2E8F0", size=13),
        tickfont=dict(color="#B8C5D6", size=11)
    )

    fig.update_yaxes(
        title_font=dict(color="#E2E8F0", size=13),
        tickfont=dict(color="#B8C5D6", size=11)
    )

    return fig

# ─────────────────────────────────────────────────────────
# DATA LOADING  — exactly the same 5 CSVs as the original
# ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    import os

    search = [
        os.environ.get("OLIST_DATA_DIR", ""),
        os.path.dirname(os.path.abspath(__file__)),
        "data", ".",
    ]

    def find(name):
        for d in search:
            p = os.path.join(d, name)
            if os.path.isfile(p):
                return p
        raise FileNotFoundError(
            f"'{name}' not found. Place all Olist CSVs beside app.py "
            "or set the OLIST_DATA_DIR environment variable."
        )

    orders      = pd.read_csv(find("olist_orders_dataset.csv"))
    order_items = pd.read_csv(find("olist_order_items_dataset.csv"))
    products    = pd.read_csv(find("olist_products_dataset.csv"))
    customers   = pd.read_csv(find("olist_customers_dataset.csv"))
    translation = pd.read_csv(find("product_category_name_translation.csv"))

    # ── mirror original wrangling logic ──────────────────
    orders = orders.loc[
        orders["order_status"] == "delivered",
        ["order_id", "customer_id", "order_purchase_timestamp"]
    ].copy()

    order_items = order_items[["order_id", "product_id", "price", "freight_value"]]

    products = (
        products[["product_id", "product_category_name"]]
        .merge(translation, on="product_category_name", how="inner")
        .rename(columns={"product_category_name_english": "product_category"})
        [["product_id", "product_category"]]
    )

    df = (
        orders
        .merge(order_items, on="order_id", how="inner")
        .merge(products,    on="product_id", how="inner")
        .merge(
            customers[["customer_id", "customer_city", "customer_state"]],
            on="customer_id", how="inner",
        )
    )

    # ── feature engineering ──────────────────────────────
    df["total_value"] = df["price"] + df["freight_value"]
    df["freight_pct"] = (
        df["freight_value"] / df["total_value"].replace(0, np.nan)
    ) * 100

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce"
    )
    df["order_year"]  = df["order_purchase_timestamp"].dt.year
    df["order_month"] = (
        df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    )
    df["order_dow"]   = df["order_purchase_timestamp"].dt.day_name()
    df["order_hour"]  = df["order_purchase_timestamp"].dt.hour

    return df


# ─────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────
try:
    df_raw  = load_data()
    DATA_OK = True
except FileNotFoundError as err:
    DATA_OK  = False
    LOAD_ERR = str(err)

# ─────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-logo">🛒</div>
  <div class="hero-text">
    <h1>Olist <em>E-commerce</em> Analytics</h1>
    <p>Business intelligence dashboard &nbsp;·&nbsp; Brazilian marketplace &nbsp;·&nbsp; 2016 – 2018</p>
    <div class="hero-badges">
      <span class="badge badge-g">100k+ Orders</span>
      <span class="badge badge-b">73 Categories</span>
      <span class="badge">Streamlit · Plotly</span>
      <span class="badge">Raghav Bhardwaj</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if not DATA_OK:
    st.error(f"**Data files not found.** {LOAD_ERR}")
    st.info(
        "Place all five Olist CSV files beside `app.py`:\n\n"
        "- `olist_orders_dataset.csv`\n"
        "- `olist_order_items_dataset.csv`\n"
        "- `olist_products_dataset.csv`\n"
        "- `olist_customers_dataset.csv`\n"
        "- `product_category_name_translation.csv`\n\n"
        "Or set the `OLIST_DATA_DIR` environment variable to their folder."
    )
    st.stop()

# ─────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0.8rem 0 0.4rem">
      <p style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;
                color:#E8EDF5;margin:0">Dashboard Filters</p>
      <p style="color:#94A3B8;font-size:0.76rem;margin:2px 0 0">Refine the analysis below</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    all_years = sorted(df_raw["order_year"].dropna().unique().astype(int))
    sel_years = st.multiselect(
        "📅 Order Year", all_years, default=all_years,
    )

    all_cats = sorted(df_raw["product_category"].dropna().unique())
    sel_cats = st.multiselect(
        "🗂 Product Categories", all_cats,
        default=all_cats[:10],
        help="Categories shown across all charts",
    )

    p_min = float(df_raw["price"].min())
    p_max = float(df_raw["price"].quantile(0.99))
    price_range = st.slider(
        "💲 Price Range (R$)",
        min_value=p_min, max_value=p_max,
        value=(p_min, p_max), step=10.0,
        format="R$%.0f",
    )

    st.divider()
    st.markdown("""
    <div style="font-size:0.74rem;color:#94A3B8;line-height:1.65">
      <b style="color:#9BAFC7">Dataset</b><br>
      Olist Brazilian E-commerce · Kaggle<br><br>
      <b style="color:#9BAFC7">Author</b><br>
      Raghav Bhardwaj · Data Science · ML · AI
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_years:
    df = df[df["order_year"].isin(sel_years)]
if sel_cats:
    df = df[df["product_category"].isin(sel_cats)]
df = df[(df["price"] >= price_range[0]) & (df["price"] <= price_range[1])]

# ─────────────────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────────────────
def sec(icon, title, sub=""):
    sub_html = f"<small>{sub}</small>" if sub else ""
    st.markdown(
        f'<div class="sec-head"><div class="sec-pill"></div>'
        f'<h3>{icon} {title}{sub_html}</h3></div>',
        unsafe_allow_html=True,
    )


def insight(html):
    st.markdown(f'<div class="insight-box">{html}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# KPI SECTION
# ─────────────────────────────────────────────────────────
sec("📌", "Executive Overview")

total_rev    = df["total_value"].sum()
total_orders = df["order_id"].nunique()
avg_order    = df.groupby("order_id")["total_value"].sum().mean()
total_custs  = df["customer_id"].nunique()
avg_freight  = df["freight_pct"].mean()
top_cat      = df.groupby("product_category")["total_value"].sum().idxmax()
top_city     = df.groupby("customer_city")["total_value"].sum().idxmax()
n_cats       = df["product_category"].nunique()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <span class="kpi-icon">💰</span>
    <div class="kpi-val">R${total_rev/1e6:.2f}M</div>
    <div class="kpi-lbl">Total Revenue</div>
    <span class="kpi-tag tag-g">GMV</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">📦</span>
    <div class="kpi-val">{total_orders:,}</div>
    <div class="kpi-lbl">Delivered Orders</div>
    <span class="kpi-tag tag-m">unique</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🛒</span>
    <div class="kpi-val">R${avg_order:.0f}</div>
    <div class="kpi-lbl">Avg Order Value</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">👥</span>
    <div class="kpi-val">{total_custs:,}</div>
    <div class="kpi-lbl">Unique Customers</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🚚</span>
    <div class="kpi-val">{avg_freight:.1f}%</div>
    <div class="kpi-lbl">Avg Freight Share</div>
    <span class="kpi-tag tag-m">of order</span>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🏆</span>
    <div class="kpi-val" style="font-size:0.92rem">{top_cat.replace('_',' ').title()}</div>
    <div class="kpi-lbl">Top Category</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🌆</span>
    <div class="kpi-val" style="font-size:0.92rem">{top_city.title()}</div>
    <div class="kpi-lbl">Top City</div>
  </div>
  <div class="kpi-card">
    <span class="kpi-icon">🗂</span>
    <div class="kpi-val">{n_cats}</div>
    <div class="kpi-lbl">Active Categories</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Revenue Trends",
    "🛍 Category Analysis",
    "💵 Pricing & Freight",
    "🌍 Geographic Insights",
])

# ════════════════════════════════════════════════════════
# TAB 1 — REVENUE TRENDS
# ════════════════════════════════════════════════════════
with tab1:

    # ── Monthly revenue line ──────────────────────────────
    monthly = (
        df.groupby("order_month")
        .agg(revenue=("total_value","sum"), orders=("order_id","nunique"))
        .reset_index()
    )
    monthly["rev_M"]    = monthly["revenue"] / 1e6
    monthly["rolling3"] = monthly["rev_M"].rolling(3, min_periods=1).mean()

    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(
        x=monthly["order_month"], y=monthly["rev_M"],
        name="Monthly Revenue",
        line=dict(color=C_BLUE, width=2),
        fill="tozeroy", fillcolor="rgba(79,142,247,0.07)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: R$%{y:.2f}M<extra></extra>",
    ))
    fig_rev.add_trace(go.Scatter(
        x=monthly["order_month"], y=monthly["rolling3"],
        name="3-Month Rolling Avg",
        line=dict(color=C_GREEN, width=2.5, dash="dot"),
        hovertemplate="<b>%{x|%b %Y}</b><br>3M Avg: R$%{y:.2f}M<extra></extra>",
    ))
    fig_rev.update_layout(base_layout(
        title="Monthly Revenue with 3-Month Rolling Average",
        height=360, hovermode="x unified",
        xaxis=_ax(title="Month"),
        yaxis=_ax(title="Revenue (R$ Million)"),
    ))
    force_chart_theme(fig_rev)

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.plotly_chart(fig_rev, use_container_width=True)
    with col_b:
        annual = (
            df.groupby("order_year")
            .agg(Revenue=("total_value","sum"), Orders=("order_id","nunique"))
            .reset_index()
        )
        annual["Revenue"] = annual["Revenue"].apply(lambda x: f"R${x/1e6:.2f}M")
        annual.columns    = ["Year", "Revenue", "Orders"]
        sec("📊", "Annual", "breakdown")
        # st.dataframe(annual, use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div style="
            background:#111520;
            border:1px solid rgba(255,255,255,0.08);
            border-radius:14px;
            padding:0.8rem;
            margin-top:0.4rem;
        ">

        <table style="
            width:100%;
            border-collapse:collapse;
            color:#E8EDF5;
            font-size:0.88rem;
        ">

        <thead>
        <tr style="
            background:#161B2C;
            color:#F8FAFC;
        ">
            <th style="padding:10px;text-align:left;">Year</th>
            <th style="padding:10px;text-align:left;">Revenue</th>
            <th style="padding:10px;text-align:left;">Orders</th>
        </tr>
        </thead>

        <tbody>

        <tr>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">2016</td>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">{annual.iloc[0]['Revenue']}</td>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">{annual.iloc[0]['Orders']}</td>
        </tr>

        <tr>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">2017</td>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">{annual.iloc[1]['Revenue']}</td>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">{annual.iloc[1]['Orders']}</td>
        </tr>

        <tr>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">2018</td>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">{annual.iloc[2]['Revenue']}</td>
        <td style="padding:10px;border-top:1px solid rgba(255,255,255,0.06);">{annual.iloc[2]['Orders']}</td>
        </tr>

        </tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)

    insight(
        "<b>📌 Insight:</b> Revenue grew sharply from 2016 → 2018, with the 3-month rolling "
        "average confirming a sustained upward trajectory — not a seasonal spike. Peak activity "
        "in late 2017 aligns with Black Friday promotional periods, a strong signal for future "
        "campaign timing."
    )

    # ── Day × Hour heatmap ────────────────────────────────
    sec("🕐", "Purchase Timing", "when do customers buy?")

    DOW = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    timing = df.groupby(["order_dow","order_hour"]).size().reset_index(name="count")
    timing["order_dow"] = pd.Categorical(timing["order_dow"], categories=DOW, ordered=True)
    pivot = (
        timing.pivot(index="order_dow", columns="order_hour", values="count")
        .reindex(DOW).fillna(0)
    )

    fig_timing = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=[f"{h:02d}:00" for h in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0,"rgba(0,0,0,0)"],[0.01,"#0d1f3c"],[0.5,"#1E56A0"],[1,C_GREEN]],
        hovertemplate="<b>%{y} — %{x}</b><br>Orders: %{z:,}<extra></extra>",
        showscale=True,
    ))
    fig_timing.update_layout(base_layout(
        title="Order Volume — Day of Week × Hour of Day",
        height=270,
        xaxis=_ax(nticks=24),
        yaxis=_ax(),
    ))
    force_chart_theme(fig_timing)
    st.plotly_chart(fig_timing, use_container_width=True)

    insight(
        "<b>📌 Insight:</b> Most orders are placed on weekday afternoons (14:00–20:00), "
        "suggesting customers browse during lunch or post-work hours. Weekend mornings are "
        "notably quieter — a potential window for targeted push campaigns."
    )


# ════════════════════════════════════════════════════════
# TAB 2 — CATEGORY ANALYSIS
# ════════════════════════════════════════════════════════
with tab2:

    cat_df = (
        df.groupby("product_category")
        .agg(
            revenue    =("total_value","sum"),
            orders     =("order_id","nunique"),
            avg_price  =("price","mean"),
            avg_freight=("freight_pct","mean"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    top10 = cat_df.head(10)

    # ── Top 10 bar ────────────────────────────────────────
    sec("💰", "Top 10 Categories", "by total revenue")

    fig_cat = go.Figure(go.Bar(
        x=top10["product_category"].str.replace("_"," ").str.title(),
        y=top10["revenue"] / 1e6,
        marker=dict(
            color=top10["revenue"],
            colorscale=[[0,"#1B357C"],[0.5,C_BLUE],[1,C_GREEN]],
            showscale=False,
        ),
        hovertemplate="<b>%{x}</b><br>Revenue: R$%{y:.2f}M<extra></extra>",
    ))
    fig_cat.update_layout(base_layout(
        title="Top Product Categories by Revenue",
        height=340,
        xaxis=_ax(tickangle=-25, title="Category"),
        yaxis=_ax(title="Revenue (R$ Million)"),
    ))
    force_chart_theme(fig_cat)
    st.plotly_chart(fig_cat, use_container_width=True)

    insight(
        "<b>📌 Insight:</b> A small number of categories contribute disproportionately to total "
        "revenue — a classic Pareto pattern. <i>Health & Beauty</i> and <i>Watches & Gifts</i> lead; "
        "both are high-ticket repeat-purchase categories, ideal for loyalty programme investment."
    )

    # ── Price heatmap ─────────────────────────────────────
    sec("🌡", "Category vs Average Price", "highest-priced segments")

    top10_price = cat_df.sort_values("avg_price", ascending=False).head(10)

    fig_heat = go.Figure(data=go.Heatmap(
        z=top10_price[["avg_price"]].values,
        x=["Average Price (R$)"],
        y=top10_price["product_category"].str.replace("_"," ").str.title(),
        colorscale=[[0,"#0d1a2d"],[0.4,"#1E56A0"],[0.7,C_GREEN],[1,C_AMBER]],
        text=[[f"R${v:.0f}"] for v in top10_price["avg_price"].values],
        texttemplate="%{text}",
        hovertemplate="<b>%{y}</b><br>Avg Price: R$%{z:.2f}<extra></extra>",
        showscale=True,
    ))
    fig_heat.update_layout(base_layout(
        title="Highest Priced Product Categories",
        height=320,
        xaxis=_ax(),
        yaxis=_ax(autorange="reversed"),
    ))
    force_chart_theme(fig_heat)
    st.plotly_chart(fig_heat, use_container_width=True)

    insight(
        "<b>📌 Insight:</b> Computers and home appliances command the highest average prices "
        "(R$1 000+), representing premium segments where targeted upsell and extended warranty "
        "programs could meaningfully increase margin per transaction."
    )


# ════════════════════════════════════════════════════════
# TAB 3 — PRICING & FREIGHT
# ════════════════════════════════════════════════════════
with tab3:

    col1, col2 = st.columns(2)

    with col1:
        sec("📊", "Order Price Distribution")
        fig_hist = go.Figure(go.Histogram(
            x=df["price"].clip(0, df["price"].quantile(0.97)),
            nbinsx=30,
            marker_color=C_BLUE, opacity=0.85,
            hovertemplate="Price: R$%{x:.0f}<br>Orders: %{y:,}<extra></extra>",
        ))
        fig_hist.update_layout(base_layout(
            title="Order Price Distribution",
            height=300,
            xaxis=_ax(title="Price (R$)"),
            yaxis=_ax(title="Order Count"),
        ))
        force_chart_theme(fig_hist)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        sec("📦", "Order Value Components")
        fig_box = go.Figure()
        for col_name, color, label in [
            ("price",         C_BLUE,  "Product Price"),
            ("freight_value", C_RED,   "Freight Value"),
            ("total_value",   C_GREEN, "Total Order Value"),
        ]:
            fig_box.add_trace(go.Box(
                y=df[col_name].clip(0, df[col_name].quantile(0.95)),
                name=label,
                marker_color=color, line_color=color,
                boxmean="sd",
                hovertemplate=f"<b>{label}</b><br>%{{y:.2f}}<extra></extra>",
            ))
        fig_box.update_layout(base_layout(
            title="Distribution of Order Metrics",
            height=300,
            xaxis=_ax(),
            yaxis=_ax(title="Value (R$)"),
            boxmode="group",
        ))
        force_chart_theme(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)

    insight(
        "<b>📌 Insight:</b> Most purchases cluster below R$200, confirming price-sensitive "
        "buying behaviour. Several high-value outliers indicate occasional premium purchases. "
        "Freight shows high variance — heavy-item categories carry disproportionate costs "
        "that erode net margin."
    )

    # ── Scatter: price vs total_value ─────────────────────
    sec("📉", "Price vs Total Order Value", "correlation analysis")

    corr   = df["price"].corr(df["total_value"])
    sample = df.sample(min(5000, len(df)), random_state=42)

    fig_scatter = px.scatter(
        sample, x="price", y="total_value",
        opacity=0.55,
        trendline="ols",
        trendline_color_override=C_GREEN,
        color_discrete_sequence=[C_BLUE],
        labels={"price":"Price (R$)", "total_value":"Total Order Value (R$)"},
        template="plotly_dark",
    )
    fig_scatter.update_traces(marker=dict(size=4, color=C_BLUE))
    fig_scatter.update_layout(base_layout(
        title=f"Price vs Total Order Value  —  Pearson r = {corr:.3f}",
        height=360,
        xaxis=_ax(title="Price (R$)"),
        yaxis=_ax(title="Total Order Value (R$)"),
        showlegend=False,
    ))

    fig_scatter.update_traces(
        marker=dict(size=4, color=C_BLUE)
    )

    fig_scatter.update_layout(
        legend_font_color="#E2E8F0",
        title_font_color="#F8FAFC",
    )
    force_chart_theme(fig_scatter)

    st.plotly_chart(fig_scatter, use_container_width=True)

    # st.metric("📊 Correlation Coefficient", f"{corr:.3f}")
    # Define the HTML component to change widget colors
    # def change_metric_color(widget_text, color_code):
    #     html_script = f"""
    #     <script>
    #         var elements = window.parent.document.querySelectorAll('*');
    #         for (var i = 0; i < elements.length; i++) {{
    #             if (elements[i].innerText.includes("{widget_text}")) {{
    #                 elements[i].style.color = "{color_code}";
    #             }}
    #         }}
    #     </script>
    #     """
    #     components.html(html_script, height=0, width=0)

    # # Display the metric (standard)
    # st.metric(label="📊 Correlation Coefficient", value=f"{corr:.3f}")

    # # Apply custom hex color to the metric label
    # change_metric_color("Correlation Coefficient", "#FF5733")

    # st.markdown(f"""
    # <div style="
    #     background:#111520;
    #     border:1px solid rgba(255,255,255,0.08);
    #     border-left:4px solid #00E5A0;
    #     border-radius:14px;
    #     padding:1rem 1.2rem;
    #     margin-top:0.5rem;
    #     min-width:260px;
    #     display:inline-block;
    # ">

    #     <div style="
    #         color:#94A3B8;
    #         font-size:0.82rem;
    #         font-weight:500;
    #         margin-bottom:0.3rem;
    #         letter-spacing:0.3px;
    #     ">
    #         📊 Correlation Coefficient
    #     </div>

    #     <div style="
    #         color:#F8FAFC;
    #         font-family:'Syne', sans-serif;
    #         font-size:2rem;
    #         font-weight:800;
    #         line-height:1;
    #     ">
    #         {corr:.3f}
    #     </div>

    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        background: #111520;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid #00E5A0;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-top: 0.5rem;
        width: 100%;
        max-width: 300px;
        box-sizing: border-box;
    ">
        <div style="
            color: #94A3B8;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 0.4rem;
            letter-spacing: 0.3px;
        ">
            📊 Correlation Coefficient
        </div>
        <div style="
            color: #F8FAFC;
            font-family: 'Syne', system-ui, -apple-system, sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
        ">
            {corr:.3f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    insight(
        f"<b>📌 Insight:</b> Pearson r&nbsp;=&nbsp;<b>{corr:.3f}</b> confirms a very strong "
        "linear relationship between product price and total order value. Higher-priced items "
        "are the primary lever for revenue optimisation — freight adds overhead but does not "
        "distort this relationship."
    )


# ════════════════════════════════════════════════════════
# TAB 4 — GEOGRAPHIC INSIGHTS
# ════════════════════════════════════════════════════════
with tab4:

    col1, col2 = st.columns(2)

    with col1:
        sec("🏙", "Top Cities", "by total revenue")
        city_rev = (
            df.groupby("customer_city")["total_value"]
            .sum().sort_values(ascending=False)
            .head(10).reset_index()
        )
        city_rev["label"] = city_rev["customer_city"].str.title()

        fig_city = go.Figure(go.Bar(
            x=city_rev["total_value"] / 1e3,
            y=city_rev["label"],
            orientation="h",
            marker=dict(
                color=city_rev["total_value"],
                colorscale=[[0,"#1B357C"],[1,C_GREEN]],
                showscale=False,
            ),
            hovertemplate="<b>%{y}</b><br>Revenue: R$%{x:.1f}K<extra></extra>",
        ))
        fig_city.update_layout(base_layout(
            title="Top Revenue-Contributing Cities",
            height=380,
            xaxis=_ax(title="Revenue (R$ Thousand)"),
            yaxis=_ax(autorange="reversed"),
        ))
        force_chart_theme(fig_city)
        st.plotly_chart(fig_city, use_container_width=True)

    with col2:
        sec("🗺", "Top States", "revenue & order volume")
        state_df = (
            df.groupby("customer_state")
            .agg(revenue=("total_value","sum"), orders=("order_id","nunique"))
            .reset_index()
            .sort_values("revenue", ascending=False)
            .head(12)
        )

        # make_subplots figures need manual layout — do NOT use base_layout()
        # as a spread dict here; build it attribute by attribute to avoid conflicts.
        fig_state = make_subplots(specs=[[{"secondary_y": True}]])
        fig_state.add_trace(
            go.Bar(
                x=state_df["customer_state"],
                y=state_df["revenue"] / 1e6,
                name="Revenue (R$M)",
                marker_color=C_BLUE, opacity=0.85,
                hovertemplate="<b>%{x}</b><br>Revenue: R$%{y:.2f}M<extra></extra>",
            ),
            secondary_y=False,
        )
        fig_state.add_trace(
            go.Scatter(
                x=state_df["customer_state"],
                y=state_df["orders"],
                name="Orders",
                mode="lines+markers",
                line=dict(color=C_GREEN, width=2),
                marker=dict(size=7),
                hovertemplate="<b>%{x}</b><br>Orders: %{y:,}<extra></extra>",
            ),
            secondary_y=True,
        )
        # set layout properties individually — avoids multi-value conflicts
        fig_state.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            # font=dict(family="DM Sans, sans-serif", color="#9BAFC7", size=12),
            font=dict(family="DM Sans, sans-serif", color="#C7D2E3", size=12),
            title_text="Revenue & Orders by State",
            # title_font=dict(family="Syne, sans-serif", color="#E8EDF5", size=14),
            title_font=dict(family="Syne, sans-serif", color="#F8FAFC", size=15),
            height=380,
            margin=dict(t=44, b=20, l=6, r=6),
            hovermode="x unified",
            legend=dict(
                bgcolor="rgba(255,255,255,0.04)",
                bordercolor="rgba(255,255,255,0.07)",
                borderwidth=1, font_size=11, x=0.62, y=0.98,
            ),
        )

        fig_state.update_layout(
            paper_bgcolor="#0A0D14",
            plot_bgcolor="#0A0D14",
        )

        fig_state.update_xaxes(
            showgrid=False,
            color="#E8EDF5"
        )

        fig_state.update_yaxes(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            color="#E8EDF5"
        )
        
        fig_state.update_yaxes(
            title_text="Revenue (R$ Million)",
            gridcolor="rgba(255,255,255,0.05)", zeroline=False,
            secondary_y=False,
        )
        fig_state.update_yaxes(
            title_text="Orders",
            gridcolor="rgba(255,255,255,0.05)", zeroline=False,
            secondary_y=True,
        )
        fig_state.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
        force_chart_theme(fig_state)
        st.plotly_chart(fig_state, use_container_width=True)

    insight(
        "<b>📌 Insight:</b> Revenue is heavily concentrated in São Paulo — expected given "
        "Brazil's economic centre. States like Minas Gerais and Rio de Janeiro show strong "
        "secondary demand and represent high-potential expansion corridors where logistics "
        "investment could unlock disproportionate growth."
    )

    # ── Avg order value by state ──────────────────────────
    sec("💲", "Avg Order Value by State")
    state_aov = (
        df.groupby("customer_state")
        .agg(aov=("total_value","mean"), orders=("order_id","nunique"))
        .reset_index()
        .sort_values("aov", ascending=False)
        .head(15)
    )
    fig_aov = go.Figure(go.Bar(
        x=state_aov["customer_state"],
        y=state_aov["aov"],
        marker=dict(
            color=state_aov["orders"],
            colorscale=[[0,"#1B357C"],[1,C_GREEN]],
            showscale=True,
            colorbar=dict(title="Orders", thickness=12, len=0.7),
        ),
        hovertemplate="<b>%{x}</b><br>Avg Order: R$%{y:.2f}<extra></extra>",
    ))
    fig_aov.update_layout(base_layout(
        title="Average Order Value by Customer State",
        height=280,
        xaxis=_ax(title="State"),
        yaxis=_ax(title="Avg Order Value (R$)"),
    ))
    force_chart_theme(fig_aov)
    st.plotly_chart(fig_aov, use_container_width=True)

    insight(
        "<b>📌 Insight:</b> Certain lower-volume states exhibit notably higher average order "
        "values, suggesting premium buyer segments outside the main urban centres. Targeted "
        "premium campaigns in these states can improve revenue quality without proportional "
        "logistics overhead."
    )


# ─────────────────────────────────────────────────────────
# STRATEGIC RECOMMENDATIONS
# ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
sec("🚀", "Strategic Recommendations")

recs = [
    ("🎯", "Focus on top categories",
     "Health & Beauty and Watches & Gifts drive outsized revenue. Concentrate marketing "
     "spend here with category-specific creatives."),
    ("📦", "Optimise freight-heavy ops",
     "Freight costs meaningfully impact total order values. Negotiate regional fulfilment "
     "agreements for heavy-item categories to protect margin."),
    ("🌆", "Target high-revenue cities",
     "Revenue concentration in select cities highlights strong regional demand clusters. "
     "Localised promotions and faster delivery SLAs can accelerate growth."),
    ("💎", "Expand premium segments",
     "Computers and appliances carry the highest average prices. Extended warranties and "
     "bundle deals can increase margin per transaction."),
    ("📈", "Monitor premium outliers",
     "High-value order outliers reveal premium customer segments. Identify and nurture "
     "these buyers with VIP programmes and early-access offers."),
]

cols = st.columns(len(recs))
for c, (icon, title, body) in zip(cols, recs):
    with c:
        st.markdown(
            f'<div class="rec-card">'
            f'<div class="rec-icon">{icon}</div>'
            f'<div class="rec-title">{title}</div>'
            f'<div class="rec-body">{body}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div class="dash-footer">
  Built with <b>Streamlit · Plotly · Pandas · NumPy</b><br>
  <b>Raghav Bhardwaj</b> &nbsp;·&nbsp; Data Science · ML · AI &nbsp;·&nbsp;
  <a href="https://github.com/RaghavBhardwaj18"
     target="_blank">GitHub ↗</a> &nbsp;·&nbsp;
  <a href="https://linkedin.com/in/raghav-bhardwaj-" target="_blank">LinkedIn ↗</a><br>
  <span style="opacity:0.45">Olist Brazilian E-commerce Public Dataset · Kaggle</span>
</div>
""", unsafe_allow_html=True)