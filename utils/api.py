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


# ── 선관위 API 공통 호출 ──────────────────────────
def nec_get(endpoint: str, params: dict, service_key: str) -> dict:
    params["serviceKey"] = service_key
    params["resultType"] = "json"
    url = f"{NEC_BASE_URL}/{endpoint}"
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API 오류: {e}")
        return {}


# ── 후보자 통합검색 ───────────────────────────────
def search_candidate(name: str) -> list:
    data = nec_get(
        "VolCandInfoInqireService2/getCandidateInfoInqire",
        {"sgId": SG_ID, "candName": name, "numOfRows": 20},
        service_key=NEC_CAND_SEARCH_KEY
    )
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
    items = data.get("response", {}).get("body", {}).get("items", {})
    if not items:
        return []
    item = items.get("item", [])
    return item if isinstance(item, list) else [item]
