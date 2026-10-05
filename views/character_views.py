from .system_views import SystemViews
from config import STAT_LABELS, TOTAL_MONTHS
from config.endings import ENDINGS
from utils import padByDisplayWidth

class CharacterViews:
  def __init__(self):
    pass

  @staticmethod
  def title(character):
    name = character.get('name')
    month = character.get('month')
    ending = character.get('ending')
    if ending is None:
      SystemViews.subtitle(f'{name} - {month}월')
    else:
      endingName = ENDINGS.get(ending, {}).get('name', ending)
      SystemViews.subtitle(f'{name} - 엔딩: {endingName}')

  @staticmethod
  def stats(stats, length=20):
    for stat, value in stats.items():
        statName = padByDisplayWidth(f"  {STAT_LABELS.get(stat)}", 10)
        if stat != 'money':
          filled = max(0, min(length, int(round((int(value) / 100) * length))))
          statInfo = f'{statName} : {value:>8} [{"▨" * filled}{"_" * (length - filled)}]'
          print(padByDisplayWidth(statInfo, 48, align='center'))

    SystemViews.lineBreak(True)
    money = int(stats.get('money') or 0)
    moneyName = padByDisplayWidth(f"  {STAT_LABELS.get('money')}", 10)
    moneyValue = padByDisplayWidth(f"{money:,}원", 31, align='right')
    print(padByDisplayWidth(f'{moneyName} : {moneyValue}', 48, align='center'))
    SystemViews.lineBreak()

  @staticmethod
  def menu():
    menus = '스케쥴 관리', '뒤로가기'
    SystemViews.menu(*menus)
    SystemViews.lineBreak()
    return SystemViews.choice('메뉴 선택', len(menus))

  @staticmethod
  def createCharacterTitle():
    SystemViews.subtitle('캐릭터 생성')

  @staticmethod
  def inputName() -> str:
    return SystemViews.input('이름 입력 (미입력 시 unknown)')

  @staticmethod
  def chooseSaveFileTitle():
    SystemViews.subtitle('저장 파일 선택')

  @staticmethod
  def chooseSaveFile(list) -> int:
    save_list = []
    if list is None or len(list) == 0:
      print()
      print('  저장된 캐릭터가 없습니다')
      print()
    else:
      for i, character in enumerate(list):
        if character is not None and i < 8:
          ending = character.get('ending')
          ending_name = ENDINGS.get(ending, {}).get('name', ending) if ending else ''
          ending_text = f" / 엔딩: {ending_name}" if ending else ''
          name = character.get('name')
          saved_text = f"{name if name else 'unknown'} "
          saved_text += f"- {character.get('month')}월 "
          saved_text += f"(턴 {character.get('turn')}/{TOTAL_MONTHS}){ending_text}"
          save_list.append(saved_text)

    save_list.append('뒤로가기')

    SystemViews.menu(*save_list)
    SystemViews.lineBreak()

    return SystemViews.choice('저장 파일 선택', len(save_list))