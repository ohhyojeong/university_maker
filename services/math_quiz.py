import random
import time


def createMathProblem(difficulty):

    if difficulty == 'easy':
        a = random.randint(1, 10)
        b = random.randint(1, 10)

    else:
        a = random.randint(10, 50)
        b = random.randint(10, 50)

    operator = random.choice(['+', '-', '*'])#리스트에서 하나가 랜덤하게 나옴

    if operator == '+':
        answer = a + b

    elif operator == '-':
        answer = a - b

    else:
        answer = a * b

    return a, operator, b, answer


def runMathQuiz(difficulty, time_limit):###################import

    score = 0
    start_time = time.time()

    while time.time() - start_time < time_limit: #제한시간동안 문제 계속나옴

        a, operator, b, answer = createMathProblem(difficulty)

        user_answer = input(f"{a} {operator} {b} = ") #입력받기

        if time.time() - start_time >= time_limit:
            print("시간 종료되었습니다!")
            break

        try:
            if int(user_answer) == answer:
                print("정답입니다")
                score += 1
            else:
                print("오답입니다")

        except ValueError:
            print("숫자를 입력해주세요.")

    return score