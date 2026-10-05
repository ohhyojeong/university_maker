# author: 오효정
from copy import deepcopy
import random

from config import (
    STATUS,
    CODE,
    OUTCOME_CRITICAL_SUCCESS,
    OUTCOME_SUCCESS,
    OUTCOME_FAILURE,
    OUTCOME_CRITICAL_FAILURE,
    EVENTS
)
from .math_quiz import runMathQuiz
from views.system_views import SystemViews


#고정: 중간, 축제, 기말, 졸업프로젝트
#트리거: 질병 스트레스가 80 넘을 때 , 최대 한달에 한번만.
#랜덤: 여행(7~9), 모의 면접(7~12월) 한 번씩만

class EventServices:

    def __init__(self):
        self.currentEvent = None #현재 진행중인 이벤트 

    def getCalendarEvents(self, month):
        calendar = {
            4: [{'id': 'midterm', 'slot': 2}], #중간
            5: [{'id': 'festival', 'slot': 2}], #축제
            6: [{'id': 'final_exam', 'slot': 2}], #기말
            11: [{'id': 'graduation_project', 'slot': 2}], #졸업프로젝트
        }
        return {
            'status': STATUS['SUCCESS'],
            'code': CODE['DATA_FETCHED'],
            'data': [
                {**entry, 'name': EVENTS[entry['id']]['name']}
                for entry in calendar.get(month, [])
            ],
        }

    def applyFixedEventDay(self, character, event_id, day):
        scheduled = self.getCalendarEvents(character.get('month'))['data']
        if event_id not in EVENTS or not any(
                entry['id'] == event_id for entry in scheduled):
            return {
                'status': STATUS['ERROR'],
                'code': CODE['DATA_NOT_FOUND'],
                'data': None,
            }

        event_key = f"{character['month']}:{event_id}"
        triggered = character.setdefault('events_triggered', [])
        started = event_key not in triggered
        if started:
            self.startEvent(event_id, character)
            triggered.append(event_key)

        return {
            'status': STATUS['SUCCESS'],
            'code': CODE['DATA_FETCHED'],
            'data': {
                'character': character,
                'day_log': {
                    'type': 'fixed_event',
                    'day': day,
                    'event_id': event_id,
                    'started': started,
                },
            },
        }

    def findTriggeredEvent(self, character):  #character를 받음 ScheduleController에서 넘겨줌
        found = None

        # 이미 진행 중인 이벤트가 있으면 새로운 이벤트 발생 X
        if character.get('pending_event'):
            return {
                'status': STATUS['SUCCESS'],
                'code': CODE['DATA_FETCHED'],
                'data': None,
            }

        triggered = character.get('events_triggered', []) #딕셔너리.get('찾을키', 기본값)

        # 1. 조건 이벤트: 스트레스가 80 이상이면 질병
        if character['stats']['stress'] >= 80:
            event_key = f"{character['month']}:illness"

            # 이번 달에 아직 질병이 발생하지 않았다면
            if event_key not in triggered:
                found = EVENTS['illness']


        # 2. 질병이 발생하지 않았다면 랜덤 이벤트 검사
        if found is None: #found가 None이라면
            candidates = []
            for event in EVENTS.values():

                # 1. 랜덤 이벤트가 아니면 제외
                if event.get('type') != 'random':
                    continue

                # 2. 발생 가능한 달이 아니면 제외
                if 'months' in event and character['month'] not in event['months']:
                    continue

                # 3. 반복 불가능 + 이미 발생했다면 제외
                if not event.get('repeatable', False) and event['id'] in triggered:
                    continue
                # 위 조건을 모두 통과하면 후보에 추가
                candidates.append(event)


            # 여행, 모의면접 등의 순서를 랜덤하게 섞음
            random.shuffle(candidates)

            # 랜덤 이벤트 발생 확률 검사(candidates)
            for event in candidates:
                if random.random() < event.get('random_chance', 0.01):
                    found = event
                    break

        return {
            'status': STATUS['SUCCESS'],
            'code': CODE['DATA_FETCHED'],
            'data': deepcopy(found),
        }

    #질병이 발생하면 질병데이터 바꾸는 메서드, 진행할 이벤트만 등록
    def toPendingEvent(self, event):
        return {
            'id': event['id'],
            'remaining_days': max(1, int(event.get('days_lost', 1))), #앞으로 소모할 일수, 최소값을 1로 제한
            'started': False, #효과가 이미 적용했는지
        }


    #이벤트가 하루하루 진행되는 걸 관리하기 위해 있는 메서드
    def applyEventDay(self, character):
        pending = character.get('pending_event')
        if not isinstance(pending, dict) or pending.get('id') not in EVENTS:
            return {
                'status': STATUS['ERROR'],
                'code': CODE['DATA_NOT_FOUND'],
                'data': None,
            }

        remaining = pending.get('remaining_days')
        if not isinstance(remaining, int) or remaining < 1:
            return {
                'status': STATUS['ERROR'],
                'code': CODE['INVALID_PLAN'],
                'data': None,
            }

        event_id = pending['id']
        if not pending.get('started', False):
            self.startEvent(event_id, character)
            pending['started'] = True
            triggered = character.setdefault('events_triggered', [])
            if event_id not in triggered:
                triggered.append(event_id)
            if EVENTS[event_id].get('once_per_month', False):
                event_key = f"{character['month']}:{event_id}"
                if event_key not in triggered:
                    triggered.append(event_key)

        pending['remaining_days'] = remaining - 1
        finished = pending['remaining_days'] == 0
        day_log = {
            'type': 'event',
            'event_id': event_id,
            'remaining_days': pending['remaining_days'],
            'finished': finished,
        }
        if finished:
            character['pending_event'] = None

        return {
            'status': STATUS['SUCCESS'],
            'code': CODE['DATA_FETCHED'],
            'data': {'character': character, 'day_log': day_log},
        }

    def startEvent(self, event_id, character):
        self.currentEvent = EVENTS[event_id] #event_id에 해당하는 이벤트를 하나꺼내 저장
        
        #eventService.loadEvent('midterm') 호출하면, event_id에는 midterm이 들어온다
        #지금 발생하고 있는 이벤트 하나만 선택해서 저장
        #EVENTS['midterm']['difficulty'] ==self.currentEvent['difficulty']

        interaction = self.currentEvent.get("interaction")


        #interaction의 value(choice, None, math_quiz) 일때 
        if interaction is None:
            print(self.currentEvent['message'])
            self.applyEffects(character, self.currentEvent['effects'])
            return None

        if interaction == "math_quiz":

            score = runMathQuiz(
                self.currentEvent['difficulty'], 
                self.currentEvent["time_limit"]
            )

            # 맞힌 개수로 결과 판정
            outcome = self.getQuizOutcome(score)

            # 결과에 맞는 effects 가져오기
            effects = self.currentEvent['effects'][outcome]

            # 캐릭터에게 적용
            self.applyEffects(character, effects)

            return outcome #맞힌 개수

 
        if interaction == "choice": #해당 이벤트에 정의된 선택지를 보여주고 고른 항목에 효과 적용
            print()
            SystemViews.headline(self.currentEvent["name"])
            print(self.currentEvent["message"])
            print()

            choices = self.currentEvent["choices"]

            SystemViews.menu(
                *(choice["text"] for choice in choices)
            )

            selected_number = SystemViews.choice(
                "선택", len(choices)
            )

            selected_choice = choices[selected_number - 1]

            self.applyEffects(character, selected_choice["effects"])

            print(f"\n선택: {selected_choice['text']}")

            return selected_choice

    # 중간 , 기말과 관련
    def getQuizOutcome(self, score): #맞힌 개수-> 시험결과

        if score >= 8:
            return OUTCOME_CRITICAL_SUCCESS #문자열을 담고 있는 상수 변수

        elif score >= 5:
            return OUTCOME_SUCCESS

        elif score >= 2:
            return OUTCOME_FAILURE

        else:
            return OUTCOME_CRITICAL_FAILURE
        
    def applyEffects(self, character, effects):
        for stat, value in effects.items():
            updated = character['stats'][stat] + value

            if stat == "money":
                character["stats"][stat] = updated
            else:
                character["stats"][stat] = max(0, min(100, updated))


        return character
