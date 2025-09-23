import json, os
from collections import UserDict
from copy import deepcopy
from PyQt5.QtWidgets import (
    QLabel
)

CONFIG_FILE = './app/config.json'
NO_SAVE_KEY = ['detector','viewer','tracker','logger','add_newmember','members']
## 'add_member' : 신규 인력 추가 모드 체크용
class DetectorState(UserDict):
    ## 싱글톤
    _instance = None
    ## 초기화 여부
    _is_init = False
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print('[Detector State] :: new instance')
        return cls._instance
    def __init__(self) -> None:
        if DetectorState._is_init:
            ## 초기화 되었다면
            print('[Detector State] :: state is already setted!')
            return
        DetectorState._is_init = True
        ## 생성시 json 정보 로드
        self.reset()
        self['viewer'] = None
        self['tracker'] = None
        print('[Detector State] :: init instance completed!')
        ## 디렉토리가 생성 되지 않았다면 생성 처리??
        if 'capture_dir' not in self.data:
            self['capture_dir'] = './captureed'
        if not os.path.exists(self['capture_dir']):
            os.makedirs(self['capture_dir'])
            for cls in self['target_list']:
                cls_dir = os.path.join(self['capture_dir'],cls)
                if not os.path.exists(cls_dir):
                    os.makedirs(cls_dir)
        if 'new_member' not in self.data:
            self['new_member'] = './new_member'
        if not os.path.exists(self['new_member']):
            os.makedirs(self['new_member'])
        if not os.path.exists(self['tts_temp']):
            os.makedirs(self['tts_temp'])
            

    def save(self):
        print('[Detector State] :: save config!')
        ## json 정보 저장
        config = {}
        ## 저장 대상에서 제외 'viewer', 'tracker', 'logger' ...
        
        for key in self:
            if key in NO_SAVE_KEY:
                continue
            config[key] = self[key]
        print(config)
        with open(CONFIG_FILE,'w') as f:
            json.dump(config,f, indent=4)
    
    def reset(self):
        ## json 정보 다시 읽어오기
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
            super().__init__(config)
        except:
            print(f'[Detector State] :: {CONFIG_FILE} not found or problem!')
            exit(0)
    
    def set_detector(self,detector):
        ## 캠 코더 처리용
        print('[Detector State] :: set detector!')
        self['detector'] = detector
    def set_viewer(self,viewer:QLabel):
        ## 캠 화면 처리용
        print('[Detector State] :: set viewer!')
        self['viewer'] = viewer
    def set_tracker(self,tracker):
        ## 캠 화면 트랙킹묭
        print('[Detector State] :: set tracker!')
        self['tracker'] = tracker
    def set_logger(self,logger):
        ## 캠 화면 로그용
        print('[Detector State] :: set logger!')
        self['logger'] = logger
