import streamlit as st
from utils.api import search_candidate

st.set_page_config(
    page_title="후보자 검색 - 내 동네 후보 탐색기",
    page_icon="🔍",
    layout="wide"
)

# ── 디자인 시스템 적용을 위한 Custom CSS ────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
        
        /* 폰트 및 배경 설정 */
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Noto Sans KR', 'Outfit', sans-serif;
            background-color: #f8fafc;
        }
        
        /* 헤더 스타일링 */
        .header-container {
            padding: 2.5rem 1.5rem;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            border-radius: 16px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2);
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
        
        /* 카드 형태 UI 스타일 */
        .candidate-card {
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .candidate-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
        
        /* 정당 배지 공통 스타일 */
        .party-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.75rem;
        }
    </style>
""", unsafe_allow_html=True)

# ── 헤더 렌더링 ────────────────────────
st.markdown("""
    <div class="header-container">
        <div class="header-title">🔍 후보자 통합 검색</div>
        <div class="header-subtitle">2026 서울 지방선거 후보자를 이름으로 빠르게 조회해 보세요.</div>
    </div>
""", unsafe_allow_html=True)

# ── 검색 영역 ────────────────────────
st.write("### 👤 후보자 이름 입력")
col1, col2 = st.columns([4, 1])

with col1:
    search_name = st.text_input(
        "검색할 후보자의 이름을 입력하세요.",
        placeholder="예: 홍길동 (이름을 적고 Enter 또는 검색을 누르세요)",
        label_visibility="collapsed"
    )

with col2:
    search_btn = st.button("🔍 검색", use_container_width=True)

# 데이터 추출을 위한 안전한 헬퍼 함수
def get_val(item: dict, keys: list, default: str = "정보 없음") -> str:
    for key in keys:
        if key in item and item[key] is not None:
            return str(item[key]).strip()
        # 대소문자 매칭 시도
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
        return "#475569"  # 기본 다크 그레이

# ── 검색 처리 및 출력 ────────────────────────
if search_name or search_btn:
    if not search_name.strip():
        st.warning("⚠️ 검색할 이름을 한 글자 이상 입력해 주세요.")
    else:
        with st.spinner("선관위 DB에서 후보자 정보를 가져오는 중입니다..."):
            results = search_candidate(search_name.strip())
            
        if not results:
            st.info(f"😕 '{search_name}' 후보자에 대한 검색 결과가 없습니다. 이름을 다시 확인해 주세요.")
        else:
            st.success(f"🎉 총 {len(results)}명의 후보자가 검색되었습니다.")
            st.write("---")
            
            for item in results:
                # API 응답 데이터 파싱
                name = get_val(item, ["name", "candName"])
                hanja_name = get_val(item, ["hanjaName"])
                party = get_val(item, ["jdName", "partyName"])
                giho = get_val(item, ["giho", "symbolNum"], default="")
                sido = get_val(item, ["sdName", "sidoName"])
                wiw = get_val(item, ["wiwName", "sggName"])
                gender = get_val(item, ["gender", "sex"])
                age = get_val(item, ["age"])
                birthday = get_val(item, ["birthday"])
                job = get_val(item, ["job"])
                edu = get_val(item, ["edu"])
                career1 = get_val(item, ["career1"])
                career2 = get_val(item, ["career2"])
                
                # 생년월일 포맷팅 (YYYYMMDD -> YYYY.MM.DD)
                if len(birthday) == 8:
                    birthday_formatted = f"{birthday[:4]}. {birthday[4:6]}. {birthday[6:]}"
                else:
                    birthday_formatted = birthday
                
                # 카드 색상 결정
                party_color = get_party_color(party)
                text_color = "#ffffff" if party_color != "#FFED00" else "#000000"
                
                # HTML Card 디자인 렌더링
                st.markdown(f"""
                    <div class="candidate-card">
                        <div class="party-badge" style="background-color: {party_color}; color: {text_color};">
                            {f"기호 {giho}번 | " if giho else ""}{party}
                        </div>
                        <h4 style="margin: 0 0 0.5rem 0; font-size: 1.4rem; font-weight: 700; color: #1e293b;">
                            {name} <span style="font-size: 1rem; font-weight: 400; color: #64748b;">({hanja_name})</span>
                        </h4>
                        <div style="font-size: 0.95rem; color: #475569; line-height: 1.6; margin-bottom: 0.5rem;">
                            📍 <b>지역구:</b> {sido} {wiw} &nbsp;|&nbsp; 
                            🎂 <b>나이(생일):</b> {age}세 ({birthday_formatted}) &nbsp;|&nbsp; 
                            👫 <b>성별:</b> {gender}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 상세 정보 Expander
                with st.expander(f"🔍 {name} 후보 상세 이력 보기"):
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.markdown(f"**💼 직업**: {job}")
                        st.markdown(f"**🎓 학력**: {edu}")
                    with col_info2:
                        st.markdown(f"**🏆 경력 1**: {career1}")
                        st.markdown(f"**🏆 경력 2**: {career2}")
                
                st.write("")  # 간격 띄우기
