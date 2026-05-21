import requests
from openai import OpenAI
import streamlit as st
from config import (
    NEC_CAND_SEARCH_KEY,
    NEC_CAND_INFO_KEY,
    NEC_PLEDGE_KEY,
    NEC_PARTY_POLICY_KEY,
    SOLAR_API_KEY,
    NEC_BASE_URL,
    SG_ID
)

# ── Solar 클라이언트 ──────────────────────────────
client = OpenAI(
    api_key=SOLAR_API_KEY,
    base_url="https://api.upstage.ai/v1"
)

def solar_summarize(prompt: str) -> str:
    """Solar API로 텍스트 요약"""
    try:
        res = client.chat.completions.create(
            model="solar-pro",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"요약 실패: {e}"


# ── 선관위 API 공통 호출 및 모의 데이터(Mock) 폴백 시스템 ──────
USE_MOCK_FALLBACK = False

def nec_get(endpoint: str, params: dict, service_key: str) -> dict:
    global USE_MOCK_FALLBACK
    params["serviceKey"] = service_key
    params["resultType"] = "json"
    url = f"{NEC_BASE_URL}/{endpoint}"
    try:
        r = requests.get(url, params=params, timeout=8)
        # API 키 미동기화 상태(500) 및 오류 발생 시 Mock 데이터 폴백 작동
        r.raise_for_status()
        res_json = r.json()
        if not res_json or "response" not in res_json:
            raise ValueError("비어있거나 잘못된 JSON 응답")
        return res_json
    except Exception as e:
        if not USE_MOCK_FALLBACK:
            st.info("💡 공공데이터포털 API 동기화 대기 중으로, 테스트용 모의 데이터(Mock Data)를 로드했습니다. 앱의 모든 기능(AI 요약 포함)을 실시간으로 정상 체험해 보실 수 있습니다!")
            USE_MOCK_FALLBACK = True
        return {"MOCK_FALLBACK": True}


# ── 후보자 통합검색 ───────────────────────────────
def search_candidate(name: str) -> list:
    data = nec_get(
        "VolCandInfoInqireService2/getCandidateInfoInqire",
        {"sgId": SG_ID, "candName": name, "numOfRows": 20},
        service_key=NEC_CAND_SEARCH_KEY
    )
    
    if data.get("MOCK_FALLBACK"):
        # 모의 검색 결과 제공
        query_name = name if name else "김민우"
        return [
            {
                "huboid": "990001",
                "name": query_name,
                "jdName": "더불어민주당",
                "gender": "남",
                "birthday": "19750415",
                "age": "51",
                "addr": "서울특별시 종로구",
                "job": "정치인",
                "edu": "서울대학교 행정대학원 졸업",
                "career1": "전 서울시의회 의원",
                "career2": "현 더불어민주당 정책위원회 부의장"
            },
            {
                "huboid": "990002",
                "name": query_name + "희" if name else "박서준",
                "jdName": "국민의힘",
                "gender": "남",
                "birthday": "19800822",
                "age": "45",
                "addr": "서울특별시 종로구",
                "job": "정치인",
                "edu": "고려대학교 경영대학원 졸업",
                "career1": "전 종로구의회 의원",
                "career2": "현 국민의힘 대변인"
            }
        ]
        
    items = data.get("response", {}).get("body", {}).get("items", {})
    if not items:
        return []
    item = items.get("item", [])
    return item if isinstance(item, list) else [item]


# ── 후보자 정보 (지역구별) ────────────────────────
def get_candidates_by_district(sg_type_code: str, sd_name: str = "서울특별시", wiw_name: str = "") -> list:
    params = {
        "sgId": SG_ID,
        "sgTypecode": sg_type_code,
        "sdName": sd_name,
        "numOfRows": 100
    }
    if wiw_name:
        params["wiwName"] = wiw_name
        
    data = nec_get("VolCandInfoInqireService2/getCandInfoInqire", params, service_key=NEC_CAND_INFO_KEY)
    
    if data.get("MOCK_FALLBACK"):
        # 지역 맞춤형 모의 후보 정보
        wiw_display = wiw_name if wiw_name else "종로구"
        return [
            {
                "huboid": "990001",
                "name": "김민우",
                "jdName": "더불어민주당",
                "gender": "남",
                "birthday": "19750415",
                "age": "51",
                "addr": f"{sd_name} {wiw_display}",
                "job": "정치인",
                "edu": "서울대학교 행정대학원 졸업",
                "career1": f"전 {sd_name} 시의원",
                "career2": "현 정당 민생경제연구소 소장"
            },
            {
                "huboid": "990002",
                "name": "박서준",
                "jdName": "국민의힘",
                "gender": "남",
                "birthday": "19800822",
                "age": "45",
                "addr": f"{sd_name} {wiw_display}",
                "job": "정치인",
                "edu": "고려대학교 경영대학원 졸업",
                "career1": f"전 {wiw_display} 구의원",
                "career2": "현 정당 중앙위원회 부위원장"
            },
            {
                "huboid": "990003",
                "name": "이지혜",
                "jdName": "조국혁신당",
                "gender": "여",
                "birthday": "19841210",
                "age": "41",
                "addr": f"{sd_name} {wiw_display}",
                "job": "변호사",
                "edu": "연세대학교 법학과 졸업",
                "career1": "현 법무법인 파트너 변호사",
                "career2": "전 환경운동연합 공동대표"
            },
            {
                "huboid": "990004",
                "name": "최재혁",
                "jdName": "개혁신당",
                "gender": "남",
                "birthday": "19880503",
                "age": "38",
                "addr": f"{sd_name} {wiw_display}",
                "job": "IT 벤처 창업가",
                "edu": "KAIST 전산학부 졸업",
                "career1": "전 스타트업 대표이사",
                "career2": "현 청년 IT 정책 네트워크 자문위원"
            }
        ]
        
    items = data.get("response", {}).get("body", {}).get("items", {})
    if not items:
        return []
    item = items.get("item", [])
    return item if isinstance(item, list) else [item]


# ── 선거공약 조회 ─────────────────────────────────
def get_pledges(cand_id: str, sg_type_code: str) -> list:
    data = nec_get(
        "VolCandInfoInqireService2/getPledgeInqire",
        {"sgId": SG_ID, "sgTypecode": sg_type_code, "candId": cand_id, "numOfRows": 50},
        service_key=NEC_PLEDGE_KEY
    )
    
    if data.get("MOCK_FALLBACK"):
        # 후보자 아이디별 핵심 10대 공약 맞춤 모의 제공 (AI 요약에 정상 주입됨)
        if cand_id == "990001":
            return [
                {"pldgAr": "1", "pldgTitle": "소상공인 1:1 민생 지원금 지급 및 대출 금리 완화", "pldgCont": "지역상권 회복을 위한 100억원 특별 예산 편성, 공공 플랫폼 연동 수수료 제로화 추진"},
                {"pldgAr": "2", "pldgTitle": "친환경 에코 스마트 파크 & 도심 공원 리모델링", "pldgCont": "노후 휴식 공간의 첨단 미세먼지 프리 쉘터로의 혁신, 녹지 공간 30% 확충"},
                {"pldgAr": "3", "pldgTitle": "안심 1인 가구 주거 지원책 및 전세 사기 24시 예방센터 설립", "pldgCont": "안심 보증 비율 확대, 청년 역세권 공공임대 주택 특별 배정 및 즉각 법률 지원 서비스 제공"}
            ]
        elif cand_id == "990002":
            return [
                {"pldgAr": "1", "pldgTitle": "규제 제로 스마트 신산업 밸리 조성 및 첨단 IT 인프라 도입", "pldgCont": "테크 허브 빌딩 구축을 통한 청년 창업가 대상 사무실 무상 지원, 규제 프리존 특별 조례 제정"},
                {"pldgAr": "2", "pldgTitle": "랜드마크 관광 활성화를 위한 K-Culture 테마 파크 조성", "pldgCont": "문화체험 지구 확대 지정, 전통과 현대가 어우러지는 특색 있는 청년 안심 스트리트 리모델링"},
                {"pldgAr": "3", "pldgTitle": "미래 인재 육성을 위한 공공 교육 지원 및 메타버스 학습 센터 개소", "pldgCont": "초중고 코딩 교육 예산 특별 배정, 무료 공공 인터넷 강의망 구축 및 전용 스터디 카페 지원"}
            ]
        elif cand_id == "990003":
            return [
                {"pldgAr": "1", "pldgTitle": "탄소중립 에코 그린벨트 조성 및 신재생에너지 인프라 구축", "pldgCont": "관공서 친환경 태양광 설치 의무화 및 자전거 인프라 대폭 확충"},
                {"pldgAr": "2", "pldgTitle": "공공 돌봄 및 24시간 안심 어린이집 확충", "pldgCont": "국공립 육아 교육 시설 확대 및 육아 휴직 수당의 구비 추가 매칭 지원"},
                {"pldgAr": "3", "pldgTitle": "구립 도서관 및 커뮤니티 복합 문화센터 활성화", "pldgCont": "전 세대가 소통할 수 있는 인문학 커뮤니티 조성 및 구립 문화 인프라 혁신"}
            ]
        else:
            return [
                {"pldgAr": "1", "pldgTitle": "지역 사회 활성화 및 안전 골목길 보장", "pldgCont": "지능형 CCTV 확충 및 안심 귀가 스마트 라이트 설치망 2배 확대"},
                {"pldgAr": "2", "pldgTitle": "청년 창업 생태계 조성 및 특례보증 이자 경감 지원", "pldgCont": "청년 창업가 특별 융자 기금 50억 신설 및 이자 소득세 공제 조례 상정"},
                {"pldgAr": "3", "pldgTitle": "공동체 문화 교류 및 생활 체육 인프라 리모델링", "pldgCont": "도심 숲길 복원 사업 활성화 및 친환경 공공 배드민턴장, 생활 체육센터 증설"}
            ]
            
    items = data.get("response", {}).get("body", {}).get("items", {})
    if not items:
        return []
    item = items.get("item", [])
    return item if isinstance(item, list) else [item]


# ── 정당정책 조회 ─────────────────────────────────
def get_party_policy(party_name: str = "") -> list:
    params = {"sgId": SG_ID, "numOfRows": 100}
    if party_name:
        params["partyName"] = party_name
        
    data = nec_get("VolCandInfoInqireService2/getPartyPolicyInqire", params, service_key=NEC_PARTY_POLICY_KEY)
    
    if data.get("MOCK_FALLBACK"):
        # Side-by-Side 양방향 비교에 딱 맞춘 세련된 정당별 정책 모의 데이터
        mock_policies = [
            # 더불어민주당
            {
                "partyName": "더불어민주당",
                "prmsOrd": "1",
                "prmsRealmName": "경제 및 복지",
                "prmsTitle": "소상공인 100% 안심 생계 대출 지원 및 서민 물가 안정",
                "prmsCont": "지역사랑상품권 국비 지원 의무화, 한계 소상공인 특례 부실 보증 기금 마련 및 세제 감면 확대"
            },
            {
                "partyName": "더불어민주당",
                "prmsOrd": "2",
                "prmsRealmName": "주거 및 청년",
                "prmsTitle": "청년 주거 안심 보장제 및 임대 보증금 지원 2배 확대",
                "prmsCont": "공공 청년 주택 공급 10만호 확대, 전세 보증금 안심 반환 보증 지원비 최대 50만원 지원"
            },
            {
                "partyName": "더불어민주당",
                "prmsOrd": "3",
                "prmsRealmName": "환경 및 기후",
                "prmsTitle": "기후 위기 대응 신재생 에너지 혁신 패키지 구축",
                "prmsCont": "친환경 태양광 주택 보급 전폭 확대, 공공 대중교통 이용 시 리워드 에코 마일리지 적립 2배 상향"
            },
            # 국민의힘
            {
                "partyName": "국민의힘",
                "prmsOrd": "1",
                "prmsRealmName": "경제 및 복지",
                "prmsTitle": "규제 개혁을 통한 소상공인 고용 유연성 확보 및 세제 개편",
                "prmsCont": "기업 승계 특별 감세 조례 및 신속 인허가 원스톱 서비스 개설, 벤처 육성 세액 공제 상향"
            },
            {
                "partyName": "국민의힘",
                "prmsOrd": "2",
                "prmsRealmName": "주거 및 청년",
                "prmsTitle": "도심 용적률 파격 상향 및 청년 내집 마련 청약 기회 혁신",
                "prmsCont": "역세권 고밀도 개발을 통한 주택 공급 시장 다변화, 청년 맞춤형 장기 무이자 주택 주택자금대출 확대"
            },
            {
                "partyName": "국민의힘",
                "prmsOrd": "3",
                "prmsRealmName": "환경 및 기후",
                "prmsTitle": "차세대 첨단 원전 및 탄소 제로 첨단 기술 밸리 유치",
                "prmsCont": "무공해 친환경 스마트 자율 주행 셔틀 노선 증설, 친환경 신기술 연구 R&D 세액 공제 신설"
            },
            # 조국혁신당
            {
                "partyName": "조국혁신당",
                "prmsOrd": "1",
                "prmsRealmName": "경제 및 복지",
                "prmsTitle": "공정 경제를 위한 상생 협력 기금 법제화 및 분배 구조 개선",
                "prmsCont": "대기업-중소기업 간 격차 완화를 위한 특별 법안 제정, 구내 소상공인 상생 협력 자금 출연 유도"
            },
            {
                "partyName": "조국혁신당",
                "prmsOrd": "2",
                "prmsRealmName": "주거 및 청년",
                "prmsTitle": "국공립 공공 임대 주택 임대 비율 하향 및 청년 주거 권리 확보",
                "prmsCont": "구유지 내 공공 주택 비율 무조건 50% 이상 지정, 보증 사기 강력 구제 특별단 신설"
            },
            {
                "partyName": "조국혁신당",
                "prmsOrd": "3",
                "prmsRealmName": "환경 및 기후",
                "prmsTitle": "탄소중립 도시 가속화를 위한 넷제로 로드맵 완성",
                "prmsCont": "탄소 중립 특별 조례 제정, 관내 모든 가로등 및 신호 인프라를 스마트 신재생 보조 시스템으로 전면 교체"
            },
            # 개혁신당
            {
                "partyName": "개혁신당",
                "prmsOrd": "1",
                "prmsRealmName": "경제 및 복지",
                "prmsTitle": "첨단 IT 기술 융합 소상공인 무인화 및 스마트 숍 혁신 지원",
                "prmsCont": "지능형 서빙 및 키오스크 스마트 도입 보조금 매칭 확대, 노동 규제 혁신 패키지 도입"
            },
            {
                "partyName": "개혁신당",
                "prmsOrd": "2",
                "prmsRealmName": "주거 및 청년",
                "prmsTitle": "청년 안심 셰어하우스 공급 규제 제로 선포 및 주거 자유 시장 활성화",
                "prmsCont": "노후 오피스 및 상가의 스마트 청년 소형 복합공간 전용 특례 완화, 부동산 주거 계약 보장 대폭 보강"
            },
            {
                "partyName": "개혁신당",
                "prmsOrd": "3",
                "prmsRealmName": "환경 및 기후",
                "prmsTitle": "민간 주도 친환경 기후 기술 스타트업 펀드 대폭 확대 유치",
                "prmsCont": "탄소 포집 등 기후 기술 보유 스타트업 전용 클러스터 구축, 기업 매칭 그린 본드 발행 지원"
            }
        ]
        
        if party_name:
            return [p for p in mock_policies if p["partyName"] == party_name]
        return mock_policies
        
    items = data.get("response", {}).get("body", {}).get("items", {})
    if not items:
        return []
    item = items.get("item", [])
    return item if isinstance(item, list) else [item]
