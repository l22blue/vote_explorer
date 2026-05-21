import streamlit as st
from utils.api import get_candidates_by_district, get_pledges, solar_summarize

st.set_page_config(
    page_title="내 동네 후보 - 내 동네 후보 탐색기",
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
    </style>
""", unsafe_allow_html=True)

# ── 헤더 렌더링 ────────────────────────
st.markdown("""
    <div class="header-container">
        <div class="header-title">🏘️ 내 동네 후보자 & AI 공약 비교</div>
        <div class="header-subtitle">내가 거주하는 자치구별 출마 후보와 선거 공약을 AI 요약으로 한눈에 살펴보세요.</div>
    </div>
""", unsafe_allow_html=True)

# ── 서울시 25개 자치구 목록 정의 ────────────────────────
seoul_districts = [
    "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", 
    "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", 
    "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"
]

# ── 선거종류 매핑 정의 ────────────────────────
election_types = {
    "🏛️ 서울특별시장 선거": {"code": "3", "needs_district": False},
    "🏘️ 자치구의 구청장 선거": {"code": "4", "needs_district": True},
    "🏢 서울특별시의회의원 선거 (시의원)": {"code": "5", "needs_district": True},
    "🏡 구·시·군의회의원 선거 (구의원)": {"code": "6", "needs_district": True}
}

# ── 상단 필터 셀렉션 ────────────────────────
st.write("### 📍 지역구 및 선거종류 선택")
col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    selected_district = st.selectbox(
        "우리 동네(자치구)를 선택하세요.",
        options=seoul_districts,
        index=22  # 기본값 종로구
    )

with col_sel2:
    selected_election_label = st.selectbox(
        "조회할 선거 종류를 선택하세요.",
        options=list(election_types.keys()),
        index=1  # 기본값 구청장 선거
    )

# 선택된 설정값 파싱
el_info = election_types[selected_election_label]
sg_type_code = el_info["code"]
is_district_election = el_info["needs_district"]

# 서울특별시장 선거일 경우 구 이름은 제외하고 조회
wiw_name_query = selected_district if is_district_election else ""

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
                        👤 <b>나이:</b> {age1}세 &nbsp;|&nbsp; 🎓 <b>학력:</b> {edu1}<br>
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
                            👤 <b>나이:</b> {age2}세 &nbsp;|&nbsp; 🎓 <b>학력:</b> {edu2}<br>
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
