# CANSLIM TERMINAL v13.1

일지([빠방홀러 4화](https://bbabangholer.tistory.com/16))와 보유 판단에서 드러난 규칙 구멍을 닫은 버전입니다.

라이브: https://onilanalysis-zj8cjtqwm759xakknesv3o.streamlit.app

## 배포

`main`의 `app.py`가 바뀌면 Streamlit Cloud가 자동으로 다시 빌드합니다.
`.streamlit/config.toml`(이 저장소는 루트 `config.toml`), `requirements.txt`는 그대로입니다.

사이드바 **시세·재무 캐시 새로고침**을 누르면 1시간 TTL 캐시를 비우고 숫자를 다시 받습니다.

## v13.1에서 고친 것

- **8주 보유 규칙** — 3주 내 +20%가 한 번 성립하면 **돌파 +56일까지 유지**하고, 만료 뒤에만 일반 익절로 전환합니다.
- **돌파일 탐색** — 베이스 저점 이후 **첫 피봇 종가 돌파**를 찾습니다.
- **가짜돌파** — 돌파 거래량 1.4배 미만이면 결함 + 상단바 `가짜돌파 위험`.
- **핸들 없는 돌파** — 기본값을 가짜돌파 쪽으로, 체크리스트에 핸들·우측 거래량.
- **C 25% 엄격** — +20~25%는 미달 경고.
- **+15% 준비** — my투자에서 +15~20%면 “오늘 20% 계획을 적는다”.
- **피벗 전 진입** — 예외 표시. 연속 예외는 시스템이 아님.
- **컨센·실적·수급 숫자** — yfinance 목표가, forward EPS, earnings_dates, totalAssets(AUM 대용), shortRatio, 52주 밴드.
- **일지 종목 불러오기** — WT·NTAP·HNGE 시드. 이후 시세·전략은 자동 갱신.
- **수동 메모 칸** — AUM 순유입·GAAP/Adj·방어선.

## 자동으로 갱신되는 숫자

시세·피봇·이평·RS·거래량 배수·8주 규칙·매도압력·CANSLIM 점수,
yfinance 컨센 목표가·선행PER·기관보유%·다음 실적일,
totalAssets·공매도 일수·52주 고저.

## 자동이 안 되는 숫자

- 자산운용사 **AUM 순유입·fee rate** — 월간 IR. `totalAssets`는 대용.
- GAAP vs Adjusted EPS — 종목마다 yfinance 정의가 다름.
- 국내 수급 — Streamlit Cloud에서 KRX가 막힐 수 있음.
- 증권사 목표가 당일 변경 — yfinance 반영 지연.

방법: 분석보강 STREET가 비면 IR을 메모에 남기고, my투자 메모에 방어선(WT 20.0 / NTAP 181 / HNGE 80.8)과 20% 목표(WT 26.06)를 적어둡니다.
