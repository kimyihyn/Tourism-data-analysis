"""
외국인 입국·관광 데이터 분석 대시보드
Design System: Figma Marketing (monochrome core + pastel color blocks)
Typography: Pretendard only
"""

import streamlit as st
import streamlit.components.v1 as components
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
# 1. Pretendard 폰트 — 부모 문서 head에 강제 주입
#    (streamlit sanitizer는 <link>를 제거하므로 JS로 우회)
# ============================================================
# 기존 components.html 부분을 아래와 같이 수정
components.html(
    """
    <script>
    window.addEventListener('load', function() {
      var doc = window.parent.document;
      if (!doc.getElementById('pretendard-font-link')) {
        var link = doc.createElement('link');
        link.id = 'pretendard-font-link';
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css';
        doc.head.appendChild(link);
      }
    });
    </script>
    """,
    height=0,
)

# ============================================================
# 2. CSS — 텍스트 요소에만 Pretendard, 아이콘(svg/material)은 제외
# ============================================================
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');

/* === Pretendard 적용 (텍스트 요소만 명시) === */
html, body, .stApp {
    font-family: "Pretendard Variable", "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}

/* 일반 텍스트 */
p, h1, h2, h3, h4, h5, h6,
li, label, td, th, caption {
    font-family: inherit;
}

/* streamlit markdown text */
[data-testid="stMarkdownContainer"] * {
    font-family: inherit;
}

/* input text only */
input, textarea, select {
    font-family: inherit !important;
}
span[data-testid="stWidgetLabel"] p, 
.stExpander summary p, 
[data-testid="stHeader"] {
    font-family: "Pretendard Variable", "Pretendard", sans-serif !important;
}


/* === 아이콘 요소는 원본 폰트 유지 (Material Symbols / streamlit icons) === */
svg, svg *, .material-icons, .material-icons-outlined,
[class*="material-symbols"], [class*="MaterialSymbols"],
[data-baseweb="icon"], [data-baseweb="icon"] *,
[class*="iconContainer"], [class*="iconContainer"] *,
[data-testid="stIcon"], [data-testid="stIcon"] *,
[class*="emotion-cache"] svg, [class*="emotion-cache"] svg * {
    font-family: revert !important;
}

.stApp { background: #FFFFFF; color: #000000; }
.main .block-container { padding-top: 0 !important; padding-bottom: 96px !important; max-width: 1280px; }
#MainMenu, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
section[data-testid="stSidebar"] { display: none !important; }

/* === TOP NAV === */
.top-nav {
    position: sticky; top: 0; z-index: 999;
    background: #FFFFFF; border-bottom: 1px solid #EFEFEF;
    padding: 14px 32px;
    display: flex; align-items: center; justify-content: space-between;
    height: 56px; margin: 0 -1rem;
}
.top-nav .wordmark { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
.top-nav .nav-links { display: flex; gap: 24px; font-size: 15px; font-weight: 480; color: #000; }
.top-nav .nav-links a { color: #000; text-decoration: none; opacity: 0.85; }
.top-nav .nav-links a:hover { opacity: 1; }
.top-nav .nav-cta { display: flex; gap: 8px; }

.pill-primary, .pill-secondary {
    border-radius: 50px; padding: 8px 20px;
    font-size: 15px; font-weight: 480; letter-spacing: -0.1px;
    text-decoration: none; display: inline-block;
    transition: transform 0.15s ease;
}
.pill-primary { background: #000; color: #FFF; }
.pill-primary:hover { background: #1a1a1a; transform: scale(1.02); color: #FFF; }
.pill-secondary { background: #FFF; color: #000; border: 1px solid #E5E5E5; }
.pill-secondary:hover { background: #F5F5F5; color: #000; }

/* === MARQUEE === */
.marquee {
    background: #000; color: #FFF;
    padding: 10px 32px; font-size: 13px; font-weight: 400;
    letter-spacing: 0.6px; text-transform: uppercase;
    margin: 0 -1rem; overflow: hidden; white-space: nowrap;
}

/* === TYPOGRAPHY === */
.hero { padding: 120px 0 80px 0; }
.eyebrow {
    font-size: 13px; font-weight: 500; letter-spacing: 0.6px;
    text-transform: uppercase; color: #000; margin-bottom: 24px;
}
.display-xl { font-size: 86px; font-weight: 340; line-height: 1.00; letter-spacing: -1.72px; margin: 0 0 32px; }
.display-lg { font-size: 64px; font-weight: 340; line-height: 1.10; letter-spacing: -0.96px; margin: 0 0 24px; }
.headline   { font-size: 26px; font-weight: 540; line-height: 1.35; letter-spacing: -0.26px; margin: 0 0 16px; }
.subhead    { font-size: 22px; font-weight: 340; line-height: 1.4;  letter-spacing: -0.26px; margin: 0 0 16px; }
.body-lg    { font-size: 19px; font-weight: 330; line-height: 1.50; letter-spacing: -0.14px; }
.body       { font-size: 17px; font-weight: 320; line-height: 1.55; letter-spacing: -0.26px; }
.body-sm    { font-size: 15px; font-weight: 330; line-height: 1.55; letter-spacing: -0.14px; }
.caption    { font-size: 12px; font-weight: 400; letter-spacing: 0.6px; text-transform: uppercase; }

/* === COLOR BLOCKS === */
.block { border-radius: 24px; padding: 56px 64px; margin: 96px 0 0; position: relative; }
.block-lime  { background: #E6F576; }
.block-lilac { background: #DCD5F5; }
.block-cream { background: #F7EDD9; }
.block-mint  { background: #CFEDD8; }
.block-pink  { background: #FBD0DD; }
.block-coral { background: #FFB6A0; }
.block-navy  { background: #1E1B4B; color: #FFF; }
.block-navy *,
.block-navy .display-lg, .block-navy .headline, .block-navy .subhead,
.block-navy .body, .block-navy .body-lg, .block-navy .eyebrow, .block-navy .caption { color: #FFF !important; }
.block-inner { max-width: 920px; }

/* === EXPLAINER CARD (차트 해설 박스) === */
.explainer {
    background: #F5F5F5; border-left: 4px solid #000;
    padding: 20px 24px; border-radius: 8px;
    margin: 16px 0 24px;
}
.explainer .explainer-eyebrow {
    font-size: 11px; font-weight: 500; letter-spacing: 0.6px;
    text-transform: uppercase; color: #000; margin-bottom: 8px; opacity: 0.6;
}
.explainer p { font-size: 15px; font-weight: 330; line-height: 1.6; margin: 0; }

/* === METRIC CARDS === */
.metric-row { display: flex; gap: 16px; margin-top: 32px; flex-wrap: wrap; }
.metric-card {
    background: #FFFFFF; border-radius: 24px; padding: 24px;
    border: 1px solid #E5E5E5; flex: 1; min-width: 180px;
}
.metric-card .metric-eyebrow {
    font-size: 12px; font-weight: 400; letter-spacing: 0.6px;
    text-transform: uppercase; color: #000; margin-bottom: 12px;
}
.metric-card .metric-value { font-size: 34px; font-weight: 540; line-height: 1.10; letter-spacing: -0.5px; color: #000; }
.metric-card .metric-suffix { font-size: 16px; font-weight: 330; }

/* === STREAMLIT WIDGET OVERRIDES === */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: none; }
.stTabs [data-baseweb="tab"] {
    background: #FFFFFF !important; color: #000 !important;
    border-radius: 50px !important; padding: 8px 20px !important;
    font-size: 15px !important; font-weight: 480 !important;
    border: 1px solid #E5E5E5 !important;
}
.stTabs [aria-selected="true"] { background: #000 !important; color: #FFF !important; border-color: #000 !important; }

.stButton > button {
    border-radius: 50px !important; font-weight: 480 !important;
    padding: 8px 24px !important; font-size: 15px !important;
    background: #000 !important; color: #FFF !important;
    border: 1px solid #000 !important;
}
.stButton > button:hover { background: #1a1a1a !important; }

.stDataFrame { border-radius: 8px; border: 1px solid #E5E5E5; overflow: hidden; }

/* === EXPANDER — 아이콘이 텍스트로 깨지지 않도록 svg 기본 폰트 보존 === */
[data-testid="stExpander"] { border: 1px solid #E5E5E5 !important; border-radius: 8px !important; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] details summary {
    font-size: 15px !important; font-weight: 480 !important; padding: 14px 18px !important;
}
[data-testid="stExpander"] svg { font-family: revert !important; }

.stCodeBlock { border-radius: 8px !important; }
pre, code { font-family: "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace !important; }

[data-testid="stMetric"] { background: #FFF; padding: 24px; border-radius: 24px; border: 1px solid #E5E5E5; }
[data-testid="stMetricLabel"] {
    font-size: 12px !important; font-weight: 400 !important;
    letter-spacing: 0.6px !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-size: 34px !important; font-weight: 540 !important; letter-spacing: -0.5px !important;
}

hr { border-color: #EFEFEF; margin: 96px 0 48px !important; }

/* === FOOTER === */
.site-footer { margin-top: 96px; padding-top: 64px; border-top: 1px solid #EFEFEF; }
.site-footer .wordmark-lg { font-size: 64px; font-weight: 700; letter-spacing: -2px; margin-bottom: 48px; line-height: 1; }
.site-footer .caption-col {
    font-size: 12px; font-weight: 400; letter-spacing: 0.6px;
    text-transform: uppercase; margin-bottom: 12px;
}
.site-footer .source-list { font-size: 14px; font-weight: 330; line-height: 1.8; }

/* mobile */
@media (max-width: 768px) {
    .display-xl { font-size: 48px; letter-spacing: -0.96px; }
    .display-lg { font-size: 36px; letter-spacing: -0.5px; }
    .block { padding: 32px 24px; border-radius: 0; margin-left: -1rem; margin-right: -1rem; }
    .top-nav .nav-links { display: none; }
}
.js-plotly-plot .plotly .modebar {
    font-family: sans-serif !important;
}

/* Plotly 차트 텍스트만 Pretendard 적용 */
.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text,
.js-plotly-plot .gtitle text,
.js-plotly-plot .legend text,
.js-plotly-plot .annotation-text,
.js-plotly-plot .hovertext text {
    font-family: "Pretendard Variable", sans-serif !important;
}
/* Plotly modebar tooltip 제거 */
.modebar-btn::after,
.modebar-btn:after,
.modebar-btn--logo::after {
    display: none !important;
    content: "" !important;
}
/* Plotly modebar tooltip 완전 제거 */
.js-plotly-plot .modebar-btn[data-title]:hover::before,
.js-plotly-plot .modebar-btn[data-title]:hover::after {
    display: none !important;
    opacity: 0 !important;
    visibility: hidden !important;
}

.js-plotly-plot .modebar-btn {
    pointer-events: auto;
}

.js-plotly-plot .modebar-btn svg {
    font-family: revert !important;
}

.js-plotly-plot .modebar-btn {
    font-family: sans-serif !important;
}

/* 왼쪽 위 undefined 제거 */
.plotly-notifier::before {
    content: "" !important;
}

.plotly-notifier {
    font-size: 0 !important;
    color: transparent !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 3. DATA LOAD
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
r_tour, r_sick, b_tour, b_sick = 0, 0, 0, 0
r_hd, p_hd, slope_hd = 0, 0, 0
r_er, p_er, slope_er = 0, 0, 0

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
# 4. PLOTLY STYLE
# ============================================================
PRETENDARD = "Pretendard Variable, Pretendard, sans-serif"
PASTEL_SEQ = ["#1E1B4B", "#FF6B4A", "#5C8AE6", "#D4A574", "#7BB785", "#C97AB5", "#8A8A8A", "#404040"]


```python
def style_fig(fig, dark=False):
    fg = "#FFFFFF" if dark else "#000000"

    fig.update_layout(
        title=dict(text=""),

        font=dict(
            family=PRETENDARD,
            color=fg,
            size=14
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        xaxis=dict(
            gridcolor="rgba(0,0,0,0.06)" if not dark else "rgba(255,255,255,0.12)",
            linecolor=fg,
            tickcolor=fg,
            title_font=dict(size=13, color=fg)
        ),

        yaxis=dict(
            gridcolor="rgba(0,0,0,0.06)" if not dark else "rgba(255,255,255,0.12)",
            linecolor=fg,
            tickcolor=fg,
            title_font=dict(size=13, color=fg)
        ),

        margin=dict(l=20, r=20, t=40, b=40),

        legend=dict(
            font=dict(
                family="Pretendard Variable, sans-serif",
                color=fg,
                size=13
            )
        ),

        title_font=dict(
            color=fg,
            size=18,
            family=PRETENDARD
        ),
    )

    return fig
```


def explainer(label, text):
    """차트 위에 두는 친절 해설 박스 (비전문가용)"""
    st.markdown(
        f"""
<div class="explainer">
  <div class="explainer-eyebrow">{label}</div>
  <p>{text}</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# 5. TOP NAV + MARQUEE
# ============================================================
st.markdown(
    """
<div class="top-nav">
  <div style="display:flex; align-items:center; gap:32px;">
    <div class="wordmark">● TOURISM DASHBOARD</div>
    <div class="nav-links">
      <a href="#overview">개요</a>
      <a href="#theme1">환율 민감도</a>
      <a href="#theme2">구성비 분석</a>
      <a href="#theme3">관광수입</a>
    </div>
  </div>
  <div class="nav-cta">
    <a class="pill-secondary" href="#sources">출처 보기</a>
    <a class="pill-primary" href="#overview">분석 시작 →</a>
  </div>
</div>
<div class="marquee">법무부 KETA · 한국관광통계 · Pearson · OLS · Lag corr · N=12 months · 2025.04 — 2026.03</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 6. HERO
# ============================================================
st.markdown(
    """
<div class="hero">
  <div class="eyebrow">DATA STORY · 외국인 입국 · 관광 데이터</div>
  <h1 class="display-xl">환율과<br/>입국 목적,<br/>그리고 관광수입.</h1>
  <p class="body-lg" style="max-width:680px;">
    2025년 4월부터 2026년 3월까지 12개월의 월별 데이터로 환율 민감도, 입국 목적 구성비,
    1인당 관광수입의 관계를 다각도로 분석함. 모든 인사이트는 실제 데이터에 근거함.
  </p>
  <div style="margin-top:40px; display:flex; gap:8px;">
    <a class="pill-primary" href="#overview">분석 보기 ↓</a>
    <a class="pill-secondary" href="#theme1">환율부터 보기</a>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 7. OVERVIEW BLOCK (cream)
# ============================================================
st.markdown('<div id="overview"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
<div class="block block-cream">
  <div class="block-inner">
    <div class="eyebrow">01 / OVERVIEW</div>
    <h2 class="display-lg">한눈에 보는<br/>12개월의 흐름.</h2>
    <p class="body" style="max-width:600px; margin-top:16px;">
      외래관광객 수, 환율, 1인당 관광수입의 평균값.
    </p>
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-eyebrow">분석 기간</div>
        <div class="metric-value">{len(df)}<span class="metric-suffix"> 개월</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-eyebrow">평균 외래관광객</div>
        <div class="metric-value">{int(df['외래관광객'].mean()/10000):,}<span class="metric-suffix"> 만명</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-eyebrow">평균 환율</div>
        <div class="metric-value">{df['환율'].mean():.0f}<span class="metric-suffix"> 원</span></div>
      </div>
      <div class="metric-card">
        <div class="metric-eyebrow">평균 1인당 수입</div>
        <div class="metric-value">${df['1인당관광수입'].mean():.0f}</div>
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow" style="margin-top:80px;">TIME SERIES</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline">외래관광객 수와 환율 추이</h3>', unsafe_allow_html=True)
explainer(
    "이 차트가 무엇을 보여주는지",
    "월별로 한국을 방문한 외래관광객 수(검정 실선, 왼쪽 축)와 원/달러 환율(주황 점선, 오른쪽 축)을 함께 그린 차트임. "
    "두 선이 비슷한 방향으로 움직이면 환율과 관광객 수에 관련이 있다는 신호임. 2025년 12월 ~ 2026년 1월 무렵 두 지표가 동반 하락하는 흐름이 관찰됨."
)

fig_overview = make_subplots(specs=[[{"secondary_y": True}]])
fig_overview.add_trace(
    go.Scatter(x=df["연월"], y=df["외래관광객"], name="외래관광객 수",
               line=dict(color="#000000", width=3), mode="lines+markers", marker=dict(size=8)),
    secondary_y=False,
)
fig_overview.add_trace(
    go.Scatter(x=df["연월"], y=df["환율"], name="환율(원/달러)",
               line=dict(color="#FF6B4A", width=3, dash="dash"), mode="lines+markers", marker=dict(size=8)),
    secondary_y=True,
)
fig_overview.update_xaxes(title_text="연월")
fig_overview.update_yaxes(title_text="외래관광객 수(명)", secondary_y=False)
fig_overview.update_yaxes(title_text="환율(원/달러)", secondary_y=True)
fig_overview.update_layout(height=460, hovermode="x unified", legend=dict(orientation="h", y=1.1))
st.plotly_chart(style_fig(fig_overview), use_container_width=True)

with st.expander("통합 SQL 보기"):
    st.code(
        """SELECT
    p.[Year/Month]                              AS year_month,
    p.[Purpose of entry]                        AS purpose,
    p.number                                    AS visits,
    t.[Foreign tourists]                        AS foreign_tourists,
    t.[exchange rate(won)]                      AS exchange_rate,
    r.[Tourism revenue per capita (dollars)]    AS revenue_per_capita
FROM monthly_permits         AS p
INNER JOIN foreign_tourists  AS t ON p.[Year/Month] = t.[Year/Month]
INNER JOIN tourism_revenue   AS r ON p.[Year/Month] = r.[Year/Month]
ORDER BY p.[Year/Month], p.[Purpose of entry];""",
        language="sql",
    )


# ============================================================
# 8. THEME 1 — LIME BLOCK
# ============================================================
st.markdown('<div id="theme1"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="block block-lime">
  <div class="block-inner">
    <div class="eyebrow">02 / THEME 01</div>
    <h2 class="display-lg">환율이 오르면<br/>누가 더 움직이나.</h2>
    <p class="subhead" style="max-width:720px;">
      관광은 환율에 민감하고, 질병치료처럼 꼭 와야 하는 방문은 환율에 둔감할 것이라는 가설을 검증함.
    </p>
    <p class="body" style="max-width:720px; margin-top:16px;">
      두 가지 지표를 함께 봄. 첫째, <b>상관계수(r)</b> — 환율이 오를 때 방문도 같이 오르는지(+) 반대로 움직이는지(−)를 −1에서 +1 사이로 나타냄.
      둘째, <b>탄력성(β)</b> — 환율이 1% 오를 때 방문 수가 몇 % 변하는지로, 값이 클수록 변화에 민감함을 의미함.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

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

st.markdown('<div class="eyebrow" style="margin-top:80px;">PEARSON CORRELATION</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline">환율과 입국 목적별 상관관계</h3>', unsafe_allow_html=True)
explainer(
    "상관계수 읽는 법",
    "막대가 오른쪽(파랑)으로 길수록 환율이 오를 때 그 목적의 방문이 함께 많아진다는 의미임. "
    "왼쪽(주황)으로 길수록 반대 방향임. 0 근처면 환율과 거의 관계없음. "
    "관광이 가장 오른쪽으로 길게 뻗어 있으면 → 원화 약세(환율 상승) 시 관광객이 늘어난다는 직관적 가설이 맞는 것임."
)

c1, c2 = st.columns([1.05, 1])
with c1:
    fig1 = px.bar(corr_df, x="상관계수(r)", y="입국목적", orientation="h",
                  color="상관계수(r)",
                  color_continuous_scale=[[0, "#FF6B4A"], [0.5, "#F5F5F5"], [1, "#1E1B4B"]],
                  range_color=[-1, 1], text="상관계수(r)")
    fig1.update_traces(textposition="outside", textfont=dict(size=13, color="#000"))
    fig1.update_layout(height=480, yaxis=dict(categoryorder="total ascending"), coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig1), use_container_width=True)
with c2:
    st.markdown('<div class="caption" style="margin-bottom:8px;">ELASTICITY β</div>', unsafe_allow_html=True)
    st.markdown('<p class="body-sm">β > 1 이면 환율보다 더 크게 반응, 0~1 이면 약하게 반응, 0 근처면 둔감, 음수면 반대 방향. 관광 β=+4.29는 매우 민감하다는 뜻임.</p>', unsafe_allow_html=True)
    fig2 = px.bar(elas_df, x="입국목적", y="탄력성(β)",
                  color="탄력성(β)",
                  color_continuous_scale=[[0, "#FF6B4A"], [0.5, "#F5F5F5"], [1, "#1E1B4B"]],
                  text="탄력성(β)")
    fig2.update_traces(textposition="outside", textfont=dict(size=12, color="#000"))
    fig2.add_hline(y=0, line_dash="dash", line_color="#000")
    fig2.update_layout(height=420, coloraxis_showscale=False, xaxis=dict(tickangle=-30))
    st.plotly_chart(style_fig(fig2), use_container_width=True)

st.markdown('<div class="eyebrow" style="margin-top:64px;">SCATTER · BY PURPOSE</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline">환율과 방문 수, 입국 목적별 산점도</h3>', unsafe_allow_html=True)
explainer(
    "산점도 읽는 법",
    "가로축은 환율, 세로축은 해당 목적의 방문 수임. 각 점이 한 달의 데이터이며 점 위 숫자는 월(月)임. "
    "빨간 점선은 OLS 회귀선으로, 두 변수의 평균적 관계 방향을 보여줌. 회귀선이 가파르게 우상향이면 환율 상승과 방문 증가가 강하게 연동됨을 의미함."
)

selected = st.multiselect("입국 목적 선택", PURPOSES, default=["관광", "질병", "사업"])
if selected:
    fig_sc = make_subplots(rows=1, cols=len(selected),
                            subplot_titles=[PURPOSE_KO[p] for p in selected])
    for i, p in enumerate(selected):
        fig_sc.add_trace(
            go.Scatter(x=df["환율"], y=df[p], mode="markers+text",
                       text=df["Year/Month"].astype(str).str[-2:] + "월",
                       textposition="top center", textfont=dict(size=10),
                       marker=dict(size=14, color="#000"), showlegend=False),
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
    fig_sc.update_layout(height=420)
    st.plotly_chart(style_fig(fig_sc), use_container_width=True)

with st.expander("SQL 보기 — 환율 민감도"):
    st.code(
        """SELECT
    p.[Purpose of entry]                       AS purpose,
    CORR(p.number, t.[exchange rate(won)])     AS pearson_r,
    AVG(p.number)                              AS avg_visits
FROM monthly_permits        AS p
INNER JOIN foreign_tourists AS t ON p.[Year/Month] = t.[Year/Month]
GROUP BY p.[Purpose of entry]
ORDER BY pearson_r;

-- 탄력성 산출용 (log-log 회귀 입력)
SELECT LN(p.number) AS log_y, LN(t.[exchange rate(won)]) AS log_x
FROM monthly_permits        AS p
INNER JOIN foreign_tourists AS t ON p.[Year/Month] = t.[Year/Month]
WHERE p.number > 0;""",
        language="sql",
    )

r_tour = corr_df.loc[corr_df["입국목적"] == "관광", "상관계수(r)"].values[0]
r_sick = corr_df.loc[corr_df["입국목적"] == "질병치료", "상관계수(r)"].values[0]
b_tour = elas_df.loc[elas_df["입국목적"] == "관광", "탄력성(β)"].values[0]
b_sick = elas_df.loc[elas_df["입국목적"] == "질병치료", "탄력성(β)"].values[0]

# ============================================================
# 9. INSIGHT BLOCK NAVY (Theme 1)
# ============================================================
st.markdown(
    f"""
<div class="block block-navy">
  <div class="block-inner">
    <div class="eyebrow">INSIGHT · THEME 01</div>
    <h2 class="display-lg">가설은<br/>데이터로 지지됨.</h2>
    <p class="body-lg" style="margin-top:24px; max-width:720px;">
      쉽게 말해, 원화가 약해져서(환율이 오르면) 외국인 입장에선 한국 여행이 저렴해짐.
      그래서 관광 목적 방문은 환율 변동에 크게 반응하지만, 질병치료처럼 꼭 와야 하는 사람들은 환율에 거의 영향받지 않음.
    </p>
    <ul style="margin-top:32px; padding-left:20px; font-size:17px; font-weight:330; line-height:1.8;">
      <li>관광 목적: r = <b>+{r_tour}</b>, β = <b>+{b_tour}</b> → 환율 1% 상승 시 방문 약 {b_tour:.1f}% 증가 추정 (매우 민감)</li>
      <li>질병치료 목적: r = <b>+{r_sick}</b>, β = <b>+{b_sick}</b> → 환율과 거의 무관 (예상대로 비탄력적)</li>
      <li>사업 목적은 환율보다 비즈니스 일정 같은 다른 요인이 더 중요한 것으로 보임</li>
      <li>다만 데이터가 12개월뿐이라 통계적 유의성(p-value)이 낮은 항목이 있음 → 추세적 시사로 한정 해석함</li>
    </ul>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 10. THEME 2 — LILAC BLOCK
# ============================================================
st.markdown('<div id="theme2"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="block block-lilac">
  <div class="block-inner">
    <div class="eyebrow">03 / THEME 02</div>
    <h2 class="display-lg">고단가 방문객이<br/>늘면 수입도 늘까.</h2>
    <p class="subhead" style="max-width:720px;">
      사업·질병치료·회의처럼 단가가 높을 것으로 추정되는 목적의 방문 비율이 1인당 관광수입을 끌어올린다는 가설을 검증함.
    </p>
    <p class="body" style="max-width:720px; margin-top:16px;">
      1인당 관광수입은 "총 관광수입 ÷ 총 외래관광객 수"로 계산되는 평균 지출액임. 사업·치료 목적은 일반 관광객보다 1인 평균 지출이 클 것으로 추정되므로,
      이런 방문객의 비율이 높은 달에 평균 지출이 더 클 것이라는 가설임.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow" style="margin-top:80px;">COMPOSITION TREND</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline">월별 입국 목적 구성비</h3>', unsafe_allow_html=True)
explainer(
    "구성비 차트 읽는 법",
    "각 월의 전체 입국허가 건수를 100%로 보았을 때 목적별 비중을 색으로 쌓은 차트임. "
    "관광(맨 아래, 진한 색)이 절대적으로 큰 비중을 차지하며, 사업·질병·회의 등은 얇은 띠로 분포함. "
    "월별로 띠의 두께가 어떻게 변하는지 보면 계절성·이벤트성 변동을 읽을 수 있음."
)

comp_long = df.melt(id_vars=["Year/Month"], value_vars=[f"{p}_비율" for p in PURPOSES],
                    var_name="입국목적", value_name="비율(%)")
comp_long["입국목적"] = comp_long["입국목적"].str.replace("_비율", "", regex=False).map(PURPOSE_KO)
fig_comp = px.area(comp_long, x="Year/Month", y="비율(%)", color="입국목적",
                    color_discrete_sequence=PASTEL_SEQ)
fig_comp.update_layout(height=460, hovermode="x unified", legend=dict(orientation="h"))
st.plotly_chart(style_fig(fig_comp), use_container_width=True)

rev_rows = []
for p in PURPOSES:
    r, pv = stats.pearsonr(df[f"{p}_비율"], df["1인당관광수입"])
    rev_rows.append({"입국목적(구성비)": PURPOSE_KO[p], "상관계수(r)": round(r, 3),
                      "p-value": round(pv, 4)})
corr_rev_df = pd.DataFrame(rev_rows).sort_values("상관계수(r)")

st.markdown('<div class="eyebrow" style="margin-top:64px;">RATIO × REVENUE PER CAPITA</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline">구성비와 1인당 관광수입의 상관</h3>', unsafe_allow_html=True)
explainer(
    "이 차트의 핵심 질문",
    "어떤 목적의 비중이 클 때 1인당 평균 지출이 늘어나는지를 본 차트임. "
    "양(+) 막대는 \"그 목적 비중↑ 일 때 1인당 수입↑\"을, 음(−) 막대는 그 반대임. "
    "가설대로라면 사업·질병·회의 막대가 양(+)이어야 하는데, 데이터는 음(−)으로 나옴 → 가설과 반대 결과임."
)

c1, c2 = st.columns([1, 1])
with c1:
    fig_rv = px.bar(corr_rev_df, x="상관계수(r)", y="입국목적(구성비)", orientation="h",
                     color="상관계수(r)",
                     color_continuous_scale=[[0, "#FF6B4A"], [0.5, "#F5F5F5"], [1, "#1E1B4B"]],
                     range_color=[-1, 1], text="상관계수(r)")
    fig_rv.update_traces(textposition="outside", textfont=dict(size=13))
    fig_rv.update_layout(height=480, yaxis=dict(categoryorder="total ascending"), coloraxis_showscale=False)
    st.plotly_chart(style_fig(fig_rv), use_container_width=True)
with c2:
    st.markdown('<p class="body-sm" style="margin-bottom:8px;">고단가 추정 비율(사업+질병+회의 합산)과 1인당 수입의 관계를 산점도로 확인함. 점 위 숫자는 연월(YYYYMM)이며 빨간 점선은 회귀선임.</p>', unsafe_allow_html=True)
    fig_hd = px.scatter(df, x="고단가추정비율", y="1인당관광수입",
                         text="Year/Month", trendline="ols",
                         labels={"고단가추정비율": "고단가 추정 비율(%)",
                                 "1인당관광수입": "1인당 관광수입($)"})
    fig_hd.update_traces(textposition="top center", marker=dict(size=14, color="#000"))
    if len(fig_hd.data) > 1:
        fig_hd.data[1].line.color = "#FF6B4A"
        fig_hd.data[1].line.dash = "dash"
        fig_hd.update_layout(height=440)
    st.plotly_chart(style_fig(fig_hd), use_container_width=True)

r_hd, p_hd = stats.pearsonr(df["고단가추정비율"], df["1인당관광수입"])
slope_hd, _, _, _, _ = stats.linregress(df["고단가추정비율"], df["1인당관광수입"])

m1, m2, m3 = st.columns(3)
m1.metric("상관계수 (r)", f"{r_hd:.3f}")
m2.metric("p-value", f"{p_hd:.4f}")
m3.metric("회귀 기울기", f"{slope_hd:.2f} $/%p")

with st.expander("SQL 보기 — 구성비 분석"):
    st.code(
        """WITH purpose_totals AS (
    SELECT [Year/Month] AS year_month, SUM(number) AS total_permits
    FROM monthly_permits GROUP BY [Year/Month]
)
SELECT
    p.[Year/Month]                                  AS year_month,
    p.[Purpose of entry]                            AS purpose,
    (p.number * 1.0 / pt.total_permits) * 100       AS ratio_pct,
    r.[Tourism revenue per capita (dollars)]        AS revenue_per_capita
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
SELECT CORR(high_value_ratio, rev) FROM agg;""",
        language="sql",
    )

top_pos = corr_rev_df.iloc[-1]
top_neg = corr_rev_df.iloc[0]

# ============================================================
# 11. INSIGHT BLOCK CORAL (Theme 2)
# ============================================================
st.markdown(
    f"""
<div class="block block-coral">
  <div class="block-inner">
    <div class="eyebrow">INSIGHT · THEME 02</div>
    <h2 class="display-lg">가설은<br/>데이터와 반대였음.</h2>
    <p class="body-lg" style="margin-top:24px; max-width:760px;">
      놀랍게도 사업·질병·회의 비율이 높은 달에 1인당 관광수입은 오히려 낮음.
      이유를 풀어보면: 관광이 폭증하는 성수기에는 외래관광객 자체가 많고, 쇼핑·면세점 매출도 함께 증가하면서 평균 지출이 올라감.
      반대로 비수기에는 사업·회의 같은 단기 출장자 비중이 상대적으로 커지지만, 이들의 평균 체류·지출은 일반 관광객의 성수기 지출보다 작음.
    </p>
    <ul style="margin-top:32px; padding-left:20px; font-size:17px; font-weight:330; line-height:1.8;">
      <li>고단가 추정 비율 vs 1인당 수입: r = <b>{r_hd:+.3f}</b> (p = {p_hd:.3f}) — 통계적으로 유의한 <b>음의 상관</b>임</li>
      <li>가장 강한 양(+)의 상관: <b>{top_pos['입국목적(구성비)']}</b> 비율 (r = {top_pos['상관계수(r)']:+.3f})</li>
      <li>가장 강한 음(−)의 상관: <b>{top_neg['입국목적(구성비)']}</b> 비율 (r = {top_neg['상관계수(r)']:+.3f})</li>
      <li>다만 단일 비율만으로 인과를 단정할 수 없음. 환율·체류기간·국적 등 다요인 영향은 데이터상 분리 확인 불가함</li>
    </ul>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 12. THEME 3 — MINT BLOCK
# ============================================================
st.markdown('<div id="theme3"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="block block-mint">
  <div class="block-inner">
    <div class="eyebrow">04 / THEME 03</div>
    <h2 class="display-lg">환율이 흔들리면<br/>1인당 수입은.</h2>
    <p class="subhead" style="max-width:720px;">
      원화 강세(환율↓) 시 외국인의 달러 기준 한국 내 지출이 작아지므로 1인당 관광수입도 낮아질 것이라는 가설임.
    </p>
    <p class="body" style="max-width:720px; margin-top:16px;">
      환율과 1인당 수입의 <b>동기(같은 달) 상관</b>과 <b>시차(Lag) 상관</b>을 함께 봄.
      시차 분석은 "환율 변화가 몇 개월 후에 관광수입에 반영되는가"를 보는 것임.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow" style="margin-top:80px;">DUAL AXIS</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline">환율과 1인당 관광수입 시계열</h3>', unsafe_allow_html=True)
explainer(
    "이 차트 읽는 법",
    "검정 실선이 환율(왼쪽 축), 주황 점선이 1인당 관광수입(오른쪽 축)임. "
    "두 선이 함께 오르내리면 \"환율↑ → 수입↑\" 관계를 의미하고, 엇갈리면 \"환율↑ → 수입↓\" 관계임. "
    "전체적으로 비슷한 방향으로 움직이지만 일부 구간(2025년 8월, 2026년 2월)에서 어긋남이 보임."
)

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
fig_t3.update_layout(height=460, hovermode="x unified", legend=dict(orientation="h", y=1.1))
st.plotly_chart(style_fig(fig_t3), use_container_width=True)

st.markdown('<div class="eyebrow" style="margin-top:64px;">SCATTER + OLS &amp; LAG ANALYSIS</div>', unsafe_allow_html=True)
st.markdown('<h3 class="headline">동기 산점도와 시차(Lag) 상관계수</h3>', unsafe_allow_html=True)
explainer(
    "두 차트 함께 읽는 법",
    "왼쪽 산점도는 같은 달의 환율-수입 관계, 오른쪽 막대는 시차별 상관계수임. "
    "오른쪽 막대에서 가로축 0은 \"같은 달\", −1은 \"환율이 1개월 먼저 변한 경우\", +1은 \"수입이 1개월 먼저 변한 경우\"임. "
    "0개월 막대가 가장 크면 환율이 즉시 반영된다는 의미이고, 1·2·3개월 막대가 더 크면 지연 효과가 있다는 뜻임."
)

c1, c2 = st.columns([1, 1])
with c1:
    fig_sc3 = px.scatter(df, x="환율", y="1인당관광수입", text="Year/Month",
                          trendline="ols",
                          labels={"환율": "환율(원/달러)", "1인당관광수입": "1인당 관광수입($)"})
    fig_sc3.update_traces(textposition="top center", marker=dict(size=14, color="#000"))
    if len(fig_sc3.data) > 1:
        fig_sc3.data[1].line.color = "#FF6B4A"
        fig_sc3.data[1].line.dash = "dash"
        fig_sc3.update_layout(height=460)
    st.plotly_chart(style_fig(fig_sc3), use_container_width=True)

with c2:
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
            lag_rows.append({"시차(개월)": lag, "상관계수(r)": round(r, 3), "표본수": len(x)})
    lag_df = pd.DataFrame(lag_rows)
    fig_lag = px.bar(lag_df, x="시차(개월)", y="상관계수(r)", text="상관계수(r)",
                     color="상관계수(r)",
                     color_continuous_scale=[[0, "#FF6B4A"], [0.5, "#F5F5F5"], [1, "#1E1B4B"]],
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

with st.expander("SQL 보기 — 환율 vs 1인당 관광수입"):
    st.code(
        """SELECT
    t.[Year/Month]                              AS year_month,
    t.[exchange rate(won)]                      AS exchange_rate,
    r.[Tourism revenue per capita (dollars)]    AS revenue_per_capita
FROM foreign_tourists       AS t
INNER JOIN tourism_revenue  AS r ON t.[Year/Month] = r.[Year/Month]
ORDER BY t.[Year/Month];

-- 시차 분석 (Lag 1~3개월)
SELECT
    t.[Year/Month] AS ym,
    t.[exchange rate(won)] AS er,
    LAG(t.[exchange rate(won)], 1) OVER (ORDER BY t.[Year/Month]) AS er_lag1,
    LAG(t.[exchange rate(won)], 2) OVER (ORDER BY t.[Year/Month]) AS er_lag2,
    LAG(t.[exchange rate(won)], 3) OVER (ORDER BY t.[Year/Month]) AS er_lag3,
    r.[Tourism revenue per capita (dollars)] AS rev
FROM foreign_tourists      AS t
INNER JOIN tourism_revenue AS r ON t.[Year/Month] = r.[Year/Month];""",
        language="sql",
    )

best_lag = lag_df.iloc[lag_df["상관계수(r)"].abs().idxmax()]
direction = "양(+)" if r_er > 0 else "음(−)"
sig_text = "통계적으로 유의함 (p<0.05)" if p_er < 0.05 else "통상 유의수준 (p<0.05)에는 미달함"

# ============================================================
# 13. INSIGHT BLOCK PINK (Theme 3)
# ============================================================
st.markdown(
    f"""
<div class="block block-pink">
  <div class="block-inner">
    <div class="eyebrow">INSIGHT · THEME 03</div>
    <h2 class="display-lg">방향성은 있지만<br/>유의성은 미달함.</h2>
    <p class="body-lg" style="margin-top:24px; max-width:760px;">
      환율이 오를수록 1인당 수입도 늘어나는 약한 양의 관계가 보이지만, 데이터가 12개월밖에 없어
      통계적으로 \"확실하다\"고 말하기는 어려움. 다만 방향성 자체는 가설(환율↓ → 수입↓)과 부합함.
    </p>
    <ul style="margin-top:32px; padding-left:20px; font-size:17px; font-weight:330; line-height:1.8;">
      <li>동기 상관: r = <b>{r_er:+.3f}</b> (p = {p_er:.3f}) → {direction}의 상관, {sig_text}</li>
      <li>회귀 기울기: <b>{slope_er:+.4f} $/원</b> → 환율 1원 상승 시 1인당 수입은 평균 약 {slope_er:.2f}달러 증가 추정</li>
      <li>시차 분석에서 절대값 최대 상관은 <b>{int(best_lag['시차(개월)'])}개월</b> 시점 (r = {best_lag['상관계수(r)']:+.3f}) — 환율 변동이 즉시 반영되는 경향이 강함</li>
      <li>표본 N=12 한계로 안정적 결론 도출은 데이터상 확인 불가함 → 추가 데이터 확보 후 재검증 필요함</li>
    </ul>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 14. FINAL TAKEAWAY (NAVY)
# ============================================================
st.markdown(
    """
<div class="block block-navy">
  <div class="block-inner">
    <div class="eyebrow">FINAL TAKEAWAY</div>
    <h2 class="display-lg">세 가설,<br/>세 가지 결론.</h2>
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:24px; margin-top:48px;">
      <div>
        <div class="caption" style="margin-bottom:8px;">THEME 01</div>
        <div class="headline" style="margin-bottom:12px;">데이터로 지지됨</div>
        <p class="body-sm">관광=환율 민감, 질병치료=환율 둔감이라는 구조가 명확히 관측됨.</p>
      </div>
      <div>
        <div class="caption" style="margin-bottom:8px;">THEME 02</div>
        <div class="headline" style="margin-bottom:12px;">가설과 반대 결과</div>
        <p class="body-sm">고단가 비율↑일수록 1인당 수입은 오히려↓ — 성수기·비수기 효과가 시사됨.</p>
      </div>
      <div>
        <div class="caption" style="margin-bottom:8px;">THEME 03</div>
        <div class="headline" style="margin-bottom:12px;">방향 부합, 유의성 미달</div>
        <p class="body-sm">N=12 한계로 안정적 결론은 데이터상 확인 불가함.</p>
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# 15. FOOTER
# ============================================================
st.markdown('<div id="sources"></div>', unsafe_allow_html=True)
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
        2025.04 – 2026.03<br/>
        N = 12 months<br/>
        Monthly granularity
      </div>
    </div>
    <div>
      <div class="caption-col">DESIGN</div>
      <div class="source-list">
        Monochrome core<br/>
        Pastel color blocks<br/>
        Pretendard typography
      </div>
    </div>
  </div>
  <div style="margin-top:64px; padding-top:24px; border-top:1px solid #EFEFEF;
              font-size:12px; letter-spacing:0.6px; text-transform:uppercase;">
    © 2026 Tourism Data Dashboard · 출처: 법무부 · 한국관광통계
  </div>
</div>
""",
    unsafe_allow_html=True,
)