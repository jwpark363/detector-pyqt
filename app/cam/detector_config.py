import json
from collections import UserDict
from typing import Dict, Any
from copy import deepcopy
from PyQt5.QtWidgets import (
    QLabel
)

CONFIG_FILE = './app/config.json'
NO_SAVE_KEY = ['viewer','tracker','add_newmember']

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

    def save(self):
        print('[Detector State] :: save config!')
        ## json 정보 저장
        config = {}
        ## 저장 대상에서 제외 'viewer', 'tracker' ...
        
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
    
    def set_viewer(self,viewer:QLabel):
        ## 캠 화면 처리용
        print('[Detector State] :: set viewer!')
        self['viewer'] = viewer
    def set_tracker(self,tracker):
        ## 캠 화면 처리용
        print('[Detector State] :: set tracker!')
        self['tracker'] = tracker