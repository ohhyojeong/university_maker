from copy import deepcopy

from .constants import DEFAULT_STATS

# 새 캐릭터 생성 시 사용하는 기본 스키마 (단일 dict)
CHARACTER_TEMPLATE = {
  'name': 'unknown',
  'turn': 0,
  'month': 1,
  'stats': deepcopy(DEFAULT_STATS),
  'history': [],
  'action_counts': {},
  'events_triggered': [],
  'pending_event': None,
  'ending': None,
}

# 파일 저장소 기본값: 캐릭터는 세이브 슬롯 목록(list)
DEFAULT_DATA = {
  'character': [],
}