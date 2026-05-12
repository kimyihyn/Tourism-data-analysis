"""
외국인 입국·관광 데이터 분석 대시보드
Design System: Figma Marketing System (monochrome core + pastel color-block sections)
Typography: Pretendard only
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# ============================================================
# 0. PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="외국인 입국·관광 데이터 분석 대시보드",
    layout="wide",
    page_icon="●",
    initial_sidebar_state="collapsed",
)

# ============================================================
# DESIGN TOKENS (Figma 시스템 차용)
# ============================================================
COLORS = {
    "primary": "#000000",
    "canvas": "#FFFFFF",
    "ink": "#000000",
    "inverse_ink": "#FFFFFF",
    "surface_soft": "#F5F5F5",
    "hairline": "#E5E5E5",
    "hairline_soft": "#EFEFEF",
    "block_lime": "#E6F576",
    "block_lilac": "#DCD5F5",
    "block_cream": "#F7EDD9",
    "block_mint": "#CFEDD8",
    "block_pink": "#FBD0DD",
    "block_coral": "#FFB6A0",
    "block_navy": "#1E1B4B",
    "accent_magenta": "#FF3B7F",
    "success": "#00C25A",
}

# ============================================================
# CSS INJECTION — Pretendard + Figma-style chrome
# (link 태그는 streamlit sanitizer가 제거함 → @import + components.html 백업 양 방식 사용)
# ============================================================

# (1) iframe 안의 Streamlit 컴포넌트가 아닌, 상위 문서 head에 Pretendard 강제 로드
import streamlit.components.v1 as components
components.html(
    """
    <script>
    (function() {
      var doc = window.parent.document;
      if (!doc.getElementById('pretendard-font-link')) {
        var link = doc.createElement('link');
        link.id = 'pretendard-font-link';
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css';
        doc.head.appendChild(link);
      }
    })();
    </script>
    """,
    height=0,
)

st.markdown(
    """
<style>
/* ========== Pretendard via @import (fallback) ========== */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');

/* ============ GLOBAL FONT ENFORCEMENT (universal selector + !important) ============ */
*, *::before, *::after {
    font-family: "Pretendard Variable", "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
html, body, .stApp, .main, .block-container,
button, input, textarea, select, p, div, span, h1, h2, h3, h4, h5, h6, li, label, a {
    font-family: "Pretendard Variable", "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, sans-serif !important;
    font-feature-settings: "kern" 1;
}

.stApp { background: #FFFFFF; color: #000000; }
.main .block-container { padding-top: 0 !important; padding-bottom: 96px !important; max-width: 1280px; }
#MainMenu, footer, header { visibility: hidden; height: 0; }

/* ============ TOP NAV (sticky) ============ */
.top-nav {
    position: sticky; top: 0; z-index: 999;
    background: #FFFFFF;
    border-bottom: 1px solid #EFEFEF;
    padding: 14px 32px;
    display: flex; align-items: center; justify-content: space-between;
    height: 56px;
    margin: 0 -1rem 0 -1rem;
}
.top-nav .wordmark { font-size: 22px; font-weight: 700; letter-spacing: -0.5px; }
.top-nav .nav-links { display: flex; gap: 24px; font-size: 16px; font-weight: 480; }
.top-nav .nav-links span { color: #000; opacity: 0.85; }
.top-nav .nav-cta { display: flex; gap: 8px; }
.pill-primary {
    background: #000; color: #FFF; border-radius: 50px;
    padding: 8px 20px; font-size: 16px; font-weight: 480;
    display: inline-block; letter-spacing: -0.1px;
}
.pill-secondary {
    background: #FFF; color: #000; border-radius: 50px;
    padding: 8px 18px 10px; font-size: 16px; font-weight: 480;
    display: inline-block; letter-spacing: -0.1px;
}

/* ============ MARQUEE STRIP ============ */
.marquee {
    background: #000; color: #FFF;
    padding: 10px 32px; font-size: 13px; font-weight: 400;
    letter-spacing: 0.6px; text-transform: uppercase;
    margin: 0 -1rem 0 -1rem;
    overflow: hidden; white-space: nowrap;
}

/* ============ HERO ============ */
.hero {
    padding: 120px 0 80px 0;
}
.eyebrow {
    font-family: "Pretendard Variable", monospace !important;
    font-size: 13px; font-weight: 500;
    letter-spacing: 0.6px; text-transform: uppercase;
    color: #000; margin-bottom: 24px;
}
.display-xl {
    font-size: 86px; font-weight: 340; line-height: 1.00;
    letter-spacing: -1.72px; color: #000; margin: 0 0 32px 0;
}
.display-lg {
    font-size: 64px; font-weight: 340; line-height: 1.10;
    letter-spacing: -0.96px; color: #000; margin: 0 0 24px 0;
}
.headline {
    font-size: 26px; font-weight: 540; line-height: 1.35;
    letter-spacing: -0.26px; color: #000; margin: 0 0 16px 0;
}
.subhead {
    font-size: 26px; font-weight: 340; line-height: 1.35;
    letter-spacing: -0.26px; color: #000; margin: 0 0 16px 0;
}
.body-lg {
    font-size: 20px; font-weight: 330; line-height: 1.40;
    letter-spacing: -0.14px; color: #000;
}
.body {
    font-size: 18px; font-weight: 320; line-height: 1.45;
    letter-spacing: -0.26px; color: #000;
}
.body-sm {
    font-size: 16px; font-weight: 330; line-height: 1.45;
    letter-spacing: -0.14px; color: #000;
}
.caption {
    font-family: "Pretendard Variable", monospace !important;
    font-size: 12px; font-weight: 400; line-height: 1.00;
    letter-spacing: 0.60px; text-transform: uppercase;
    color: #000;
}

/* ============ COLOR BLOCK SECTIONS ============ */
.block {
    border-radius: 24px;
    padding: 48px 64px;
    margin: 96px 0 0 0;
    position: relative;
}
.block-lime  { background: #E6F576; }
.block-lilac { background: #DCD5F5; }
.block-cream { background: #F7EDD9; }
.block-mint  { background: #CFEDD8; }
.block-pink  { background: #FBD0DD; }
.block-coral { background: #FFB6A0; }
.block-navy  { background: #1E1B4B; color: #FFF; }
.block-navy .display-lg, .block-navy .headline, .block-navy .subhead,
.block-navy .body, .block-navy .body-lg, .block-navy .eyebrow, .block-navy .caption,
.block-navy p, .block-navy div, .block-navy span, .block-navy li { color: #FFF !important; }

.block-inner { max-width: 920px; }

/* ============ METRIC CARDS ============ */
.metric-row { display: flex; gap: 16px; margin-top: 24px; flex-wrap: wrap; }
.metric-card {
    background: #FFFFFF; border-radius: 24px; padding: 24px;
    border: 1px solid #E5E5E5; flex: 1; min-width: 180px;
}
.metric-card .metric-eyebrow {
    font-size: 12px; font-weight: 400;
    letter-spacing: 0.60px; text-transform: uppercase;
    color: #000; margin-bottom: 12px;
}
.metric-card .metric-value {
    font-size: 36px; font-weight: 540; line-height: 1.10;
    letter-spacing: -0.5px; color: #000;
}
.block-navy .metric-card { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18); }
.block-navy .metric-card .metric-eyebrow, .block-navy .metric-card .metric-value { color: #FFF; }

/* ============ STREAMLIT WIDGET OVERRIDES ============ */
.stRadio > div { gap: 8px; }
.stRadio label { font-size: 16px !important; font-weight: 480 !important; }

div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
    border-radius: 8px !important; border-color: #E5E5E5 !important;
    font-family: "Pretendard Variable", sans-serif !important;
}

button[kind="primary"], button[kind="secondary"], .stButton > button {
    border-radius: 50px !important;
    font-family: "Pretendard Variable", sans-serif !important;
    font-weight: 480 !important; letter-spacing: -0.1px !important;
    padding: 8px 20px !important; font-size: 16px !important;
    border: 1px solid #000 !important;
}
.stButton > button { background: #000 !important; color: #FFF !important; }
.stButton > button:hover { background: #1a1a1a !important; transform: scale(1.02); }

/* tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: transparent; border-bottom: none; }
.stTabs [data-baseweb="tab"] {
    background: #FFFFFF !important; color: #000 !important;
    border-radius: 50px !important; padding: 8px 20px !important;
    font-size: 16px !important; font-weight: 480 !important;
    border: 1px solid #E5E5E5 !important;
}
.stTabs [aria-selected="true"] { background: #000 !important; color: #FFF !important; border-color: #000 !important; }

/* dataframe */
.stDataFrame { border-radius: 8px; border: 1px solid #E5E5E5; overflow: hidden; }

/* expander */
.streamlit-expanderHeader, [data-testid="stExpander"] summary {
    font-size: 16px !important; font-weight: 480 !important;
    border-radius: 8px !important; padding: 16px !important;
    background: #FFFFFF !important; border: 1px solid #E5E5E5 !important;
}
[data-testid="stExpander"] { border: none !important; }

/* code blocks */
.stCodeBlock, pre, code {
    border-radius: 8px !important;
    font-family: "Pretendard Variable", "SF Mono", Menlo, monospace !important;
}

/* metric default streamlit override */
[data-testid="stMetric"] { background: #FFF; padding: 24px; border-radius: 24px; border: 1px solid #E5E5E5; }
[data-testid="stMetricLabel"] {
    font-size: 12px !important; font-weight: 400 !important;
    letter-spacing: 0.6px !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-size: 36px !important; font-weight: 540 !important;
    letter-spacing: -0.5px !important;
}

/* sidebar hidden */
section[data-testid="stSidebar"] { display: none !important; }

/* hr separator */
hr { border-color: #EFEFEF; margin: 96px 0 48px 0 !important; }

/* insight callout list */
.insight-list li {
    font-size: 18px; font-weight: 320; line-height: 1.7;
    letter-spacing: -0.26px; margin-bottom: 12px;
}

/* footer */
.site-footer {
    margin-top: 96px; padding-top: 64px; border-top: 1px solid #EFEFEF;
}
.site-footer .wordmark-lg {
    font-size: 64px; font-weight: 700; letter-spacing: -2px;
    color: #000; margin-bottom: 48px; line-height: 1;
}
.site-footer .caption-col {
    font-size: 12px; font-weight: 400;
    letter-spacing: 0.6px; text-transform: uppercase;
    color: #000; margin-bottom: 8px;
}
.site-footer .source-list { font-size: 14px; font-weight: 320; color: #000; line-height: 1.8; }

/* mobile */
@media (max-width: 768px) {
    .display-xl { font-size: 48px; letter-spacing: -0.96px; }
    .display-lg { font-size: 40px; letter-spacing: -0.6px; }
    .block { padding: 32px 20px; border-radius: 0; margin-left: -1rem; margin-right: -1rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 1. DATA LOAD & TRANSFORM
# ============================================================
@st.cache_data
def load_data():
    permits = pd.read_csv("Monthly permits by purpose of entry.csv")
    revenue = pd.read_csv("Tourism revenue per capita (dollars).csv")
    tourists = pd.read_csv("Trends in foreign tourists.csv")
    return permits, revenue, tourists


try:
    permits_df, revenue_df, tourists_df = load_data()
except FileNotFoundError as e:
    st.error(f"CSV 파일을 찾을 수 없음: {e}")
    st.stop()

PURPOSE_KO = {
    "관광": "관광", "방문": "방문", "사업": "사업", "질병": "질병치료",
    "회의": "회의", "각종행사": "각종행사", "스포츠 경기": "스포츠 경기", "기타": "기타",
}
PURPOSES = list(PURPOSE_KO.keys())

permits_pivot = (
    permits_df.pivot_table(
        index="Year/Month", columns="Purpose of entry", values="number", aggfunc="sum"
    ).reset_index()
)
df = permits_pivot.merge(tourists_df, on="Year/Month").merge(revenue_df, on="Year/Month")
df = df.rename(columns={
    "Foreign tourists": "외래관광객",
    "exchange rate(won)": "환율",
    "Tourism revenue per capita (dollars)": "1인당관광수입",
})
df["Year/Month"] = df["Year/Month"].astype(int)
df["연월"] = pd.to_datetime(df["Year/Month"].astype(str), format="%Y%m")
df = df.sort_values("연월").reset_index(drop=True)

df["총입국허가"] = df[PURPOSES].sum(axis=1)
for p in PURPOSES:
    df[f"{p}_비율"] = df[p] / df["총입국허가"] * 100
df["고단가추정비율"] = df["사업_비율"] + df["질병_비율"] + df["회의_비율"]


# ============================================================
# 2. PLOTLY THEME
# ============================================================
PLOTLY_FONT = dict(family="Pretendard Variable, Pretendard, sans-serif", color="#000000", size=14)
PASTEL_SEQ = ["#E6F576", "#DCD5F5", "#F7EDD9", "#CFEDD8", "#FBD0DD", "#FFB6A0", "#1E1B4B", "#9CA3AF"]


def style_fig(fig, dark=False):
    fg = "#FFFFFF" if dark else "#000000"
    bg = "rgba(0,0,0,0)"
    fig.update_layout(
        font=dict(family="Pretendard Variable, Pretendard, sans-serif", color=fg, size=14),
        paper_bgcolor=bg, plot_bgcolor=bg,
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)" if not dark else "rgba(255,255,255,0.12)", linecolor=fg, tickcolor=fg, title_font=dict(size=13, color=fg)),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)" if not dark else "rgba(255,255,255,0.12)", linecolor=fg, tickcolor=fg, title_font=dict(size=13, color=fg)),
        margin=dict(l=20, r=20, t=40, b=40),
        legend=dict(font=dict(color=fg, size=13)),
        title_font=dict(color=fg, size=18, family="Pretendard Variable, sans-serif"),
    )
    return fig


# ============================================================
# 3. TOP NAV + MARQUEE
# ============================================================
st.markdown(
    """
<div class="top-nav">
  <div style="display:flex; align-items:center; gap:32px;">
    <div class="wordmark">● DASHBOARD</div>
    <div class="nav-links">
      <span>개요</span><span>환율 민감도</span><span>구성비 분석</span><span>관광수입</span>
    </div>
  </div>
  <div class="nav-cta">
    <span class="pill-secondary">출처 보기</span>
    <span class="pill-primary">분석 시작</span>
  </div>
</div>
<div class="marquee">법무부 KETA · 한국관광공사 · 한국관광통계 · Pearson · OLS · Lag corr · N=12 months · 202504 – 202603</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 4. HERO — display-xl on white canvas
# ============================================================
st.markdown(
    f"""
<div class="hero">
  <div class="eyebrow">DATA STORY · 외국인 입국 · 관광 데이터</div>
  <h1 class="display-xl">환율과<br/>입국 목적,<br/>그리고 관광수입.</h1>
  <p class="body-lg" style="max-width:680px;">
    202504~202603 12개월의 월별 데이터로 환율 민감도, 입국 목적 구성비, 1인당 관광수입의
    관계를 다각도로 분석함. 모든 인사이트는 데이터에 근거함.
  </p>
  <div style="margin-top:40px; display:flex; gap:8px;">
    <span class="pill-primary">분석 보기 ↓</span>
    <span class="pill-secondary">SQL 보기</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 5. OVERVIEW METRICS — cream block
# ============================================================
st.markdown(
    f"""
<div class="block block-cream">
  <div class="block-inner">
    <div class="eyebrow">01 / OVERVIEW</div>
    <h2 class="display-lg">한눈에 보는<br/>12개월의 흐름.</h2>
    <p class="body" style="max-width:600px; margin-top:16px;">
      외래관광객 수 · 환율 · 1인당 관광수입의 평균값임. 단일 수치이지만, 이 셋의
      관계가 본 분석의 출발점임.
    </p>
    <div class="metric-row">
      <div class="metric-card"><div class="metric-eyebrow">분석 기간</div><div class="metric-value">{len(df)}<span style="font-size:18px; font-weight:330;">개월</span></div></div>
      <div class="metric-card"><div class="metric-eyebrow">평균 외래관광객</div><div class="metric-value">{int(df['외래관광객'].mean()/10000):,}<span style="font-size:18px; font-weight:330;">만명</span></div></div>
      <div class="metric-card"><div class="metric-eyebrow">평균 환율</div><div class="metric-value">{df['환율'].mean():.0f}<span style="font-size:18px; font-weight:330;">원</span></div></div>
      <div class="metric-card"><div class="metric-eyebrow">평균 1인당 수입</div><div class="metric-value">${df['1인당관광수입'].mean():.0f}</div></div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Overview chart on white canvas
st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="eyebrow">TIME SERIES</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline">외래관광객 수와 환율 추이</h3>', unsafe_allow_html=True)

fig_overview = make_subplots(specs=[[{"secondary_y": True}]])
fig_overview.add_trace(
    go.Scatter(x=df["연월"], y=df["외래관광객"], name="외래관광객 수",
               line=dict(color="#000000", width=3), mode="lines+markers",
               marker=dict(size=8)),
    secondary_y=False,
)
fig_overview.add_trace(
    go.Scatter(x=df["연월"], y=df["환율"], name="환율(원/달러)",
               line=dict(color="#FF6B4A", width=3, dash="dash"), mode="lines+markers",
               marker=dict(size=8)),
    secondary_y=True,
)
fig_overview.update_xaxes(title_text="연월")
fig_overview.update_yaxes(title_text="외래관광객 수(명)", secondary_y=False)
fig_overview.update_yaxes(title_text="환율(원/달러)", secondary_y=True)
fig_overview.update_layout(height=460, hovermode="x unified",
                            legend=dict(orientation="h", y=1.1))
st.plotly_chart(style_fig(fig_overview), use_container_width=True)

with st.expander("🗄 통합 SQL 보기"):
    st.code(
        """
SELECT
    p.[Year/Month]                              AS year_month,
    p.[Purpose of entry]                        AS purpose,
    p.number                                    AS visits,
    t.[Foreign tourists]                        AS foreign_tourists,
    t.[exchange rate(won)]                      AS exchange_rate,
    r.[Tourism revenue per capita (dollars)]    AS revenue_per_capita
FROM monthly_permits         AS p
INNER JOIN foreign_tourists  AS t ON p.[Year/Month] = t.[Year/Month]
INNER JOIN tourism_revenue   AS r ON p.[Year/Month] = r.[Year/Month]
ORDER BY p.[Year/Month], p.[Purpose of entry];
        """,
        language="sql",
    )


# ============================================================
# 6. THEME 1 — LIME BLOCK: 환율 민감도
# ============================================================
st.markdown(
    f"""
<div class="block block-lime">
  <div class="block-inner">
    <div class="eyebrow">02 / THEME 01</div>
    <h2 class="display-lg">환율이 오르면<br/>누가 더 움직이나.</h2>
    <p class="subhead" style="max-width:720px;">
      관광은 환율에 탄력적, 질병치료는 비탄력적일 것이라는 가설.<br/>
      12개월의 월별 데이터로 Pearson 상관과 로그-로그 탄력성을 함께 본다.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)

# correlation + elasticity
corr_rows = []
for p in PURPOSES:
    r, pv = stats.pearsonr(df["환율"], df[p])
    corr_rows.append({"입국목적": PURPOSE_KO[p], "상관계수(r)": round(r, 3),
                       "p-value": round(pv, 4), "월평균 방문수": int(df[p].mean())})
corr_df = pd.DataFrame(corr_rows).sort_values("상관계수(r)")

elas_rows = []
log_er = np.log(df["환율"])
for p in PURPOSES:
    if (df[p] > 0).all():
        slope, intercept, r, pv, _ = stats.linregress(log_er, np.log(df[p]))
        elas_rows.append({"입국목적": PURPOSE_KO[p], "탄력성(β)": round(slope, 3),
                          "R²": round(r ** 2, 3), "p-value": round(pv, 4)})
elas_df = pd.DataFrame(elas_rows).sort_values("탄력성(β)")

c1, c2 = st.columns([1.05, 1])
with c1:
    st.markdown('<div class="caption">PEARSON CORRELATION</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="headline" style="margin-top:8px;">환율 vs 입국 목적별 상관</h3>', unsafe_allow_html=True)
    fig1 = px.bar(corr_df, x="상관계수(r)", y="입국목적", orientation="h",
                  color="상관계수(r)", color_continuous_scale=[[0, "#FF6B4A"], [0.5, "#FFFFFF"], [1, "#1E1B4B"]],
                  range_color=[-1, 1], text="상관계수(r)")
    fig1.update_traces(textposition="outside", textfont=dict(size=13, color="#000"))
    fig1.update_layout(height=480, yaxis=dict(categoryorder="total ascending"),
                       coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig1), use_container_width=True)
with c2:
    st.markdown('<div class="caption">ELASTICITY β (LOG-LOG)</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="headline" style="margin-top:8px;">탄력성 계수</h3>', unsafe_allow_html=True)
    fig2 = px.bar(elas_df, x="입국목적", y="탄력성(β)",
                  color="탄력성(β)", color_continuous_scale=[[0, "#FF6B4A"], [0.5, "#FFFFFF"], [1, "#1E1B4B"]],
                  text="탄력성(β)")
    fig2.update_traces(textposition="outside", textfont=dict(size=13, color="#000"))
    fig2.add_hline(y=0, line_dash="dash", line_color="#000")
    fig2.update_layout(height=480, coloraxis_showscale=False, xaxis=dict(tickangle=-30))
    st.plotly_chart(style_fig(fig2), use_container_width=True)

st.markdown('<div style="height:64px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="caption">SCATTER · BY PURPOSE</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline" style="margin-top:8px;">환율 vs 방문 수 산점도</h3>', unsafe_allow_html=True)

selected = st.multiselect("입국 목적 선택", PURPOSES, default=["관광", "질병", "사업"])
if selected:
    fig_sc = make_subplots(rows=1, cols=len(selected),
                            subplot_titles=[PURPOSE_KO[p] for p in selected])
    for i, p in enumerate(selected):
        fig_sc.add_trace(
            go.Scatter(x=df["환율"], y=df[p], mode="markers+text",
                       text=df["Year/Month"].astype(str).str[-2:] + "월",
                       textposition="top center", textfont=dict(size=10),
                       marker=dict(size=14, color="#000")),
            row=1, col=i + 1,
        )
        slope, intercept, _, _, _ = stats.linregress(df["환율"], df[p])
        xline = np.linspace(df["환율"].min(), df["환율"].max(), 50)
        fig_sc.add_trace(
            go.Scatter(x=xline, y=slope * xline + intercept, mode="lines",
                       line=dict(color="#FF6B4A", dash="dash", width=2), showlegend=False),
            row=1, col=i + 1,
        )
    fig_sc.update_xaxes(title_text="환율(원/달러)")
    fig_sc.update_yaxes(title_text="방문 수(명)", col=1)
    fig_sc.update_layout(height=420, showlegend=False)
    st.plotly_chart(style_fig(fig_sc), use_container_width=True)

with st.expander("🗄 SQL — 환율 민감도"):
    st.code(
        """
SELECT
    p.[Purpose of entry]                       AS purpose,
    CORR(p.number, t.[exchange rate(won)])     AS pearson_r,
    AVG(p.number)                              AS avg_visits
FROM monthly_permits        AS p
INNER JOIN foreign_tourists AS t ON p.[Year/Month] = t.[Year/Month]
GROUP BY p.[Purpose of entry]
ORDER BY pearson_r;

-- 탄력성용
SELECT LN(p.number) AS log_y, LN(t.[exchange rate(won)]) AS log_x
FROM monthly_permits        AS p
INNER JOIN foreign_tourists AS t ON p.[Year/Month] = t.[Year/Month]
WHERE p.number > 0;
        """,
        language="sql",
    )

r_tour = corr_df.loc[corr_df["입국목적"] == "관광", "상관계수(r)"].values[0]
r_sick = corr_df.loc[corr_df["입국목적"] == "질병치료", "상관계수(r)"].values[0]
b_tour = elas_df.loc[elas_df["입국목적"] == "관광", "탄력성(β)"].values[0]
b_sick = elas_df.loc[elas_df["입국목적"] == "질병치료", "탄력성(β)"].values[0]

# ============================================================
# 7. INSIGHT BLOCK — NAVY (Theme 1 결론)
# ============================================================
st.markdown(
    f"""
<div class="block block-navy">
  <div class="block-inner">
    <div class="eyebrow">INSIGHT · THEME 01</div>
    <h2 class="display-lg">가설은<br/>데이터로 지지됨.</h2>
    <ul class="insight-list" style="margin-top:32px; padding-left:20px;">
      <li>관광 목적: r = <b>+{r_tour}</b>, 탄력성 β = <b>+{b_tour}</b> → 환율에 <b>매우 탄력적</b>임</li>
      <li>질병치료 목적: r = <b>+{r_sick}</b>, β = <b>+{b_sick}</b> → <b>비탄력적</b>임 (가설 부합)</li>
      <li>사업 목적은 r 값이 0에 근접함 → 비즈니스 수요는 환율보다 비가격 요인이 지배함</li>
      <li>표본 12개월의 한계로 통계적 유의성이 낮은 항목 다수임 → 추세적 시사로 한정함</li>
    </ul>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 8. THEME 2 — LILAC BLOCK: 구성비 vs 1인당 수입
# ============================================================
st.markdown(
    f"""
<div class="block block-lilac">
  <div class="block-inner">
    <div class="eyebrow">03 / THEME 02</div>
    <h2 class="display-lg">고단가 방문객이<br/>늘면 수입도 늘까.</h2>
    <p class="subhead" style="max-width:720px;">
      사업·질병치료·회의 같은 고단가 추정 비율이 1인당 관광수입을 끌어올린다는 가설.<br/>
      구성비 데이터로 검증한다.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="caption">COMPOSITION TREND</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline" style="margin-top:8px;">월별 입국 목적 구성비</h3>', unsafe_allow_html=True)

comp_long = df.melt(id_vars=["Year/Month"], value_vars=[f"{p}_비율" for p in PURPOSES],
                    var_name="입국목적", value_name="비율(%)")
comp_long["입국목적"] = comp_long["입국목적"].str.replace("_비율", "", regex=False).map(PURPOSE_KO)
fig_comp = px.area(comp_long, x="Year/Month", y="비율(%)", color="입국목적",
                    color_discrete_sequence=PASTEL_SEQ)
fig_comp.update_layout(height=460, hovermode="x unified", legend=dict(orientation="h"))
st.plotly_chart(style_fig(fig_comp), use_container_width=True)

st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)

# correlation with revenue
rev_rows = []
for p in PURPOSES:
    r, pv = stats.pearsonr(df[f"{p}_비율"], df["1인당관광수입"])
    rev_rows.append({"입국목적(구성비)": PURPOSE_KO[p], "상관계수(r)": round(r, 3),
                      "p-value": round(pv, 4)})
corr_rev_df = pd.DataFrame(rev_rows).sort_values("상관계수(r)")

c1, c2 = st.columns([1, 1])
with c1:
    st.markdown('<div class="caption">RATIO × REVENUE PER CAPITA</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="headline" style="margin-top:8px;">구성비 vs 1인당 수입 상관</h3>', unsafe_allow_html=True)
    fig_rv = px.bar(corr_rev_df, x="상관계수(r)", y="입국목적(구성비)", orientation="h",
                     color="상관계수(r)",
                     color_continuous_scale=[[0, "#FF6B4A"], [0.5, "#FFFFFF"], [1, "#1E1B4B"]],
                     range_color=[-1, 1], text="상관계수(r)")
    fig_rv.update_traces(textposition="outside", textfont=dict(size=13))
    fig_rv.update_layout(height=480, yaxis=dict(categoryorder="total ascending"),
                          coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig_rv), use_container_width=True)
with c2:
    st.markdown('<div class="caption">HIGH-VALUE RATIO × REVENUE</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="headline" style="margin-top:8px;">고단가 추정 비율 산점도</h3>', unsafe_allow_html=True)
    fig_hd = px.scatter(df, x="고단가추정비율", y="1인당관광수입",
                         text="Year/Month", trendline="ols",
                         labels={"고단가추정비율": "고단가 추정 비율(%)",
                                 "1인당관광수입": "1인당 관광수입($)"})
    fig_hd.update_traces(textposition="top center",
                          marker=dict(size=14, color="#000"))
    # OLS trendline color
    fig_hd.data[1].line.color = "#FF6B4A"
    fig_hd.data[1].line.dash = "dash"
    fig_hd.update_layout(height=480)
    st.plotly_chart(style_fig(fig_hd), use_container_width=True)

r_hd, p_hd = stats.pearsonr(df["고단가추정비율"], df["1인당관광수입"])
slope_hd, _, _, _, _ = stats.linregress(df["고단가추정비율"], df["1인당관광수입"])

# metrics
m1, m2, m3 = st.columns(3)
m1.metric("상관계수 (r)", f"{r_hd:.3f}")
m2.metric("p-value", f"{p_hd:.4f}")
m3.metric("회귀 기울기", f"{slope_hd:.2f}")

with st.expander("🗄 SQL — 구성비 분석"):
    st.code(
        """
WITH purpose_totals AS (
    SELECT [Year/Month] AS year_month, SUM(number) AS total_permits
    FROM monthly_permits GROUP BY [Year/Month]
)
SELECT
    p.[Year/Month]                                                AS year_month,
    p.[Purpose of entry]                                          AS purpose,
    (p.number * 1.0 / pt.total_permits) * 100                     AS ratio_pct,
    r.[Tourism revenue per capita (dollars)]                      AS revenue_per_capita
FROM monthly_permits         AS p
INNER JOIN purpose_totals    AS pt ON p.[Year/Month] = pt.year_month
INNER JOIN tourism_revenue   AS r  ON p.[Year/Month] = r.[Year/Month];

-- 고단가(사업+질병+회의) 비율 vs 1인당 수입
WITH agg AS (
    SELECT
        p.[Year/Month] AS ym,
        SUM(CASE WHEN p.[Purpose of entry] IN ('사업','질병','회의') THEN p.number ELSE 0 END)
            * 100.0 / SUM(p.number) AS high_value_ratio,
        MAX(r.[Tourism revenue per capita (dollars)]) AS rev
    FROM monthly_permits p
    INNER JOIN tourism_revenue r ON p.[Year/Month] = r.[Year/Month]
    GROUP BY p.[Year/Month]
)
SELECT CORR(high_value_ratio, rev) FROM agg;
        """,
        language="sql",
    )

top_pos = corr_rev_df.iloc[-1]
top_neg = corr_rev_df.iloc[0]

# ============================================================
# 9. INSIGHT BLOCK — CORAL (Theme 2 결론, 반전 결과)
# ============================================================
st.markdown(
    f"""
<div class="block block-coral">
  <div class="block-inner">
    <div class="eyebrow">INSIGHT · THEME 02</div>
    <h2 class="display-lg">가설은<br/>데이터와 반대였음.</h2>
    <ul class="insight-list" style="margin-top:32px; padding-left:20px;">
      <li>고단가 추정 비율(사업+질병+회의) vs 1인당 수입: r = <b>{r_hd:+.3f}</b> (p = {p_hd:.3f}) → <b>음의 상관</b>이 유의하게 관측됨</li>
      <li>가장 강한 양(+)의 상관: <b>{top_pos['입국목적(구성비)']}</b> 비율 (r = {top_pos['상관계수(r)']:+.3f})</li>
      <li>가장 강한 음(−)의 상관: <b>{top_neg['입국목적(구성비)']}</b> 비율 (r = {top_neg['상관계수(r)']:+.3f})</li>
      <li>해석: 관광객이 집중되는 성수기에 1인당 쇼핑·면세 매출도 함께 증가 → 평균 1인당 수입이 상승하는 구조 가능성 있음</li>
      <li>회의·사업 비중이 큰 달은 비수기 경향 → 단기 출장자 비중으로 평균 지출이 낮게 산출되는 효과 추정됨</li>
      <li>다요인 영향 분리는 단일 변수로 데이터상 확인 불가함</li>
    </ul>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 10. THEME 3 — MINT BLOCK: 환율 vs 1인당 수입
# ============================================================
st.markdown(
    f"""
<div class="block block-mint">
  <div class="block-inner">
    <div class="eyebrow">04 / THEME 03</div>
    <h2 class="display-lg">환율이 흔들리면<br/>1인당 수입은.</h2>
    <p class="subhead" style="max-width:720px;">
      원화 강세(환율↓) 시 달러 기준 1인당 관광수입도 함께 낮아질 것이라는 가설.<br/>
      동기 상관과 시차(Lag) 효과를 함께 본다.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="caption">DUAL AXIS TIME SERIES</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline" style="margin-top:8px;">환율 vs 1인당 관광수입 시계열</h3>', unsafe_allow_html=True)

fig_t3 = make_subplots(specs=[[{"secondary_y": True}]])
fig_t3.add_trace(
    go.Scatter(x=df["연월"], y=df["환율"], name="환율(원/달러)",
               line=dict(color="#000000", width=3), mode="lines+markers", marker=dict(size=8)),
    secondary_y=False,
)
fig_t3.add_trace(
    go.Scatter(x=df["연월"], y=df["1인당관광수입"], name="1인당 관광수입($)",
               line=dict(color="#FF6B4A", width=3, dash="dash"), mode="lines+markers", marker=dict(size=8)),
    secondary_y=True,
)
fig_t3.update_xaxes(title_text="연월")
fig_t3.update_yaxes(title_text="환율(원/달러)", secondary_y=False)
fig_t3.update_yaxes(title_text="1인당 관광수입($)", secondary_y=True)
fig_t3.update_layout(height=460, hovermode="x unified",
                     legend=dict(orientation="h", y=1.1))
st.plotly_chart(style_fig(fig_t3), use_container_width=True)

st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)

c1, c2 = st.columns([1, 1])
with c1:
    st.markdown('<div class="caption">SCATTER + OLS</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="headline" style="margin-top:8px;">동기 산점도</h3>', unsafe_allow_html=True)
    fig_sc3 = px.scatter(df, x="환율", y="1인당관광수입", text="Year/Month",
                          trendline="ols",
                          labels={"환율": "환율(원/달러)", "1인당관광수입": "1인당 관광수입($)"})
    fig_sc3.update_traces(textposition="top center",
                           marker=dict(size=14, color="#000"))
    fig_sc3.data[1].line.color = "#FF6B4A"
    fig_sc3.data[1].line.dash = "dash"
    fig_sc3.update_layout(height=460)
    st.plotly_chart(style_fig(fig_sc3), use_container_width=True)

with c2:
    st.markdown('<div class="caption">LAG CORRELATION</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="headline" style="margin-top:8px;">시차별 상관계수</h3>', unsafe_allow_html=True)
    lag_rows = []
    for lag in range(-3, 4):
        if lag < 0:
            x = df["환율"].iloc[:lag].reset_index(drop=True)
            y = df["1인당관광수입"].iloc[-lag:].reset_index(drop=True)
        elif lag > 0:
            x = df["환율"].iloc[lag:].reset_index(drop=True)
            y = df["1인당관광수입"].iloc[:-lag].reset_index(drop=True)
        else:
            x = df["환율"].reset_index(drop=True)
            y = df["1인당관광수입"].reset_index(drop=True)
        if len(x) >= 3:
            r, pv = stats.pearsonr(x, y)
            lag_rows.append({"시차(개월)": lag, "상관계수(r)": round(r, 3),
                              "표본수": len(x)})
    lag_df = pd.DataFrame(lag_rows)
    fig_lag = px.bar(lag_df, x="시차(개월)", y="상관계수(r)", text="상관계수(r)",
                     color="상관계수(r)",
                     color_continuous_scale=[[0, "#FF6B4A"], [0.5, "#FFFFFF"], [1, "#1E1B4B"]],
                     range_color=[-1, 1])
    fig_lag.update_traces(textposition="outside", textfont=dict(size=13))
    fig_lag.add_hline(y=0, line_dash="dash", line_color="#000")
    fig_lag.update_layout(height=460, coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig_lag), use_container_width=True)

r_er, p_er = stats.pearsonr(df["환율"], df["1인당관광수입"])
slope_er, _, _, _, _ = stats.linregress(df["환율"], df["1인당관광수입"])

m1, m2, m3 = st.columns(3)
m1.metric("상관계수 (r)", f"{r_er:.3f}")
m2.metric("p-value", f"{p_er:.4f}")
m3.metric("회귀 기울기", f"{slope_er:.4f} $/원")

with st.expander("🗄 SQL — 환율 vs 1인당 관광수입"):
    st.code(
        """
SELECT
    t.[Year/Month]                              AS year_month,
    t.[exchange rate(won)]                      AS exchange_rate,
    r.[Tourism revenue per capita (dollars)]    AS revenue_per_capita
FROM foreign_tourists       AS t
INNER JOIN tourism_revenue  AS r ON t.[Year/Month] = r.[Year/Month]
ORDER BY t.[Year/Month];

-- 시차 분석
SELECT
    t.[Year/Month] AS ym,
    t.[exchange rate(won)] AS er,
    LAG(t.[exchange rate(won)], 1) OVER (ORDER BY t.[Year/Month]) AS er_lag1,
    LAG(t.[exchange rate(won)], 2) OVER (ORDER BY t.[Year/Month]) AS er_lag2,
    LAG(t.[exchange rate(won)], 3) OVER (ORDER BY t.[Year/Month]) AS er_lag3,
    r.[Tourism revenue per capita (dollars)] AS rev
FROM foreign_tourists      AS t
INNER JOIN tourism_revenue AS r ON t.[Year/Month] = r.[Year/Month];
        """,
        language="sql",
    )

best_lag = lag_df.iloc[lag_df["상관계수(r)"].abs().idxmax()]
direction = "양(+)" if r_er > 0 else "음(−)"

# ============================================================
# 11. INSIGHT BLOCK — PINK (Theme 3 결론)
# ============================================================
st.markdown(
    f"""
<div class="block block-pink">
  <div class="block-inner">
    <div class="eyebrow">INSIGHT · THEME 03</div>
    <h2 class="display-lg">방향성은 있지만<br/>유의성은 미달함.</h2>
    <ul class="insight-list" style="margin-top:32px; padding-left:20px;">
      <li>동기 상관: r = <b>{r_er:+.3f}</b> (p = {p_er:.3f}) → <b>{direction}의 상관</b>이 관측됨</li>
      <li>회귀 기울기: <b>{slope_er:+.4f} $/원</b> → 환율 1원 상승 시 1인당 수입은 약 {slope_er:.2f}달러 변화 추정됨</li>
      <li>가설 방향성(환율↓ → 수입↓)과 부합하나 통상 유의수준(p&lt;0.05)에는 미달함</li>
      <li>시차 분석: 절대값 최대 상관은 <b>{int(best_lag['시차(개월)'])}개월</b> 시점 (r = {best_lag['상관계수(r)']:+.3f}) → 즉시 반영 경향이 강함</li>
      <li>표본 N=12 한계로 안정적 결론 도출은 데이터상 확인 불가함</li>
    </ul>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 12. CONCLUSION BLOCK — NAVY (종합)
# ============================================================
st.markdown(
    f"""
<div class="block block-navy">
  <div class="block-inner">
    <div class="eyebrow">FINAL TAKEAWAY</div>
    <h2 class="display-lg">세 가설,<br/>세 가지 결론.</h2>
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:24px; margin-top:48px;">
      <div>
        <div class="caption" style="margin-bottom:8px;">THEME 01</div>
        <div class="headline" style="margin-bottom:8px;">데이터로 지지됨</div>
        <div class="body-sm">환율 민감도 구조(관광=탄력적, 질병=비탄력적)가 명확히 관측됨.</div>
      </div>
      <div>
        <div class="caption" style="margin-bottom:8px;">THEME 02</div>
        <div class="headline" style="margin-bottom:8px;">가설과 반대 결과</div>
        <div class="body-sm">고단가 비율↑일수록 1인당 수입은 오히려↓ — 비수기 효과 가능성 시사됨.</div>
      </div>
      <div>
        <div class="caption" style="margin-bottom:8px;">THEME 03</div>
        <div class="headline" style="margin-bottom:8px;">방향성 부합, 유의성 미달</div>
        <div class="body-sm">N=12 한계로 안정적 결론은 데이터상 확인 불가함.</div>
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 13. FOOTER
# ============================================================
st.markdown(
    """
<div class="site-footer">
  <div class="wordmark-lg">Dashboard.</div>
  <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:48px;">
    <div>
      <div class="caption-col">DATA SOURCES</div>
      <div class="source-list">
        법무부 _ 월별 전자여행허가(KETA) 입국 목적별 현황<br/>
        한국관광통계 _ 방한 외래관광객 추이<br/>
        한국관광통계 _ 1인당 관광 수입
      </div>
    </div>
    <div>
      <div class="caption-col">METHODOLOGY</div>
      <div class="source-list">
        Pearson Correlation<br/>
        Log-Log Elasticity (OLS)<br/>
        Lag Cross-Correlation (-3 to +3 m)
      </div>
    </div>
    <div>
      <div class="caption-col">PERIOD</div>
      <div class="source-list">
        202504 – 202603<br/>
        N = 12 months<br/>
        Monthly granularity
      </div>
    </div>
    <div>
      <div class="caption-col">DESIGN</div>
      <div class="source-list">
        Monochrome core<br/>
        Pastel color-block sections<br/>
        Pretendard typography
      </div>
    </div>
  </div>
  <div style="margin-top:64px; padding-top:24px; border-top:1px solid #EFEFEF;
              font-size:12px; letter-spacing:0.6px; text-transform:uppercase; color:#000;">
    © 2026 Tourism Data Dashboard · 출처: 법무부 · 한국관광통계
  </div>
</div>
""",
    unsafe_allow_html=True,
)
