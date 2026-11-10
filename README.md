# CANSLIM TERMINAL

일지([빠방홀러 4화](https://bbabangholer.tistory.com/16))와 보유 판단에서 드러난 규칙 구멍을 닫은 버전입니다.

라이브: https://onilanalysis-zj8cjtqwm759xakknesv3o.streamlit.app

## 배포

`main`의 `app.py`가 바뀌면 Streamlit Cloud가 자동으로 다시 빌드합니다.
`.streamlit/config.toml`(이 저장소는 루트 `config.toml`), `requirements.txt`는 그대로입니다.

사이드바 **시세·재무 캐시 새로고침**을 누르면 1시간 TTL 캐시를 비우고 숫자를 다시 받습니다.

## v14.44

IBD 의존도를 낮추기 위해 수치 계산에 방어적 가드를 넣었습니다.  
`safe_div` / `safe_ret` / `robust_rs_proxy`로 0나누기·NaN·빠진 데이터를 막고, sticky_bar 오류는 경고로 바꾼 뒤 계속 동작합니다.  
앱 자체 계산(RS·A/D·점수)이 우선이며, IBD Checkup/Pulse는 참고용으로만 남기는 안내를 보여 줍니다.

## v14.43

11/6 30종목 비교를 반영했습니다.  
**Quality Score** (Comp 근사)와 **Timing / Buy Checklist Score** (기존 점수)를 분리합니다.  
Quality는 시장 상태와 베이스·피벗 준비도 페널티를 거의 주지 않아 우량주가 낮게 나오는 문제를 줄입니다.  
A/D는 13주 업볼륨/다운볼륨 비율로 대리합니다.  
앱은 시장 국면·RS·매수 타이밍 확인에 쓸 만하고, 우량주 선별은 IBD Checkup과 함께 보세요.

## v14.42

SPCX처럼 상장일이 짧으면 일봉은 성공인데도 "시세를 가져오지 못했습니다"가 나왔다. 120일 미만을 실패로 지웠기 때문이다. 30일 이상이면 화면을 연다.
