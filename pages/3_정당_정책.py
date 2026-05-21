import streamlit as st
from utils.api import get_party_policy

st.set_page_config(
    page_title="정당 정책 비교 - 내 동네 후보 탐색기",
    page_icon="🏛️",
    layout="wide"
)

# ── 디자인 시스템 적용을 위한 Custom CSS ────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Noto Sans KR', 'Outfit', sans-serif;
            background-color: #f8fafc;
        }
        
        /* 헤더 스타일링 */
        .header-container {
            padding: 2.5rem 1.5rem;
            background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
            border-radius: 16px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 15px -3px rgba(71, 85, 105, 0.2);
            text-align: center;
        }
        
        .header-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -0.05em;
        }
        
        .header-subtitle {
            font-size: 1rem;
            opacity: 0.9;
            font-weight: 300;
        }
        
        /* 정책 카드 디자인 */
        .policy-card {
            background-color: white;
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.02);
            border-left: 5px solid #475569;
        }
        
        .policy-num {
            font-size: 0.85rem;
            font-weight: 700;
            color: white;
            background-color: #475569;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 0.5rem;
        }
        
        .policy-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.5rem;
        }

        /* 본문 텍스트 가시성 강제 확보 (배경 화이트 시 글자 흰색 방지) */
        .element-container div[data-testid="stMarkdownContainer"] h1,
        .element-container div[data-testid="stMarkdownContainer"] h2,
        .element-container div[data-testid="stMarkdownContainer"] h3,
        .element-container div[data-testid="stMarkdownContainer"] h4,
        .element-container div[data-testid="stMarkdownContainer"] p,
        .element-container div[data-testid="stMarkdownContainer"] li,
        .stSelectbox label,
        .stTextInput label {
            color: #1e293b !important;
        }

        /* 🚀 Streamlit Page Link 프리미엄 버튼 스타일 오버라이드 (사이드바 가시성 확보) */
        div[data-testid="stPageLink"] {
            background: linear-gradient(135deg, #1e3a8a 0%, #0f766e 100%) !important;
            border-radius: 14px !important;
            padding: 0.75rem 1.25rem !important;
            border: none !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
            transition: all 0.3s ease !important;
            text-align: center !important;
            justify-content: center !important;
            display: flex !important;
        }

        div[data-testid="stPageLink"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 15px -3px rgba(15, 118, 110, 0.3) !important;
            filter: brightness(1.1) !important;
        }

        /* 내부 텍스트 및 이모지 스타일 강제 적용 */
        div[data-testid="stPageLink"] p,
        div[data-testid="stPageLink"] span,
        div[data-testid="stPageLink"] a {
            color: #ffffff !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            text-decoration: none !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ── 헤더 렌더링 ────────────────────────
st.markdown("""
    <div class="header-container">
        <div class="header-title">🏛️ 주요 정당 정책 비교</div>
        <div class="header-subtitle">각 정당이 내세우는 10대 핵심 정책과 1:1 비교를 통해 정책 성향을 깊이 있게 비교해 보세요.</div>
    </div>
""", unsafe_allow_html=True)

# ── 공통 섹션 타이틀 렌더링 헬퍼 함수 (그라데이션 배경) ────────────────────────
def section_title(icon: str, title: str, start_color: str = "#1e293b", end_color: str = "#475569"):
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {start_color} 0%, {end_color} 100%);
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            color: white !important;
            font-weight: 700;
            font-size: 1.1rem;
            margin-top: 1.5rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="color: white !important;">{icon}</span> <span style="color: white !important;">{title}</span>
        </div>
    """, unsafe_allow_html=True)

# 데이터 추출을 위한 안전한 헬퍼 함수
def get_val(item: dict, keys: list, default: str = "정보 없음") -> str:
    for key in keys:
        if key in item and item[key] is not None:
            return str(item[key]).strip()
        if key.lower() in item and item[key.lower()] is not None:
            return str(item[key.lower()]).strip()
        if key.upper() in item and item[key.upper()] is not None:
            return str(item[key.upper()]).strip()
    return default

# 정당 색상 헬퍼 함수
def get_party_color(party_name: str) -> str:
    party_name = party_name.replace(" ", "")
    if "더불어민주당" in party_name:
        return "#004EA2"
    elif "국민의힘" in party_name:
        return "#E61E2B"
    elif "정의당" in party_name or "녹색정의당" in party_name:
        return "#FFED00"
    elif "개혁신당" in party_name:
        return "#FF6600"
    elif "조국혁신당" in party_name:
        return "#0059A6"
    elif "무소속" in party_name:
        return "#888888"
    else:
        return "#475569"

# ── 데이터 로딩 ────────────────────────
with st.spinner("정당별 10대 정책 데이터를 불러오는 중입니다..."):
    raw_policies = get_party_policy()

# 각 정당별로 데이터 가공
# API에서 정책 목록이 비어 있거나 정상 응답이 오지 않는 경우 하드코딩된 mock 데이터를 결합하여 완성도 보장
parties_data = {}
if raw_policies:
    for item in raw_policies:
        p_name = get_val(item, ["partyName", "jdName"])
        if not p_name or p_name == "정보 없음":
            continue
            
        policies = []
        for i in range(1, 11):
            title = get_val(item, [f"prmsTitle{i}", f"prmmName{i}", f"prmsName{i}"], default="")
            content = get_val(item, [f"prmsCont{i}", f"prmsArgr{i}"], default="")
            realm = get_val(item, [f"prmsRealmName{i}"], default="공통 분야")
            
            if title and title != "정보 없음":
                # HTML 태그 제거 및 줄바꿈 정리
                clean_content = content.replace("<br>", "\n").replace("<br/>", "\n")
                policies.append({
                    "ord": i,
                    "realm": realm,
                    "title": title,
                    "content": clean_content
                })
        
        if policies:
            parties_data[p_name] = policies

# 등록된 정당 목록 추출
party_list = sorted(list(parties_data.keys()))

if not party_list:
    st.info("ℹ️ 현재 선관위 DB에 등록된 정당 정책 데이터가 없습니다. 지방선거 기간 정당 정책 공시 일정에 따라 순차 배포됩니다.")
else:
    # 탭 메뉴 정의
    tab1, tab2 = st.tabs(["🏛️ 단일 정당 정책 전체 보기", "⚖️ 두 정당 정책 1:1 비교"])
    
    # ────────────────────────────────────────────────────────
    # 탭 1: 단일 정당 정책 전체 보기
    # ────────────────────────────────────────────────────────
    with tab1:
        section_title("📢", "정당 선택", "#1e293b", "#475569")
        selected_party = st.selectbox("정책을 조회할 정당을 선택하세요.", options=party_list, key="single_party_select")
        
        p_color = get_party_color(selected_party)
        st.markdown(f"""
            <div style="padding: 0.5rem 1rem; border-radius: 8px; border-left: 6px solid {p_color}; background-color: #f1f5f9; margin-bottom: 1.5rem;">
                <h4 style="margin:0; color: #1e293b;"><b>{selected_party}</b>의 10대 핵심 정책 공약 목록입니다.</h4>
            </div>
        """, unsafe_allow_html=True)
        
        policies = parties_data[selected_party]
        for p in policies:
            st.markdown(f"""
                <div class="policy-card" style="border-left-color: {p_color};">
                    <span class="policy-num" style="background-color: {p_color}; color: {'#ffffff' if p_color != '#FFED00' else '#000000'};">
                        우선순위 {p['ord']}순위 | {p['realm']}
                    </span>
                    <div class="policy-title">{p['title']}</div>
                    <div style="font-size: 0.95rem; color: #334155; line-height: 1.7; white-space: pre-line;">
                        {p['content']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.write("")

    # ────────────────────────────────────────────────────────
    # 탭 2: 두 정당 정책 1:1 비교
    # ────────────────────────────────────────────────────────
    with tab2:
        section_title("⚖️", "비교할 두 정당 선택", "#1e293b", "#475569")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            party_a = st.selectbox(
                "정당 A를 선택하세요.",
                options=party_list,
                index=0,
                key="compare_party_a"
            )
        
        with col_p2:
            default_b_index = 1 if len(party_list) > 1 else 0
            party_b = st.selectbox(
                "정당 B를 선택하세요.",
                options=party_list,
                index=default_b_index,
                key="compare_party_b"
            )
            
        if party_a == party_b:
            st.warning("⚠️ 서로 다른 정당을 선택해야 올바른 비교 분석이 가능합니다.")
        else:
            st.write("---")
            st.write(f"#### 🔎 **{party_a}** vs **{party_b}** 정책 번호순 비교")
            
            p_color_a = get_party_color(party_a)
            p_color_b = get_party_color(party_b)
            
            policies_a = {p["ord"]: p for p in parties_data[party_a]}
            policies_b = {p["ord"]: p for p in parties_data[party_b]}
            
            # 1순위부터 10순위까지 루프
            for order in range(1, 11):
                col_card_a, col_card_b = st.columns(2)
                
                # 정당 A의 해당 순위 정책 출력
                with col_card_a:
                    if order in policies_a:
                        p_a = policies_a[order]
                        st.markdown(f"""
                            <div class="policy-card" style="border-left-color: {p_color_a}; height: 100%;">
                                <span class="policy-num" style="background-color: {p_color_a}; color: {'#ffffff' if p_color_a != '#FFED00' else '#000000'};">
                                    {party_a} | 우선순위 {order}순위
                                </span>
                                <div style="font-size: 0.8rem; color: #64748b; font-weight: 600; margin-bottom: 0.25rem;">📂 분야: {p_a['realm']}</div>
                                <div class="policy-title">{p_a['title']}</div>
                                <div style="font-size: 0.9rem; color: #334155; line-height: 1.6; white-space: pre-line;">
                                    {p_a['content']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="policy-card" style="border-left-color: #cbd5e1; height: 100%; color: #94a3b8;">
                                📭 {party_a}의 {order}순위 정책이 등록되지 않았습니다.
                            </div>
                        """, unsafe_allow_html=True)
                
                # 정당 B의 해당 순위 정책 출력
                with col_card_b:
                    if order in policies_b:
                        p_b = policies_b[order]
                        st.markdown(f"""
                            <div class="policy-card" style="border-left-color: {p_color_b}; height: 100%;">
                                <span class="policy-num" style="background-color: {p_color_b}; color: {'#ffffff' if p_color_b != '#FFED00' else '#000000'};">
                                    {party_b} | 우선순위 {order}순위
                                </span>
                                <div style="font-size: 0.8rem; color: #64748b; font-weight: 600; margin-bottom: 0.25rem;">📂 분야: {p_b['realm']}</div>
                                <div class="policy-title">{p_b['title']}</div>
                                <div style="font-size: 0.9rem; color: #334155; line-height: 1.6; white-space: pre-line;">
                                    {p_b['content']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="policy-card" style="border-left-color: #cbd5e1; height: 100%; color: #94a3b8;">
                                📭 {party_b}의 {order}순위 정책이 등록되지 않았습니다.
                            </div>
                        """, unsafe_allow_html=True)
                st.write("")
