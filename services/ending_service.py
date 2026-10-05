# author: 정진규
from config import ENDINGS

def get_ending(stats):
  """stats를 받아 조건에 맞는 엔딩 정보(딕셔너리)를 반환한다."""
  money = stats.get('money', 1_500_000)
  intel = stats.get('intelligence', 0)
  charm = stats.get('charm', 0)
  stamina = stats.get('stamina', 0)
  stress = stats.get('stress', 0)

  if intel >= 75 and charm >= 60 and stress <= 50:
    ending_id = 'large_company'
  elif intel >= 70 and money >= 3_000_000:
    ending_id = 'abroad'
  elif money >= 6_000_000 and intel >= 60:
    ending_id = 'startup'
  elif charm >= 75:
    ending_id = 'youtuber'
  elif stamina >= 80 and intel < 40:
    ending_id = 'labor'
  elif intel >= 50 and stress <= 70:
    ending_id = 'sme'
  else:
    ending_id = 'unemployed'

  return ENDINGS[ending_id]