# 🗳️ 내 동네 후보 탐색기

2026 서울 지방선거 후보자 정보 탐색 웹앱

## 시작하기

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. API 키 설정
`config.py` 파일에 키 입력:
```python
NEC_API_KEY = "공공데이터포털_인증키"
SOLAR_API_KEY = "업스테이지_API키"
```

### 3. 실행
```bash
streamlit run app.py
```

## 폴더 구조
```
vote_explorer/
├── app.py                  # 메인 홈 화면
├── config.py               # API 키 설정
├── requirements.txt
├── utils/
│   └── api.py              # 선관위 API + Solar 호출
└── pages/
    ├── 1_후보자_검색.py     # 이름으로 후보 검색
    ├── 2_내동네_후보.py     # 지역구별 후보 & 공약
    └── 3_정당_정책.py      # 정당별 정책 비교
```

## 사용한 API
- 중앙선거관리위원회 후보자 정보 (공공데이터포털)
- 중앙선거관리위원회 선거공약 정보
- 중앙선거관리위원회 정당정책 정보
- 중앙선거관리위원회 후보자 통합검색
- Upstage Solar API (공약 AI 요약)
