from .system_views import SystemViews
from .character_views import CharacterViews
from config import OUTCOME_LABELS

class ScheduleViews:
  """표시 전용. 조회는 하지 않고 컨트롤러가 넘긴 값만 사용."""

  def __init__(self):
    pass

  @staticmethod
  def title(name, month, currentSlot, monthlyActions):
    SystemViews.subtitle(
      f'{name}님의 {month}월 스케쥴 [{currentSlot}/{monthlyActions}]'
    )

  @staticmethod
  def slotLabel(item):
    if item is None:
      return '(미선택)'
    return item.get('name')

  def description(self, schedules, currentIndex):
    print()
    for index, item in enumerate(schedules):
      print(f'   {index + 1}. {self.slotLabel(item)}')
    print()
    SystemViews.lineBreak()

    print(f'  {currentIndex + 1}번째 스케줄을 선택해 주세요')

  def chooseSchedule(self, schedules, actions, currentIndex) -> int:
    self.description(schedules, currentIndex)
    print()

    menu = [item.get('name') for item in actions]
    menu.append('뒤로가기')
    SystemViews.menu(*menu)
    SystemViews.lineBreak()

    return SystemViews.choice(f'{currentIndex + 1} 번째 스케쥴', len(menu))

  def monthStart(self, month):
    print(f'{month}월 일정을 시작합니다')
    print()

  def monthEnd(self, month):
    SystemViews.lineBreak()
    SystemViews.subtitle(
      f'{month}월 일정이 종료되었습니다!',
      '캐릭터 정보를 확인해 주세요',
    )
    print()

  def nextMonth(self):
    SystemViews.input('엔터를 누르면, 다음 달로 넘어갑니다')

  @staticmethod
  def showEnding(ending, stats=None):
    SystemViews.headline('엔딩', ending.get('name', ''))
    message = ending.get('message')
    if message:
      print(message)
      print()
    CharacterViews.stats(stats or {})

  def setCanceled(self):
    SystemViews.errorMessage('스케쥴 선택을 취소했습니다')
    print()

  @staticmethod
  def insufficientMoney(actionName=None):
    if actionName:
      SystemViews.errorMessage(
        f'소지금이 부족해서 [{actionName}]을(를) 선택할 수 없습니다'
      )
    else:
      SystemViews.errorMessage('소지금이 부족해서 선택할 수 없습니다')
    SystemViews.input('엔터를 누르면 다시 선택합니다')

  def dayLog(self, dayLog):
    if not dayLog:
      return

    logType = dayLog.get('type')
    if logType == 'action':
      self.printActionDay(dayLog)
      return
    if logType == 'fixed_event':
      self.printFixedEventDay(dayLog)
      return
    if logType == 'event':
      self.printEventDay(dayLog)

  @staticmethod
  def printActionDay(dayLog):
    month = dayLog.get('month')
    day = dayLog.get('day')
    name = dayLog.get('action_name')
    outcome = dayLog.get('outcome')
    label = OUTCOME_LABELS.get(outcome, outcome)
    message = dayLog.get('message') or ''
    print(f'{month}월 {day}일 [{name}]')
    print(f'- {label}! {message}')
    print()

  @staticmethod
  def printFixedEventDay(dayLog):
    month = dayLog.get('month')
    day = dayLog.get('day')
    name = dayLog.get('event_name')
    message = dayLog.get('message') or ''
    print(f'{month}월 {day}일 [{name}]')
    if message:
      print(f'- {message}')
    print()

  @staticmethod
  def printEventDay(dayLog):
    month = dayLog.get('month')
    day = dayLog.get('day')
    name = dayLog.get('event_name')
    message = dayLog.get('message') or ''
    if name:
      print(f'{month}월 {day}일 [{name}]')
    else:
      print(f'{month}월 {day}일')
    if message:
      print(f'- {message}')
    print()