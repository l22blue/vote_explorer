import streamlit as st
from utils.api import get_candidates_by_district, get_pledges, solar_summarize

st.set_page_config(
    page_title="제9회 서울 지방선거 후보 - 서울 지방선거 & 역대 후보 탐색기",
    page_icon="🏘️",
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
            background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
            border-radius: 16px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 15px -3px rgba(20, 184, 166, 0.2);
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
        
        /* 후보 격자 레이아웃 카드 */
        .grid-card {
            background-color: white;
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
            transition: all 0.2s ease;
        }
        
        .grid-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.08);
        }
        
        .party-tag {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
        }
        
        /* AI 요약 로딩 및 결과 보드 */
        .summary-box {
            background-color: #f0fdfa;
            border-left: 5px solid #0f766e;
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            box-shadow: inset 0 2px 4px 0 rgba(0,0,0,0.02);
        }
        
        .summary-title {
            color: #0f766e;
            font-weight: 700;
            font-size: 1.15rem;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
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

        /* 📝 일반 버튼 premium styling 및 글자색 강제 흰색 지정 */
        /* 📝 일반 버튼 premium styling 및 글자색 강제 흰색 지정 */
        button, 
        button:hover, 
        button:active, 
        button:focus,
        .stButton > button,
        .stButton > button:hover,
        .stButton > button:active,
        .stButton > button:focus,
        div[data-testid="stButton"] button,
        div[data-testid="stButton"] button:hover,
        div[data-testid="stButton"] button:active,
        div[data-testid="stButton"] button:focus {
            background: #1e293b !important;
            background-color: #1e293b !important;
            background-image: none !important;
            color: #ffffff !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
        }

        /* 버튼 내부의 모든 텍스트/p/span 요소를 흰색으로 강제 지정 (높은 specificity) */
        button *, 
        button *:hover, 
        button *:active, 
        button *:focus,
        .stButton > button *,
        .stButton > button *:hover,
        .stButton > button *:active,
        .stButton > button *:focus,
        .element-container div[data-testid="stMarkdownContainer"] button p,
        .element-container div[data-testid="stMarkdownContainer"] button span,
        .stButton button p,
        .stButton button span,
        .stButton button div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stButton"] button p,
        div[data-testid="stButton"] button div[data-testid="stMarkdownContainer"] p,
        button p,
        button span {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ── 헤더 렌더링 ────────────────────────
st.markdown("""
    <div class="header-container">
        <div class="header-title">🏘️ 제9회 서울 지방선거 후보 & AI 공약 비교</div>
        <div class="header-subtitle">어제 치러진 제9회 전국동시지방선거 서울특별시장 및 각 자치구별 출마 후보와 선거 공약을 AI 요약으로 살펴보세요.</div>
    </div>
""", unsafe_allow_html=True)

# ── 서울시 25개 자치구 목록 정의 ────────────────────────
# ── 서울시 선거구 및 관할 구역 매핑 데이터 로드 ────────────────────────
import json
import os

@st.cache_data
def get_seoul_districts_map():
    try:
        # parent directory is workspace, then utils/seoul_districts_2026.json
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils", "seoul_districts_2026.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        st.error(f"선거구 맵 로딩 중 오류 발생: {e}")
    return {}

seoul_districts_map = get_seoul_districts_map()

# ── 서울시 25개 자치구 목록 정의 ────────────────────────
seoul_districts = list(seoul_districts_map.keys()) if seoul_districts_map else [
    "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", 
    "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", 
    "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"
]

# ── 선거종류 매핑 정의 ────────────────────────
election_types = {
    "🏛️ 서울특별시장 선거": {"code": "3", "level": "city"},
    "🏘️ 자치구의 구청장 선거": {"code": "4", "level": "gu"},
    "🏢 서울특별시의회의원 선거 (시의원)": {"code": "5", "level": "sido_district"},
    "👥 자치구의회의원 선거 (구의원)": {"code": "6", "level": "gugun_district"}
}

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

# ── 상단 필터 셀렉션 ────────────────────────
section_title("📍", "선거종류 및 지역구 선택", "#0f766e", "#14b8a6")

selected_election_label = st.selectbox(
    "1. 조회할 선거 종류를 선택하세요.",
    options=list(election_types.keys()),
    index=1  # 기본값 구청장 선거
)

# 선택된 설정값 파싱
el_info = election_types[selected_election_label]
sg_type_code = el_info["code"]
level = el_info["level"]

col_sel1, col_sel2 = st.columns(2)

selected_district = "서울특별시"
selected_dong = ""
wiw_name_query = ""

if level == "city":
    with col_sel1:
        st.selectbox("2. 자치구 선택", options=["서울 전체 (선택 필요 없음)"], disabled=True)
    with col_sel2:
        st.selectbox("3. 행정동 선택", options=["서울 전체 (선택 필요 없음)"], disabled=True)
elif level == "gu":
    with col_sel1:
        selected_district = st.selectbox(
            "2. 자치구(구청장 선거구)를 선택하세요.",
            options=seoul_districts,
            index=seoul_districts.index("종로구") if "종로구" in seoul_districts else 0
        )
    with col_sel2:
        st.selectbox("3. 행정동 선택", options=["구 전체 (선택 필요 없음)"], disabled=True)
    wiw_name_query = selected_district
else:
    # 시의원, 구의원 선거 (동 선택 필요)
    with col_sel1:
        selected_district = st.selectbox(
            "2. 자치구를 선택하세요.",
            options=seoul_districts,
            index=seoul_districts.index("종로구") if "종로구" in seoul_districts else 0
        )
    
    # 해당 구의 모든 동 목록 구하기
    gu_data = seoul_districts_map.get(selected_district, [])
    all_dongs = []
    for item in gu_data:
        all_dongs.extend(item.get("dongs", []))
    all_dongs = sorted(list(set(all_dongs)))
    
    with col_sel2:
        selected_dong = st.selectbox(
            "3. 살고 계신 행정동을 선택하세요.",
            options=all_dongs
        )
        
    # 선택된 동에 해당하는 선거구 찾기
    resolved_district_name = ""
    for item in gu_data:
        if selected_dong in item.get("dongs", []):
            if level == "sido_district":
                resolved_district_name = item.get("sido_district", "")
            else:
                resolved_district_name = item.get("gugun_district", "")
            break
            
    if resolved_district_name:
        wiw_name_query = f"{selected_district}{resolved_district_name}"
        st.info(f"✨ 선택하신 **{selected_district} {selected_dong}**은(는) **{resolved_district_name}** 관할구역입니다. (선거구명: `{wiw_name_query}`)")
    else:
        st.error("선거구 매핑을 찾을 수 없습니다. 데이터를 확인해 주세요.")

# ── 데이터 로딩 ────────────────────────
with st.spinner("해당 지역구의 후보자 명단을 가져오는 중입니다..."):
    candidates = get_candidates_by_district(
        sg_type_code=sg_type_code,
        sd_name="서울특별시",
        wiw_name=wiw_name_query
    )

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

if not candidates:
    st.info(f"ℹ️ 선택하신 지역구({selected_district}) 및 선거종류에 등록된 후보자 정보가 현재 없습니다.")
else:
    st.success(f"🔍 총 {len(candidates)}명의 후보자가 발견되었습니다.")
    
    # 후보자 리스트 격자 레이아웃 구성 (2열)
    for index in range(0, len(candidates), 2):
        col_cand1, col_cand2 = st.columns(2)
        
        # 1번째 후보 카드 출력 (왼쪽)
        with col_cand1:
            item1 = candidates[index]
            name1 = get_val(item1, ["name", "candName"])
            giho1 = get_val(item1, ["giho", "symbolNum"], default="")
            party1 = get_val(item1, ["jdName", "partyName"])
            huboid1 = get_val(item1, ["huboid", "candId"])
            wiw1 = get_val(item1, ["wiwName", "sggName"])
            age1 = get_val(item1, ["age"])
            job1 = get_val(item1, ["job"])
            edu1 = get_val(item1, ["edu"])
            
            p_color1 = get_party_color(party1)
            t_color1 = "#ffffff" if p_color1 != "#FFED00" else "#000000"
            
            st.markdown(f"""
                <div class="grid-card">
                    <span class="party-tag" style="background-color: {p_color1}; color: {t_color1};">
                        {f"기호 {giho1}번 | " if giho1 else ""}{party1}
                    </span>
                    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.4rem; font-weight: 700; color: #0f172a;">
                        {name1} <span style="font-weight: 400; font-size: 1rem; color: #64748b;">({wiw1})</span>
                    </h3>
                    <div style="font-size: 0.9rem; color: #475569; line-height: 1.6; margin-bottom: 1rem;">
                        👤 <b>나이:</b> {age1}세<br>
                        🎓 <b>학력:</b> {edu1}<br>
                        💼 <b>직업:</b> {job1}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # AI 요약 버튼
            if st.button(f"📝 {name1} 후보 공약 AI 요약", key=f"btn_sum_{huboid1}_{index}"):
                with st.spinner(f"Solar AI가 {name1} 후보의 공약을 분석하여 요약 보고서를 작성하는 중..."):
                    # 공약 목록 조회
                    pledge_list = get_pledges(huboid1, sg_type_code)
                    
                    if not pledge_list:
                        st.warning(f"⚠️ {name1} 후보의 등록된 상세 선거 공약 데이터가 현재 선관위 DB에 없습니다.")
                    else:
                        # 공약 텍스트 조립
                        pledge_text = ""
                        for idx, pledge in enumerate(pledge_list, 1):
                            # 여러 포맷의 공약 필드 추출 시도
                            for k in range(1, 11):
                                title = get_val(pledge, [f"pldgTitle{k}"], default="")
                                content = get_val(pledge, [f"pldgArgr{k}"], default="")
                                if title and title != "정보 없음":
                                    pledge_text += f"\n[공약 {k}] {title}\n"
                                    if content and content != "정보 없음":
                                        pledge_text += f"내용: {content}\n"
                        
                        if not pledge_text.strip():
                            # 통째로 대표 공약 필드가 있는 경우 처리 (예: pldgTitle, pldgArgr)
                            for pledge in pledge_list:
                                title = get_val(pledge, ["pldgTitle"], default="")
                                content = get_val(pledge, ["pldgArgr"], default="")
                                if title and title != "정보 없음":
                                    pledge_text += f"\n[공약] {title}\n내용: {content}\n"
                        
                        if not pledge_text.strip():
                            st.warning(f"⚠️ {name1} 후보의 공약 텍스트를 구성하지 못했습니다. 상세 공약 문서가 준비되지 않았을 수 있습니다.")
                        else:
                            # Solar Prompt 요청
                            prompt = f"""
                            아래는 2026 서울 지방선거 후보자의 공식 공약 정보입니다.
                            이 공약을 분석하여 유권자가 30초 만에 쉽게 파악할 수 있도록 친절하고 핵심적인 요약 보고서를 작성해 주세요.
                            
                            [요약 규칙]
                            1. 전체 공약을 아우르는 **3대 핵심 공약 요약**을 굵은 글씨와 글머리 기호(bullet points)를 사용하여 명확하게 요약해 주세요.
                            2. 각 핵심 공약별로 **구체적인 실행 계획 및 기대효과**를 1-2문장으로 쉽게 설명해 주세요.
                            3. 친절하고 가독성이 뛰어난 한국어 어조를 사용하고, 불필요한 서론은 생략하고 바로 요약 결과를 보여주세요.
                            
                            후보자: {name1} ({party1})
                            선거구: {wiw1}
                            
                            공약 정보:
                            {pledge_text}
                            """
                            summary_res = solar_summarize(prompt)
                            
                            # 요약 결과 출력
                            st.markdown(f"""
                                <div class="summary-box">
                                    <div class="summary-title">✨ Upstage Solar AI 분석 보고서</div>
                                    <div style="font-size: 0.95rem; color: #1f2937; line-height: 1.7; white-space: pre-line;">
                                        {summary_res}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

        # 2번째 후보 카드 출력 (오른쪽 - 인덱스가 유효한 경우)
        if index + 1 < len(candidates):
            with col_cand2:
                item2 = candidates[index + 1]
                name2 = get_val(item2, ["name", "candName"])
                giho2 = get_val(item2, ["giho", "symbolNum"], default="")
                party2 = get_val(item2, ["jdName", "partyName"])
                huboid2 = get_val(item2, ["huboid", "candId"])
                wiw2 = get_val(item2, ["wiwName", "sggName"])
                age2 = get_val(item2, ["age"])
                job2 = get_val(item2, ["job"])
                edu2 = get_val(item2, ["edu"])
                
                p_color2 = get_party_color(party2)
                t_color2 = "#ffffff" if p_color2 != "#FFED00" else "#000000"
                
                st.markdown(f"""
                    <div class="grid-card">
                        <span class="party-tag" style="background-color: {p_color2}; color: {t_color2};">
                            {f"기호 {giho2}번 | " if giho2 else ""}{party2}
                        </span>
                        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.4rem; font-weight: 700; color: #0f172a;">
                            {name2} <span style="font-weight: 400; font-size: 1rem; color: #64748b;">({wiw2})</span>
                        </h3>
                        <div style="font-size: 0.9rem; color: #475569; line-height: 1.6; margin-bottom: 1rem;">
                            👤 <b>나이:</b> {age2}세<br>
                            🎓 <b>학력:</b> {edu2}<br>
                            💼 <b>직업:</b> {job2}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # AI 요약 버튼
                if st.button(f"📝 {name2} 후보 공약 AI 요약", key=f"btn_sum_{huboid2}_{index+1}"):
                    with st.spinner(f"Solar AI가 {name2} 후보의 공약을 분석하여 요약 보고서를 작성하는 중..."):
                        # 공약 목록 조회
                        pledge_list2 = get_pledges(huboid2, sg_type_code)
                        
                        if not pledge_list2:
                            st.warning(f"⚠️ {name2} 후보의 등록된 상세 선거 공약 데이터가 현재 선관위 DB에 없습니다.")
                        else:
                            # 공약 텍스트 조립
                            pledge_text2 = ""
                            for idx, pledge in enumerate(pledge_list2, 1):
                                for k in range(1, 11):
                                    title = get_val(pledge, [f"pldgTitle{k}"], default="")
                                    content = get_val(pledge, [f"pldgArgr{k}"], default="")
                                    if title and title != "정보 없음":
                                        pledge_text2 += f"\n[공약 {k}] {title}\n"
                                        if content and content != "정보 없음":
                                            pledge_text2 += f"내용: {content}\n"
                            
                            if not pledge_text2.strip():
                                for pledge in pledge_list2:
                                    title = get_val(pledge, ["pldgTitle"], default="")
                                    content = get_val(pledge, ["pldgArgr"], default="")
                                    if title and title != "정보 없음":
                                        pledge_text2 += f"\n[공약] {title}\n내용: {content}\n"
                            
                            if not pledge_text2.strip():
                                st.warning(f"⚠️ {name2} 후보의 공약 텍스트를 구성하지 못했습니다. 상세 공약 문서가 준비되지 않았을 수 있습니다.")
                            else:
                                # Solar Prompt 요청
                                prompt2 = f"""
                                아래는 2026 서울 지방선거 후보자의 공식 공약 정보입니다.
                                이 공약을 분석하여 유권자가 30초 만에 쉽게 파악할 수 있도록 친절하고 핵심적인 요약 보고서를 작성해 주세요.
                                
                                [요약 규칙]
                                1. 전체 공약을 아우르는 **3대 핵심 공약 요약**을 굵은 글씨와 글머리 기호(bullet points)를 사용하여 명확하게 요약해 주세요.
                                2. 각 핵심 공약별로 **구체적인 실행 계획 및 기대효과**를 1-2문장으로 쉽게 설명해 주세요.
                                3. 친절하고 가독성이 뛰어난 한국어 어조를 사용하고, 불필요한 서론은 생략하고 바로 요약 결과를 보여주세요.
                                
                                후보자: {name2} ({party2})
                                선거구: {wiw2}
                                
                                공약 정보:
                                {pledge_text2}
                                """
                                summary_res2 = solar_summarize(prompt2)
                                
                                # 요약 결과 출력
                                st.markdown(f"""
                                    <div class="summary-box">
                                        <div class="summary-title">✨ Upstage Solar AI 분석 보고서</div>
                                        <div style="font-size: 0.95rem; color: #1f2937; line-height: 1.7; white-space: pre-line;">
                                            {summary_res2}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
        st.write("---")

# ── 버튼 스타일 최종 override 강제 주입 (DOM 최하단에서 오버라이딩 확보) ────────────────
st.markdown("""
    <style>
        button, 
        .stButton button, 
        div[data-testid="stButton"] button {
            background: #1e293b !important;
            background-color: #1e293b !important;
            background-image: none !important;
            color: #ffffff !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2) !important;
        }
        button:hover, 
        .stButton button:hover, 
        div[data-testid="stButton"] button:hover {
            background: #0f172a !important;
            background-color: #0f172a !important;
            color: #ffffff !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4) !important;
        }
        button *, 
        .stButton button *, 
        div[data-testid="stButton"] button *,
        .element-container div[data-testid="stMarkdownContainer"] button p,
        .element-container div[data-testid="stMarkdownContainer"] button span {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
    </style>
""", unsafe_allow_html=True)

