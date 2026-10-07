# University Maker

대학 4학년의 1년을 보내며 다양한 활동과 이벤트를 경험하고,  
캐릭터의 스탯에 따라 서로 다른 엔딩을 확인하는 **Python 콘솔 육성 시뮬레이션 게임**입니다.

[IBM x RedHat] AI Transformation - AX Academy에서 진행한 팀 프로젝트로 개발했습니다.

## 주요 기능

- 캐릭터 생성 및 저장/불러오기
- 월별 일정 선택 및 진행
- 재력, 지능, 매력, 체력, 스트레스 스탯 관리
- 활동 결과에 따른 스탯 변화
- 중간고사, 기말고사, 대학 축제 등 고정 이벤트
- 질병, 여행, 모의 면접 등 조건 및 랜덤 이벤트
- 선택형 이벤트 및 수학 퀴즈 미니게임
- 최종 스탯에 따른 다양한 엔딩

## Tech Stack

- Python
- JSON
- Git / GitHub

## Project Structure

```text
univeersity_maker/
├── config/         # 게임 설정, 활동, 이벤트, 엔딩 데이터
├── controllers/    # 게임 진행 및 일정 제어
├── managers/       # 데이터 관리
├── resources/      # 캐릭터 저장 데이터
├── services/       # 캐릭터, 활동, 이벤트, 엔딩 로직
├── views/          # 콘솔 화면 출력 및 입력
├── main.py         # 프로그램 실행
└── utils.py
```

## 실행 방법

```bash
git clone https://github.com/ohhyojeong/university_maker.git
cd univeersity_maker
python main.py
```


