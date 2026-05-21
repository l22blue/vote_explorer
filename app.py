import streamlit as st

st.set_page_config(
    page_title="내 동네 후보 탐색기",
    page_icon="🗳️",
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
        
        /* 히어로 섹션 */
        .hero-section {
            background: linear-gradient(135deg, #1e3a8a 0%, #0f766e 100%);
            border-radius: 24px;
            padding: 4rem 2rem;
            text-align: center;
            color: white;
            margin-bottom: 3rem;
            box-shadow: 0 20px 25px -5px rgba(15, 118, 110, 0.15);
        }
        
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            letter-spacing: -0.03em;
            text-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
            opacity: 0.95;
            font-weight: 300;
            max-width: 700px;
            margin: 0 auto;
            line-height: 1.6;
        }
        
        /* 카드 디자인 */
        .nav-card {
            background: white;
            border-radius: 20px;
            padding: 2.5rem 2rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1rem;
        }
        
        .nav-icon {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            display: inline-block;
            transition: transform 0.3s ease;
        }
        
        .nav-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
            border-color: #3b82f6;
        }
        
        .nav-card:hover .nav-icon {
            transform: scale(1.15) rotate(5deg);
        }
        
        .nav-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.75rem;
        }
        
        .nav-desc {
            font-size: 0.95rem;
            color: #475569;
            line-height: 1.6;
            min-height: 4.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🗳️ 내 동네 후보 탐색기</div>
        <div class="hero-subtitle">
            2026 서울 지방선거 후보자의 상세 프로필과 핵심 공약을 간편하게 탐색해 보세요.<br>
            Upstage의 강력한 Solar AI를 활용하여, 복잡한 공약도 3줄 요약 보고서로 빠르게 파악할 수 있습니다.
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🔍</div>
            <div class="nav-title">후보자 통합 검색</div>
            <div class="nav-desc">이름 입력 한 번으로 서울시에 출마한 모든 후보자의 정당, 나이, 학력, 경력을 빠르고 쉽게 검색합니다.</div>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_후보자_검색.py", label="👉 후보자 검색하기", use_container_width=True)

with col2:
    st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🏘️</div>
            <div class="nav-title">내 동네 후보 & 공약</div>
            <div class="nav-desc">내가 거주하는 자치구의 출마 후보자 명단을 확인하고, 복잡한 공약들을 AI 요약 분석을 통해 비교해 보세요.</div>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_내동네_후보.py", label="👉 내 동네 후보 확인하기", use_container_width=True)

with col3:
    st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🏛️</div>
            <div class="nav-title">정당별 정책 비교</div>
            <div class="nav-desc">선거에 참여하는 정당의 10대 주요 정책을 단일 조회 및 1:1 대조 방식으로 비교하여 최선의 선택을 내려보세요.</div>
        </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_정당_정책.py", label="👉 정당 정책 비교하기", use_container_width=True)

