# author: 임유빈

from copy import deepcopy
from config import CODE, STATUS, CHARACTER_TEMPLATE

class CharacterServices:
    def __init__(self, store):
        self.store = store
        self.playCharacter = None  # 현재 플레이 중인 캐릭터 세션

    def findAllCharacters(self):
        """저장된 모든 캐릭터 목록을 반환 (최대 8개 슬롯 제한 관리용)"""
        result = self.store.findAll('character')

        if result.get('status') == STATUS['SUCCESS']: #findall에서 불러온 데이터를 리스트형태로 반환
                                                      #출력은 controllers 또는 views 파일에서 실행
            data = result.get('data')

            if isinstance(data, list):
                return data[:8]  # 조건 4, 6: 최대 8개 슬롯
            elif isinstance(data, dict):     #createCharacter함수에서 이미 8개가 넘을 경우를 방지
                return [data]
        return []

    def createCharacter(self, name=None, birth_month=1):
        """
        - 슬롯 8개 초과 시 경고 출력 후 리턴
        - 이름 미입력 시 'unknown' 및 중복 방지 숫자 부여 (unknown 2, 3...)
        - 이미 존재하는 이름이면 실패 출력 후 재입력 유도
        - 이름, 생일(month), 기본 스탯(deepcopy) 조합 후 DataManager로 저장
        """

        existing_characters = self.findAllCharacters()

        # 저장된 캐릭터가 8개 이상이면 세이브 슬롯 가득 참 경고 후 리턴
        if len(existing_characters) >= 8:
            print("[경고] 세이브 슬롯이 가득 찼습니다! (최대 8개)")
            return {'status': STATUS['ERROR'], 'code': CODE['SLOT_FULL'], 'data': None}

        existing_names = [char.get('name') for char in existing_characters if isinstance(char, dict)]
                         #char에 저장된 캐릭터 목록을 꺼내옴(for-in)   #char가 dict형태인지 확인(if)
                         #char에서 'name' 키에 맞는 값(실제이름)을 가져옴(char.get('name'))

        # 이름을 입력하지 않은 경우 ('unknown' + 중복 방지 숫자)
            # 이름이 아예 없거나   or      #공백만 적었을 경우 공백 사라지고 빈칸이면
        if not name or (isinstance(name, str) and not name.strip()):
            base_name = "unknown"   #기본 이름은 unknown
            name = base_name
            counter = 1
            while name in existing_names:       # name 변수에 들어있는 이름(unknown)이 existing_names 목록에 있으면
                counter += 1                      # 카운트하는 숫자가 1씩 올라감
                name = f"{base_name} {counter}"    # name은 "unknown n" 으로 출력
        else:
            # 유저가 이미 있는 이름을 입력한 경우
            name = name.strip()
            if name in existing_names:
                print(f"[실패] 이미 존재하는 이름입니다: '{name}'. 다시 입력해주세요.")
                return {'status': STATUS['ERROR'], 'code': CODE['DUPLICATE_NAME'], 'data': None}

        # 기본 스탯 템플릿 deepcopy 복사 및 이름, 생일(month) 설정
        new_char = deepcopy(CHARACTER_TEMPLATE)
        new_char['name'] = name
        new_char['month'] = birth_month  # 생일(또는 시작 월) 정보 반영

        # DataManager를 통해 저장 (store.create 활용)
        result = self.store.create('character', new_char)

        if result.get('status') == STATUS['SUCCESS']: # 위의 작업이 정상적으로 작동한다면(새로운 캐릭터 생성)

            data = result.get('data')

            if isinstance(data, list) and len(data) > 0:  #data(캐릭터 목록)가 리스트 형태인지 확인 + 리스트 안에 1개 이상의 캐릭터가 있다면
                self.playCharacter = data[-1]             #가장 마지막에 있는(=제일 최근에 새로 추가된)캐릭터를 플레이어로 지정
            else:
                self.playCharacter = new_char             #위의 조건이 맞아도 속의 데이터가 어긋나있을 경우를 대비해서 기본 스탯을 쥐어주는 상태로 현재플레이어로 진행

            print(f"[성공] 캐릭터 생성 완료: {self.playCharacter.get('name')} (ID: {self.playCharacter.get('id')})")
                                      # 새 캐릭터 생성 완료시 "[성공] 캐릭터 생성 완료: [이름] (ID: [아이디])" 출력됨

            return {'status': STATUS['SUCCESS'], 'data': self.playCharacter}

        else:
            print("[실패] 캐릭터 저장 중 오류가 발생했습니다.")
            return {'status': STATUS['ERROR'], 'code': CODE['SAVE_FAILED'], 'data': None}

    def loadCharacter(self, index):
        """
        SceneController의 chooseSave()와 완벽 호환되는 이어하기 메서드:
        - 전달받은 슬롯 번호(index)를 이용해 목록에서 해당 캐릭터를 안전하게 탐색
        - 데이터 형식을 방어적으로 검증한 뒤 playCharacter로 지정하고 반환
        """

        # 1. 저장된 전체 캐릭터 목록 가져오기
        existing_characters = self.findAllCharacters()

        # 2. 방어 코드: 목록이 리스트 형태가 아니거나, 인덱스가 범위를 벗어났는지 확인
        if not isinstance(existing_characters, list) or index < 0 or index >= len(existing_characters):
            print("[실패] 유효하지 않은 저장 슬롯입니다.")                    #목록 갯수보다 큰 번호는 접근X
            return None  # SceneController의 `if character:`에 걸려서 안전하게 무시됨

        # 3. 해당 인덱스의 캐릭터 데이터 가져오기
        target_char = existing_characters[index]

        # 4. 방어 코드: 가져온 데이터가 딕셔너리 형태인지 확인 (캐릭터 목록은 리스트, 캐릭터 개별은 딕셔너리로 데이터 저장)
        if isinstance(target_char, dict):
            self.playCharacter = target_char
            print(f"[성공] 이어하기 성공: {target_char.get('name')} (ID: {target_char.get('id')})")
            return self.playCharacter  # SceneController의 lobby(character)로 전달됨
        else:
            print("[실패] 손상되었거나 올바르지 않은 캐릭터 데이터입니다.")
            return None

    def saveCharacter(self, character=None):
        """
        조용하게 백그라운드에서 캐릭터 데이터를 영구 저장하는 함수 (사일런트 오토세이브)
        - 성공 시에는 군더더기 없이 조용히 True를 반환하고,
        - 실패(에러) 시에만 로그를 남깁니다.
        """

        # 1. 대상 캐릭터 설정 (인자로 받지 않았으면 현재 플레이 중인 캐릭터 선택)
        target_char = character if character is not None else self.playCharacter

        # 2. 방어 코드: 저장할 캐릭터가 없으면 차단
        if not target_char or 'id' not in target_char:
            print("[에러] 저장할 캐릭터 세션이 없습니다.")  #출력은 선택
            return False

        # 3. 데이터베이스(저장소)에 업데이트 요청
        char_id = target_char['id']
        result = self.store.update('character', char_id, target_char)

        # 4. 결과 처리 (성공 시 출력 없이 True, 실패 시에만 에러 출력)
        if result.get('status') == STATUS['SUCCESS']:
            return True
        else:
            print("[에러] 캐릭터 데이터 동기화 실패")
            return False