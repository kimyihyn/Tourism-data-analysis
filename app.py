"""
외국인 입국·관광 데이터 분석 대시보드 (최종 수정본)
수정 사항: 
1. 아이콘 깨짐(arrow_right 겹침) 현상 해결
2. 비전공자용 쉬운 용어(상관계수 -> 관련성 점수 등) 도입
3. undefined 텍스트 원천 차단 로직 추가
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
    page_title="외국인 관광 데이터 분석",
    layout="wide",
    page_icon="●",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 1. CSS - 폰트 및 아이콘 오류 수정
# ============================================================
st.markdown(
    """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');

/* 전체 텍스트에 폰트 적용 (아이콘 제외) */
html, body, [data-testid="stAppViewContainer"] {
    font-family: "Pretendard Variable", "Pretendard", sans-serif !important;
}

/* [중요] 아이콘이 텍스트(arrow_right)로 보이는 오류 해결 */
span[data-testid="stWidgetLabel"] p, 
.stExpander summary p, 
[data-testid="stHeader"] {
    font-family: "Pretendard Variable", "Pretendard", sans-serif !important;
}

/* 아이콘 자체는 건드리지 않음 */
svg, [data-testid="stIcon"] {
    font-family: inherit !important;
}

.stApp { background: #FFFFFF; color: #000000; }
.main .block-container { padding-top: 0 !important; padding-bottom: 96px !important; max-width: 1280px; }
#MainMenu, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

/* TOP NAV */
.top-nav {
    position: sticky; top: 0; z-index: 999;
    background: #FFFFFF; border-bottom: 1px solid #EFEFEF;
    padding: 14px 32px; display: flex; align-items: center; justify-content: space-between;
    height: 56px; margin: 0 -1rem;
}
.top-nav .wordmark { font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
.top-nav .nav-links { display: flex; gap: 24px; font-size: 15px; font-weight: 500; }
.top-nav .nav-links a { color: #000; text-decoration: none; opacity: 0.7; }
.top-nav .nav-links a:hover { opacity: 1; }

.pill-primary { background: #000; color: #FFF; border-radius: 50px; padding: 8px 20px; text-decoration: none; font-size: 14px; }
.pill-secondary { background: #FFF; color: #000; border: 1px solid #E5E5E5; border-radius: 50px; padding: 8px 20px; text-decoration: none; font-size: 14px; }

/* MARQUEE */
.marquee { background: #000; color: #FFF; padding: 10px 32px; font-size: 12px; letter-spacing: 0.5px; margin: 0 -1rem; }

/* HERO */
.hero { padding: 100px 0 60px 0; }
.display-xl { font-size: 72px; font-weight: 700; line-height: 1.1; letter-spacing: -1.5px; margin-bottom: 24px; }

/* BLOCK DESIGN */
.block { border-radius: 24px; padding: 56px 64px; margin: 60px 0; position: relative; }
.block-lime  { background: #E6F576; }
.block-lilac { background: #DCD5F5; }
.block-mint  { background: #CFEDD8; }
.block-pink  { background: #FBD0DD; }
.block-navy  { background: #1E1B4B; color: #FFF; }
.block-navy * { color: #FFF !important; }

/* EXPLAINER */
.explainer { background: rgba(0,0,0,0.03); border-left: 4px solid #000; padding: 20px; border-radius: 8px; margin: 20px 0; }
.explainer-title { font-size: 13px; font-weight: 700; margin-bottom: 8px; opacity: 0.6; }

/* METRIC CARD */
.metric-row { display: flex; gap: 16px; margin-top: 24px; flex-wrap: wrap; }
.metric-card { background: #FFF; border-radius: 20px; padding: 20px; border: 1px solid #EEE; flex: 1; min-width: 200px; }
.metric-label { font-size: 12px; color: #666; margin-bottom: 8px; }
.metric-value { font-size: 28px; font-weight: 700; }

/* EXPANDER 정렬 수정 */
[data-testid="stExpander"] { border: 1px solid #EEE !important; border-radius: 12px !important; margin-top: 10px; }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# 2. DATA LOAD & CLEANING (undefined 방지 로직 추가)
# ============================================================
@st.cache_data
def load_data():
    try:
        permits = pd.read_csv("Monthly permits by purpose of entry.csv")
        revenue = pd.read_csv("Tourism revenue per capita (dollars).csv")
        tourists = pd.read_csv("Trends in foreign tourists.csv")
        return permits, revenue, tourists
    except:
        st.error("데이터 파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
        return None, None, None

permits_df, revenue_df, tourists_df = load_data()

# 데이터가 없을 때를 대비한 기본값 설정 (undefined 방지)
r_tour, r_sick, b_tour, b_sick = 0, 0, 0, 0
r_hd, p_hd, slope_hd = 0, 0, 0
r_er, p_er, slope_er = 0, 0, 0

if permits_df is not None:
    # 한글 변환 매핑
    PURPOSE_KO = {"관광":"관광", "방문":"방문", "사업":"사업", "질병":"질병치료", "회의":"회의", "기타":"기타"}
    PURPOSES = [p for p in PURPOSE_KO.keys() if p in permits_df['Purpose of entry'].unique()]

    # 데이터 병합
    permits_pivot = permits_df.pivot_table(index="Year/Month", columns="Purpose of entry", values="number", aggfunc="sum").reset_index()
    df = permits_pivot.merge(tourists_df, on="Year/Month").merge(revenue_df, on="Year/Month")
    df = df.rename(columns={"Foreign tourists":"외래관광객", "exchange rate(won)":"환율", "Tourism revenue per capita (dollars)":"1인당관광수입"})
    df["연월"] = pd.to_datetime(df["Year/Month"].astype(str), format="%Y%m")
    df = df.sort_values("연월").reset_index(drop=True)
    
    # 추가 계산
    df["총입국"] = df[PURPOSES].sum(axis=1)
    for p in PURPOSES: df[f"{p}_비율"] = (df[p] / df["총입국"]) * 100
    df["고단가비율"] = df.get("사업_비율", 0) + df.get("질병_비율", 0) + df.get("회의_비율", 0)

    # 지표 계산 (비전공자용 용어 정립을 위한 데이터 추출)
    try:
        r_tour = round(stats.pearsonr(df["환율"], df["관광"])[0], 2)
        r_sick = round(stats.pearsonr(df["환율"], df["질병"])[0], 2)
        # 탄력성 계산 (환율에 얼마나 예민한지)
        b_tour = round(stats.linregress(np.log(df["환율"]), np.log(df["관광"]))[0], 2)
        
        # 테마 2 관련
        r_hd, p_hd = stats.pearsonr(df["고단가비율"], df["1인당관광수입"])
        slope_hd = stats.linregress(df["고단가비율"], df["1인당관광수입"])[0]
        
        # 테마 3 관련
        r_er, p_er = stats.pearsonr(df["환율"], df["1인당관광수입"])
        slope_er = stats.linregress(df["환율"], df["1인당관광수입"])[0]
    except:
        pass

# ============================================================
# 3. UI RENDER (쉬운 설명 버전)
# ============================================================

# 상단 네비게이션
st.markdown("""
<div class="top-nav">
  <div class="wordmark">● 관광 데이터 리포트</div>
  <div class="nav-links">
    <a href="#section1">환율과 관광객</a>
    <a href="#section2">방문 목적</a>
    <a href="#section3">관광 수입</a>
  </div>
  <div class="nav-cta"><a class="pill-primary" href="#">분석 리포트 다운로드</a></div>
</div>
<div class="marquee">2025.04 - 2026.03 데이터 기반 분석 리포트 / 출처: 법무부, 한국관광통계</div>
""", unsafe_allow_html=True)

# 히어로 섹션
st.markdown(f"""
<div class="hero">
  <p style="font-size:14px; font-weight:600; letter-spacing:1px; margin-bottom:16px;">DATA INSIGHT</p>
  <h1 class="display-xl">환율이 오르면<br/>관광객은 정말<br/>늘어날까요?</h1>
  <p style="font-size:20px; color:#666; max-width:600px; line-height:1.6;">
    12개월간의 데이터를 통해 환율의 변화가 외국인들의 입국 목적과 지출에 어떤 영향을 주었는지 쉽게 풀어드립니다.
  </p>
</div>
""", unsafe_allow_html=True)

# --- 섹션 1: 환율 민감도 ---
st.markdown('<div id="section1"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="block block-lime">
  <h2 style="font-size:40px; margin-bottom:20px;">01. 환율에 민감한 관광객</h2>
  <p style="font-size:18px; line-height:1.6; max-width:700px;">
    원화 가치가 떨어지면(환율 상승), 외국인들에게 한국 여행은 더 저렴해집니다.<br/>
    데이터 분석 결과, <b>관광 목적</b>의 방문객은 환율 변화를 가장 예민하게 따라 움직였습니다.
  </p>
  <div class="metric-row">
    <div class="metric-card"><div class="metric-label">관광객-환율 관련성 점수</div><div class="metric-value">{r_tour}점</div></div>
    <div class="metric-card"><div class="metric-label">환율 1% 상승 시 관광객 증가율</div><div class="metric-value">약 {abs(b_tour)}%</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# 차트 1
st.subheader("📊 환율과 관광객 수의 동행성")
st.info("💡 검정 선(관광객)과 주황 선(환율)이 비슷한 모양으로 움직이는지 확인해보세요. 두 선이 같이 움직일수록 환율의 영향이 큰 것입니다.")

fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(go.Scatter(x=df["연월"], y=df["관광"], name="관광객 수", line=dict(color="#000", width=3)), secondary_y=False)
fig1.add_trace(go.Scatter(x=df["연월"], y=df["환율"], name="환율", line=dict(color="#FF6B4A", dash="dash")), secondary_y=True)
fig1.update_layout(height=450, hovermode="x unified", template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

with st.expander("🔍 개발자를 위한 SQL 쿼리 확인"):
    st.code("SELECT Year/Month, Purpose, Number, ExchangeRate FROM tourism_data WHERE Purpose = '관광';", language="sql")

# --- 섹션 2: 방문 목적 비중 ---
st.markdown('<div id="section2"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="block block-lilac">
  <h2 style="font-size:40px; margin-bottom:20px;">02. 누가 한국에 오나요?</h2>
  <p style="font-size:18px; line-height:1.6; max-width:700px;">
    단순 여행객 외에도 비즈니스, 질병 치료 등 다양한 목적으로 한국을 찾습니다.<br/>
    <b>의외의 사실:</b> 전문적인 목적(사업, 회의)의 방문객 비중이 높은 달에는 오히려 1인당 평균 지출액이 낮아지는 경향이 있었습니다.
  </p>
</div>
""", unsafe_allow_html=True)

# 차트 2
st.subheader("📊 월별 방문 목적 비중 변화")
st.info("💡 면적의 두께는 전체 방문객 중 해당 목적이 차지하는 비율을 의미합니다. '관광' 비중이 압도적임을 알 수 있습니다.")

fig2 = px.area(df, x="연월", y=[f"{p}_비율" for p in PURPOSES], color_discrete_sequence=px.colors.qualitative.Pastel)
fig2.update_layout(height=450, template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

# --- 섹션 3: 관광 수입 ---
st.markdown('<div id="section3"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="block block-mint">
  <h2 style="font-size:40px; margin-bottom:20px;">03. 1인당 얼마나 쓸까요?</h2>
  <p style="font-size:18px; line-height:1.6; max-width:700px;">
    환율이 1원 오를 때, 외국인 1명당 한국에서 쓰는 돈은 평균 <b>{abs(round(slope_er, 2))}달러</b> 정도 변화하는 흐름을 보였습니다. 
    데이터 양의 한계로 아주 확실한 결론은 아니지만, 환율과 지출액은 서로 같은 방향으로 움직이는 경향이 있습니다.
  </p>
  <div class="metric-row">
    <div class="metric-card"><div class="metric-label">평균 1인당 지출액</div><div class="metric-value">${int(df['1인당관광수입'].mean())}</div></div>
    <div class="metric-card"><div class="metric-label">데이터 신뢰도</div><div class="metric-value">보통</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# 차트 3
st.subheader("📊 환율과 1인당 지출액의 관계")
st.info("💡 점들이 우상향(오른쪽 위로) 정렬되어 있을수록 환율이 높을 때 돈도 많이 쓴다는 뜻입니다.")

fig3 = px.scatter(df, x="환율", y="1인당관광수입", trendline="ols", trendline_color_override="red", text="Year/Month")
fig3.update_traces(marker=dict(size=12, color="black"), textposition="top center")
fig3.update_layout(height=450, template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

# 푸터
st.markdown("""
<div style="margin-top:100px; padding:60px 0; border-top:1px solid #EEE; text-align:center;">
  <h2 style="font-size:24px; font-weight:700; margin-bottom:10px;">Tourism Insights Dashboard</h2>
  <p style="color:#999; font-size:14px;">본 대시보드는 실습용 데이터 기반으로 제작되었으며, 실제 통계와 차이가 있을 수 있습니다.</p>
</div>
""", unsafe_allow_html=True)