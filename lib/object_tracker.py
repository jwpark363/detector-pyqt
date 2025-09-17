import cv2, torch, copy
import numpy as np
from cv2.typing import MatLike
from datetime import datetime

class ObjectTracker:
    def __init__(self) -> None:
        ## id : {count,saved} 저장
        self.store = {}
        ## 출력 여부
        self.verbose = False
        ## 클래스 분류 대상 ["0","67",...]
        self.classes = []
        ## 이벤트 디렉토리 이미지 저장 위치
        self.event_dir = '.'
        ## 캡쳐 대상 최소 프레임 카운터 2초 48프레임
        self.count_limit = 0
        ## 캡쳐 대상 사이즈 최소 사람 width 10000, height 10000
        self.size_limit = {}
        ## 로그 팝업
        self.logger = None
    
    def init_config(self, config):
        print('tracker',config)
        self.event_dir = config['capture_dir']
        self.count_limit = config['count_limit']
        for target in config['target_list']:
            # print(config['target_list'][target])
            if config['target_list'][target][3]: ## 대상이면
                self.classes.append(target)
                self.size_limit[target] = {
                    'width':config['target_list'][target][1],
                    'height':config['target_list'][target][2]
                }
        self.print_config()
    ## logger 세팅
    def set_logger(self, logger):
        self.logger = logger
        ## 탐지 되었을 때와 저장 될때 로그 처리
    def print_config(self):
        print(f'분류 대상 : {self.classes}')
        print(f'이벤트 디렉토리 : {self.event_dir}')
        print(f'캡처 최소 프레임 : {self.count_limit}')
        print(f'캡처 최소 사이즈 : {self.size_limit}')

    def check_n_save(self, frame:MatLike, datas:np.ndarray):
        ## id:{count:0,saved:False,cls:1,file:file}
        store = copy.deepcopy(self.store)
        ## 탐지에서 벗어난 ID 삭제용
        new_cls = set()
        for box in datas:
            cls = str(int(box[-1]))
        # 1. 신규 frame box 데이터 필터(사람, 핸드폰)
            if cls not in self.classes:
                continue
            id = int(box[4])
            new_cls.add(id)
            ## 박스 사이즈 width, height 고려
            x1,y1,x2,y2 = box[:4].astype(int)
            width,height = abs(x2 - x1),abs(y2 - y1)
            if self.verbose:
                print(cls,width,height,self.size_limit[cls]['width'],self.size_limit[cls]['height'])
        # 2. ID 카운팅
            if id in store:
                store[id]['count'] = self.store[id]['count'] + 1
            else:
                store[id] = {'count':1, 'saved':False}
                ## @@@@@@ 탐지 로그 처리
                if self.logger:
                    self.logger.add_log(id,cls,False,'')
        # 3. 최소 20개(설정) 이상 인경우 프레임 이미지로 저장 후 ID 삭제
        ### 저장시 해당 프레임과 BOX 데이터도 함께 저장 매치 시키기 위해 id_timestamp.jpg, id_timestamp.box
        ### 파일 포맷 : cls_id_x1_y1_x2_y2_yyyymmddhhmiss.jpg
            if (not store[id]['saved']) and store[id]['count'] >= self.count_limit \
            and width >= int(self.size_limit[cls]['width']) and height >= int(self.size_limit[cls]['height']):
                img_file = f'{cls}_{id}_{x1}_{y1}_{x2}_{y2}_{datetime.today().strftime("%Y%m%d%H%M%S")}.jpg'
                frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                cv2.imwrite(f'{self.event_dir}/{img_file}',frame)
                ## 클래스에 박스 이미지 저장
                cv2.imwrite(f'{self.event_dir}/{cls}/{img_file}',frame[y1:y2,x1:x2])
                ## @@@@@@ 저장 로그 처리
                if self.logger:
                    self.logger.add_log(id,cls,True,img_file,f'count:{store[id]["count"]},size:{width}x{height}')
                if self.verbose:
                    print(f'&&& id {id}-{width}x{height} saved & deleted')
        #### 프레임 저장 후 해당 아이디가 사라질때 까지 추가 저장 하지 않게 하기위함
                store[id]['saved'] = True
        # 4. 신규 frame box에 존재하지 않는 ID 삭제(신규 store로 기존 store 대체)
        for cls in set(store.keys()) -new_cls:
            del store[cls]
        self.store = store
        if self.verbose:
            print(self.store)