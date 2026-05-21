import os
import streamlit as st
from dotenv import load_dotenv

# .env 파일 로드 (로컬 개발용)
load_dotenv()

def get_config_value(key, default_val):
    # Streamlit Cloud의 st.secrets에서 먼저 조회
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    # 로컬 .env 또는 시스템 환경 변수 조회
    return os.getenv(key, default_val)

# 5개 API 키 로드
NEC_CAND_SEARCH_KEY = get_config_value("NEC_CAND_SEARCH_KEY", "여기에_후보자통합검색_API키")
NEC_CAND_INFO_KEY = get_config_value("NEC_CAND_INFO_KEY", "여기에_후보자정보조회_API키")
NEC_PLEDGE_KEY = get_config_value("NEC_PLEDGE_KEY", "여기에_선거공약조회_API키")
NEC_PARTY_POLICY_KEY = get_config_value("NEC_PARTY_POLICY_KEY", "여기에_정당정책조회_API키")
SOLAR_API_KEY = get_config_value("SOLAR_API_KEY", "여기에_업스테이지_API키")

# 선관위 API 기본 URL
NEC_BASE_URL = "http://apis.data.go.kr/9760000"

# 2026 지방선거 ID (선관위 기준)
SG_ID = "20260603"          # 선거 ID
SG_TYPE_CODE = "3"          # 시·도지사선거 기본값
