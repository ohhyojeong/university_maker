# author: 오효정
EVENTS = {

    # 중간고사
    'midterm': {
        'id': 'midterm',
        'name': '중간고사',
        'message': '중간고사 기간입니다.',
        'interaction': 'math_quiz',
        'difficulty': 'easy',
        'time_limit': 20,
        'days_lost': 3,

        'effects': {
            'critical_success': {
                'intelligence': 10,
                'stress': -5,
            },

            'success': {
                'intelligence': 5,
                'stress': 3,
            },

            'failure': {
                'intelligence': 2,
                'stress': 8,
            },

            'critical_failure': {
                'stress': 15,
                'stamina': -3,
            },
        },
    },



    # 기말고사
    'final_exam': {
        'id': 'final_exam',
        'name': '기말고사',
        'message': '기말고사 기간입니다.',
        'interaction': 'math_quiz',
        'difficulty': 'hard',
        'time_limit': 20,
        'days_lost': 4,

        'effects': {
            'critical_success': {
                'intelligence': 15,
                'stress': -5,
            },

            'success': {
                'intelligence': 8,
                'stress': 5,
            },

            'failure': {
                'intelligence': 3,
                'stress': 10,
            },

            'critical_failure': {
                'stress': 20,
                'stamina': -5,
            },
        },
    },



    # 대학 축제
    'festival': {
        'id': 'festival',
        'name': '대학 축제',
        'message': '친구들이 축제에 같이 가자고 한다!',
        'interaction': 'choice',

        'choices': [
            {
                'text': '친구들과 축제를 즐긴다.',
                'effects': {
                    'money': -80_000,
                    'charm': 10,
                    'stress': -10,
                },
            },
            {
                'text': '축제 기간에도 공부한다.',
                'effects': {
                    'intelligence': 8,
                    'stress': 8,
                },
            },
            {
                'text': '축제 주점에서 알바한다.',
                'effects': {
                    'money': 400_000,
                    'charm': 3,
                    'stamina': -3,
                },
            },
        ],

        'days_lost': 2,
    },


    #  질병
    'illness': {
        'id': 'illness',
        'name': '갑작스러운 몸살',
        'message': '무리한 일정 때문인지 몸살에 걸려 며칠 동안 누워 지냈다.',
        'progress_message': '몸이 아파 일정을 진행할 수 없다.',
        'finish_message': '아픈 게 나아서 내일부터 스케줄대로 활동할 수 있다.',
        'type': 'condition',
        'once_per_month': True, #같은 달에는 한번만

        'trigger': {
            'stat': 'stress',
            'op': 'gte', #greater than or equal,
            'value': 80,
        },

        'days_lost': 5,

        'effects': {
            'stress': -20,
            'stamina': -15,
        },
    },



    # 모의 면접
    'mock_interview': {
        'id': 'mock_interview',
        'months': [7, 8, 9, 10, 11, 12],  #모의 면접은 7~12월
        'name': '모의 면접',
        'message': '학교 취업지원센터에서 진행하는 모의 면접에 참가했다.',
        'type': 'random',

        'trigger': None,

        'days_lost': 2,

        'effects': {
            'intelligence': 5,
            'charm': 8,
            'stress': 10,
        },
    },



    # 여행
    'travel': {
        'id': 'travel',
        'months': [7, 8, 9], #여행은 7~9월
        'name': '갑작스러운 여행 제안',
        'message': '친구가 졸업 전에 제주도로 여행을 가자고 한다!',
        'type': 'random',
        'random_chance': 0.01, # 일반 행동을 마친 하루마다 1% 확률
        'repeatable': False,
        'interaction': 'choice',

        'choices': [
            {
                'text': '지금 아니면 언제 가겠어! 여행을 간다.',
                'effects': {
                    'money': -650_000,
                    'charm': 5,
                    'stress': -20,
                },
            },
            {
                'text': '취업 준비 때문에 거절한다.',
                'effects': {
                    'intelligence': 5,
                    'stress': 5,
                },
            },
            {
                'text': '여행비를 벌기 위해 알바부터 한다.',
                'effects': {
                    'money': 280_000,
                    'stamina': -5,
                    'stress': 5,
                },
            },
        ],

        'days_lost': 4,
    },



    # 졸업 프로젝트

    'graduation_project': {
        'id': 'graduation_project',
        'name': '졸업 프로젝트',
        'message': '졸업 프로젝트가 시작되었다. 어떤 역할을 맡을까?',
        'interaction': 'choice',

        'choices': [
            {
                'text': '팀장을 맡는다.',
                'effects': {
                    'intelligence': 5,
                    'charm': 8,
                    'stress': 15,
                },
            },
            {
                'text': '개발을 담당한다.',
                'effects': {
                    'intelligence': 12,
                    'stamina': -5,
                    'stress': 10,
                },
            },
            {
                'text': '발표를 담당한다.',
                'effects': {
                    'charm': 12,
                    'stress': 8,
                },
            },
        ],

        'days_lost': 5,
    },
}