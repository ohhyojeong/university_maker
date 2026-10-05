from time import sleep

from config import (
  TOTAL_MONTHS,
  MONTHLY_ACTIONS,
  DAY_PAUSE_SECONDS,
  SCHEDULE_KIND_FIXED_EVENT,
  STATUS,
  CODE,
  ENDINGS,
  EVENTS,
)
from views import ScheduleViews, CharacterViews
from services import (
  ActionsServices,
  CharacterServices,
  EventServices,
  get_ending
)


class ScheduleController:
  def __init__(self, store):
    self.actionsServices = ActionsServices()
    self.characterServices = CharacterServices(store)
    self.eventServices = EventServices()
    self.scheduleViews = ScheduleViews()
    self.characterViews = CharacterViews()
    self.isCancel = False

  def scheduleSelection(self, character):
    self.isCancel = False
    actions = self.actionsServices.findAllActions()

    while not self.isCancel and character.get('ending') is None:
      month = character.get('month')
      schedules = self.initializeSchedules(month)

      while None in schedules:
        currentIndex = schedules.index(None)
        self.scheduleViews.title(
          character.get('name'),
          month,
          currentIndex + 1,
          MONTHLY_ACTIONS,
        )
        menuIndex = self.scheduleViews.chooseSchedule(
          schedules, actions, currentIndex,
        ) - 1

        if menuIndex == len(actions):
          self.setCanceled()
          break

        selectedAction = actions[menuIndex]
        result = self.actionsServices.selectScheduleAction(
          character,
          selectedAction.get('id'),
          schedules,
          currentIndex,
        )
        if result.get('status') == STATUS['ERROR']:
          if result.get('code') == CODE['INSUFFICIENT_MONEY']:
            actionName = (result.get('data') or {}).get('action_name')
            self.scheduleViews.insufficientMoney(actionName)
          continue

      if self.isCancel:
        break

      self.runMonth(character, schedules)

      if month < TOTAL_MONTHS:
        self.nextMonth(character)
      else:
        self.endGame(character)
        break

  def initializeSchedules(self, month):
    schedules = [None] * MONTHLY_ACTIONS
    result = self.eventServices.getCalendarEvents(month)
    fixedEvents = result.get('data') or [] if result.get('status') != STATUS['ERROR'] else []

    for fixed in fixedEvents:
      slot = int(fixed.get('slot', 0)) - 1
      if slot < 0 or slot >= MONTHLY_ACTIONS:
        continue
      schedules[slot] = {
        'kind': SCHEDULE_KIND_FIXED_EVENT,
        'id': fixed.get('id'),
        'name': fixed.get('name'),
      }
    return schedules

  def setCanceled(self):
    self.isCancel = True
    self.scheduleViews.setCanceled()
    print()

  def runMonth(self, character, schedules):
    dayQueue = self.actionsServices.buildDayQueue(schedules)
    self.scheduleViews.monthStart(character.get('month'))
    self.runDayQueue(character, dayQueue)

  def enrichEventDayLog(self, dayLog, character, day):
    if not dayLog:
      return dayLog

    logType = dayLog.get('type')
    if logType not in ('fixed_event', 'event'):
      return dayLog

    eventId = dayLog.get('event_id')
    event = EVENTS.get(eventId) or {}
    name = event.get('name')
    enriched = {
      **dayLog,
      'month': character.get('month'),
      'day': day if dayLog.get('day') is None else dayLog.get('day'),
    }

    if logType == 'fixed_event':
      enriched['event_name'] = name
      return enriched

    if dayLog.get('finished'):
      enriched['message'] = event.get('finish_message') or (
        f'{name}이 끝나 내일부터 스케줄대로 활동할 수 있다.'
      )
    else:
      enriched['message'] = event.get('progress_message') or (
        f'{name} 때문에 일정을 진행할 수 없다.'
      )
    return enriched

  def runDayQueue(self, character, dayQueue):
    """
    컨트롤러 오케스트레이션:
    - pending 있으면 EventService만 (재조회 없음)
    - fixed_event면 고정 일정 1일
    - action이면 Actions → Event 발생 판정 → pending 세팅
    - 매일 Character 저장 (saveCharacter)
    """
    for day, item in enumerate(dayQueue, start=1):
      dayLog = None

      if character.get('pending_event'):
        eventResult = self.eventServices.applyEventDay(character)
        if eventResult.get('status') == STATUS['ERROR']:
          break
        payload = eventResult.get('data') or {}
        character = payload.get('character') or character
        dayLog = self.enrichEventDayLog(payload.get('day_log'), character, day)
      elif item.get('kind') == SCHEDULE_KIND_FIXED_EVENT:
        fixedResult = self.eventServices.applyFixedEventDay(
          character, item.get('id'), day,
        )
        if fixedResult.get('status') == STATUS['ERROR']:
          break
        payload = fixedResult.get('data') or {}
        character = payload.get('character') or character
        dayLog = self.enrichEventDayLog(payload.get('day_log'), character, day)
      else:
        actionResult = self.actionsServices.applyDay(
          character, item.get('id'), day,
        )
        if actionResult.get('status') == STATUS['ERROR']:
          break
        payload = actionResult.get('data') or {}
        character = payload.get('character') or character
        dayLog = payload.get('day_log')

        foundResult = self.eventServices.findTriggeredEvent(character)
        found = (foundResult.get('data')
                 if foundResult.get('status') != STATUS['ERROR']
                 else None)
        if found:
          character['pending_event'] = self.eventServices.toPendingEvent(found)

      self.saveCharacter(character)

      if dayLog:
        self.scheduleViews.dayLog(dayLog)

      sleep(DAY_PAUSE_SECONDS)

  def nextMonth(self, character):
    self.scheduleViews.monthEnd(character.get('month'))
    self.characterViews.stats(character.get('stats'))
    
    character['month'] += 1
    self.saveCharacter(character)
    self.scheduleViews.nextMonth()

  def endGame(self, character, ending=None):
    if ending is None:
      result = get_ending(character.get('stats') or {})
    elif isinstance(ending, dict):
      result = ending
    elif ending in ENDINGS:
      result = ENDINGS[ending]
    else:
      result = {'id': ending, 'name': ending, 'message': ''}

    self.scheduleViews.showEnding(result, character.get('stats') or {})
    character['ending'] = result.get('id') or result.get('name')
    self.saveCharacter(character)

  def saveCharacter(self, character):
    self.characterServices.saveCharacter(character)