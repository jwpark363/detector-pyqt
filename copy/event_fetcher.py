import time
import os
import requests
from lib.evnet_handler import DetectorHandler

## requests post with capture image
def post(file_path:str):
    url = 'http://localhost:8000/app/upload'
    print(f'upload file : {file_path}')
    with open(file_path, 'rb') as img:
        files = {'file':(os.path.basename(file_path), img, 'image/jpeg')}
        print(files)
        print(f'api url : {url}')
        response = requests.post(url,files=files)
    print(response.status_code, response.text)
    return response.json()

def personAction(file:str):
    print('person action',file)
    result = post(file)
    ## result tts 처리
    print(result)
    print('person action end')

def phoneAction(file:str):
    print('phone action',file)
    result = post(file)
    ## result tts 처리
    print(result)
    print('phone action end')

ACTION_MAP = {
    'person': personAction,
    'phone': phoneAction,
}

if __name__ == "__main__":
    target_directory = '.'
    event_handler = DetectorHandler(target_directory,ACTION_MAP)

    print('**** Detector Event Handler Start....')
    for observer in event_handler.observers:
        print(observer)
        observer.start()
        
    try:
        while True:
            time.sleep(0.4)
    except KeyboardInterrupt:
        for observer in event_handler.observers:
            observer.stop()
        for observer in event_handler.observers:
            observer.join()