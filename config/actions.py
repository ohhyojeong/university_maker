ACTIONS = [
  {
    'id': 1,
    'name': '취업 준비',
    'weights': {
      'money': -8_000,
      'intelligence': 1,
      'stamina': -1,
      'stress': 1,
    },
    'messages': {
      'critical_success': '자소서가 술술 써지고 면접 연습도 완벽했다!',
      'success': '스펙 정리를 차분히 이어 갔다.',
      'failure': '집중이 안 돼 서류만 바라봤다.',
      'critical_failure': '지원 마감을 놓칠 뻔했다..',
    },
  },
  {
    'id': 2,
    'name': '아르바이트',
    'weights': {
      'money': 90_000,
      'stamina': -1,
      'stress': 1,
    },
    'messages': {
      'critical_success': '손님에게 칭찬을 받고 팁까지 받았다!',
      'success': '무난하게 일을 마쳤다.',
      'failure': '실수가 잦아 눈치를 봤다.',
      'critical_failure': '실수 연발이었다..',
    },
  },
  {
    'id': 3,
    'name': '외관 관리',
    'weights': {
      'money': -45_000,
      'charm': 1,
      'stamina': 1,
      'stress': -1,
    },
    'messages': {
      'critical_success': '거울 속 내가 낯설 정도로 빛났다!',
      'success': '피부와 스타일을 깔끔히 가꿨다.',
      'failure': '관리 루틴을 제대로 못 지켰다.',
      'critical_failure': '컨디션이 망가져 외출이 부끄러웠다..',
    },
  },
  {
    'id': 4,
    'name': '쇼핑',
    'weights': {
      'money': -50_000,
      'charm': 1,
      'stress': -1,
    },
    'messages': {
      'critical_success': '원하던 아이템을 세일로 건졌다!',
      'success': '쓸모 있는 물건을 골라 담았다.',
      'failure': '충동구매만 하고 후회했다.',
      'critical_failure': '지갑만 비우고 취향도 놓쳤다..',
    },
  },
  {
    'id': 5,
    'name': '건강 관리',
    'weights': {
      'money': -35_000,
      'stamina': 1,
      'stress': -1,
    },
    'messages': {
      'critical_success': '운동이 잘 되어 몸이 한결 가볍다!',
      'success': '스트레칭과 식단을 지켰다.',
      'failure': '피곤해서 운동을 대충 넘겼다.',
      'critical_failure': '무리하다 몸살이 날 뻔했다..',
    },
  },
  {
    'id': 6,
    'name': '영어 공부',
    'weights': {
      'money': -5_000,
      'intelligence': 1,
      'stamina': -1,
      'stress': 1,
    },
    'messages': {
      'critical_success': '표현이 머릿속에 쏙쏙 들어왔다!',
      'success': '단어와 리스닝을 꾸준히 했다.',
      'failure': '문법만 보다가 진도가 밀렸다.',
      'critical_failure': '단어가 하나도 안 외워졌다..',
    },
  },
  {
    'id': 7,
    'name': '돈 모으기',
    'weights': {
      'money': 30_000,
      'stress': 1,
    },
    'messages': {
      'critical_success': '예상보다 많이 저축했다!',
      'success': '계획대로 통장에 넣었다.',
      'failure': '쓸데없는 지출이 새어 나갔다.',
      'critical_failure': '충동적으로 돈을 다 써 버렸다..',
    },
  },
  {
    'id': 8,
    'name': '휴식/여가',
    'weights': {
      'money': -28_000,
      'stamina': 1,
      'stress': -1,
    },
    'messages': {
      'critical_success': '푹 쉬어 머리가 맑아졌다!',
      'success': '취미로 기분 전환을 했다.',
      'failure': '쉬는 데도 마음이 복잡했다.',
      'critical_failure': '쉬려다 오히려 더 지쳤다..',
    },
  },
]