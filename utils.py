
def getDisplayWidth(text: str) -> int:
    """
    [순수 파이썬 기본 문법 활용]
    문자열의 실제 터미널 출력 너비(칸 수)를 계산합니다.
    - 한글(가~힣, 자음/모음): 2칸
    - 영어, 숫자, 공백: 1칸
    """
    width = 0
    for char in str(text):
        if '가' <= char <= '힣' or 'ㄱ' <= char <= 'ㅣ':
            width += 2
        else:
            width += 1
    return width


def padByDisplayWidth(text: str, targetWidth: int, align: str = "left", fillChar: str = " ") -> str:
    """

    문자의 시각적 너비(Display Width)를 고려하여 지정한 너비만큼 정렬 패딩을 추가합니다.
    (한글/전각 문자와 영문/반각 문자가 섞여 있어도 정렬이 깨지지 않도록 합니다.)
    
    :param text: 출력할 문자열
    :param targetWidth: 목표 총 너비 (칸 수)
    :param align: 정렬 방향 ('left', 'right', 'center')
    :param fillChar: 빈자리를 채울 문자 (기본 공백)
    :return: 너비가 맞춰진 문자열
    """
    currentWidth = getDisplayWidth(text)
    paddingNeeded = max(0, targetWidth - currentWidth)

    if align == "left":
        return str(text) + (fillChar * paddingNeeded)
    elif align == "right":
        return (fillChar * paddingNeeded) + str(text)
    elif align == "center":
        leftPad = paddingNeeded // 2
        rightPad = paddingNeeded - leftPad
        return (fillChar * leftPad) + str(text) + (fillChar * rightPad)
    else:
        return str(text)

