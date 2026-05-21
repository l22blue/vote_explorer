import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 5개 API 키 로드
NEC_CAND_SEARCH_KEY = os.getenv("NEC_CAND_SEARCH_KEY", "여기에_후보자통합검색_API키")
NEC_CAND_INFO_KEY = os.getenv("NEC_CAND_INFO_KEY", "여기에_후보자정보조회_API키")
NEC_PLEDGE_KEY = os.getenv("NEC_PLEDGE_KEY", "여기에_선거공약조회_API키")
NEC_PARTY_POLICY_KEY = os.getenv("NEC_PARTY_POLICY_KEY", "여기에_정당정책조회_API키")
SOLAR_API_KEY = os.getenv("SOLAR_API_KEY", "여기에_업스테이지_API키")

# 선관위 API 기본 URL
NEC_BASE_URL = "http://apis.data.go.kr/9760000"

# 2026 지방선거 ID (선관위 기준)
SG_ID = "20260603"          # 선거 ID
SG_TYPE_CODE = "3"          # 시·도지사선거 기본값
