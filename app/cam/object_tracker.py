import cv2, copy
import numpy as np
from cv2.typing import MatLike
from datetime import datetime
from app.cam.detector_config import DetectorState

class ObjectTracker:
    def __init__(self) -> None:
        ## 출력 여부
        self.verbose = False
        ## id : {count,saved} 저장
        self.store = {}
        ## config set
        self.config = DetectorState()
    
    def check_n_save(self, frame:MatLike, datas:np.ndarray):
        ## 로그 팝업
        logger =self.config.get('logger',None)
        ## id:{count:0,saved:False,cls:1,file:file}
        store = copy.deepcopy(self.store)
        ## 탐지에서 벗어난 ID 삭제용
        new_cls = set()
        for box in datas:
            cls = str(int(box[-1]))
        # 1. 신규 frame box 데이터 필터(대상이 아닌경우)
            if (cls not in self.config['target_list']) \
                or (not self.config['target_list'][cls][3]):
                continue
            id = int(box[4])
            new_cls.add(id)
            ## 박스 사이즈 width, height 고려
            x1,y1,x2,y2 = box[:4].astype(int)
            width,height = abs(x2 - x1),abs(y2 - y1)
            if self.verbose:
                print(cls,width,height,self.config['target_list'][cls][1],self.config['target_list'][cls][2])
        # 2. ID 카운팅
            # if id in store:
            #     store[id]['count'] = self.store[id]['count'] + 1
            # else:
            #     store[id] = {'count':1, 'saved':False}
            try:
                store[id]['count'] = self.store[id]['count'] + 1
            except:
                store[id] = {'count':1, 'saved':False}
                ## @@@@@@ 탐지 로그 처리
                if logger:
                    logger.add_log(id,cls,'False','')
        # 3. 최소 20개(설정) 이상 인경우 프레임 이미지로 저장 후 ID 삭제
        ### 저장시 해당 프레임과 BOX 데이터도 함께 저장 매치 시키기 위해 id_timestamp.jpg, id_timestamp.box
        ### 파일 포맷 : cls_id_x1_y1_x2_y2_yyyymmddhhmiss.jpg
            if (not store[id]['saved']) and store[id]['count'] >= self.config['count_limit']\
            and width >= int(self.config['target_list'][cls][1]) and height >= int(self.config['target_list'][cls][2]):
                img_file = f'{cls}_{id}_{x1}_{y1}_{x2}_{y2}_{datetime.today().strftime("%Y%m%d%H%M%S")}.jpg'
                frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                cv2.imwrite(f'{self.config["capture_dir"]}/{img_file}',frame)
                ## 클래스에 박스 이미지 저장
                cv2.imwrite(f'{self.config["capture_dir"]}/{cls}/{img_file}',frame[y1:y2,x1:x2])
                ## @@@@@@ 저장 로그 처리
                if logger:
                    logger.add_log(id,cls,'True',img_file,f'count:{store[id]["count"]},size:{width}x{height}')
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