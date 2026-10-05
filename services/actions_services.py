import random
from fractions import Fraction
from config import (
  ACTIONS,
  DAYS_PER_ACTION,
  SCHEDULE_KIND_ACTION,
  SCHEDULE_KIND_FIXED_EVENT,
  STATUS,
  CODE,
  STAT_MIN,
  STAT_MAX,
  OUTCOME_MULTIPLIERS,
  OUTCOME_CHANCES,
  OUTCOME_CRITICAL_SUCCESS,
  OUTCOME_CRITICAL_FAILURE,
  OUTCOME_FAILURE,
  OUTCOME_SUCCESS,
  CRITICAL_FAILURE_STRESS_BONUS,
)

class ActionsServices:
  def __init__(self):
    pass

  @staticmethod
  def findAllActions():
    return [
      { 'id': action.get('id'), 'name': action.get('name') }
      for action in ACTIONS
    ]

  @staticmethod
  def buildDayQueue(schedules):
    dayQueue = []
    for item in schedules:
      if item is None:
        continue
      kind = item.get('kind')
      itemId = item.get('id')
      if kind not in (SCHEDULE_KIND_ACTION, SCHEDULE_KIND_FIXED_EVENT):
        continue
      dayQueue.extend([
        { 'kind': kind, 'id': itemId }
        for _ in range(DAYS_PER_ACTION)
      ])
    return dayQueue

  @staticmethod
  def getAction(actionId):
    for action in ACTIONS:
      if action.get('id') == actionId:
        return action
    return None

  @staticmethod
  def getSlotMoneyCost(actionId):
    action = ActionsServices.getAction(actionId)
    if action is None:
      return 0

    moneyWeight = (action.get('weights') or {}).get('money', 0)
    if moneyWeight >= 0:
      return 0
    return abs(moneyWeight) * DAYS_PER_ACTION

  @staticmethod
  def getReservedMoneyCost(schedules):
    reserved = 0
    for item in schedules or []:
      if item is None:
        continue
      if item.get('kind') != SCHEDULE_KIND_ACTION:
        continue
      reserved += ActionsServices.getSlotMoneyCost(item.get('id'))
    return reserved

  @staticmethod
  def canAffordAction(character, actionId, schedules=None):
    cost = ActionsServices.getSlotMoneyCost(actionId)
    if cost == 0:
      return True

    money = int((character.get('stats') or {}).get('money') or 0)
    reserved = ActionsServices.getReservedMoneyCost(schedules)
    return money >= reserved + cost

  @staticmethod
  def selectScheduleAction(character, actionId, schedules, currentIndex):
    action = ActionsServices.getAction(actionId)
    if action is None:
      return {
        'status': STATUS['ERROR'],
        'code': CODE['INVALID_ACTION'],
        'data': None,
      }

    if not ActionsServices.canAffordAction(character, actionId, schedules):
      return {
        'status': STATUS['ERROR'],
        'code': CODE['INSUFFICIENT_MONEY'],
        'data': {'action_name': action.get('name')},
      }

    schedules[currentIndex] = {
      'kind': SCHEDULE_KIND_ACTION,
      'id': action.get('id'),
      'name': action.get('name'),
    }

    return {
      'status': STATUS['SUCCESS'],
      'code': CODE['DATA_SAVED'],
      'data': {
        'schedules': schedules,
        'slot': schedules[currentIndex],
      },
    }

  @staticmethod
  def rollOutcome():
    total = sum(weight for _, weight in OUTCOME_CHANCES)
    roll = random.randrange(total)
    cumulative = 0
    for outcome, weight in OUTCOME_CHANCES:
      cumulative += weight
      if roll < cumulative:
        return outcome
    return OUTCOME_SUCCESS

  @staticmethod
  def isGainStat(stat, weight):
    if stat == 'stress':
      return weight < 0
    return weight > 0

  @staticmethod
  def calcDayDelta(weights, outcome):
    delta = {}

    for stat, weight in (weights or {}).items():
      if weight == 0:
        continue

      if stat == 'money':
        if weight > 0:
          multiplier = OUTCOME_MULTIPLIERS.get(outcome, Fraction(1, 1))
          delta[stat] = int(weight * multiplier)
        else:
          delta[stat] = weight
        continue

      if ActionsServices.isGainStat(stat, weight):
        if outcome == OUTCOME_CRITICAL_SUCCESS:
          delta[stat] = weight * 2
        elif outcome == OUTCOME_SUCCESS:
          delta[stat] = weight
        elif outcome == OUTCOME_FAILURE:
          delta[stat] = 0
        elif outcome == OUTCOME_CRITICAL_FAILURE:
          delta[stat] = -weight
        else:
          delta[stat] = weight
      else:
        if outcome == OUTCOME_CRITICAL_FAILURE:
          delta[stat] = weight * 2
        else:
          delta[stat] = weight

    if outcome == OUTCOME_CRITICAL_FAILURE:
      delta['stress'] = delta.get('stress', 0) + CRITICAL_FAILURE_STRESS_BONUS

    return delta

  @staticmethod
  def applyDelta(character, delta):
    stats = character.setdefault('stats', {})

    for stat, value in delta.items():
      current = stats.get(stat, 0)
      updated = current + value

      if stat == 'money':
        stats[stat] = max(0, updated)
      else:
        stats[stat] = max(STAT_MIN, min(STAT_MAX, updated))

    return character

  @staticmethod
  def getOutcomeMessage(action, outcome):
    messages = action.get('messages') or {}
    return messages.get(outcome, '')

  @staticmethod
  def applyDay(character, actionId, day=None):
    action = ActionsServices.getAction(actionId)
    if action is None:
      return {
        'status': STATUS['ERROR'],
        'code': CODE['INVALID_ACTION'],
        'data': None,
      }

    outcome = ActionsServices.rollOutcome()
    delta = ActionsServices.calcDayDelta(action.get('weights'), outcome)
    ActionsServices.applyDelta(character, delta)

    counts = character.setdefault('action_counts', {})
    counts[actionId] = counts.get(actionId, 0) + 1

    return {
      'status': STATUS['SUCCESS'],
      'code': CODE['DATA_FETCHED'],
      'data': {
        'character': character,
        'day_log': {
          'type': 'action',
          'month': character.get('month'),
          'day': day,
          'action_id': actionId,
          'action_name': action.get('name'),
          'outcome': outcome,
          'message': ActionsServices.getOutcomeMessage(action, outcome),
          'delta': delta,
        },
      },
    }