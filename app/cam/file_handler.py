import edge_tts, tempfile, asyncio, os, requests
from gtts import gTTS
from watchdog.events import FileSystemEventHandler
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from app.cam.detector_config import DetectorState

BASE_URL = 'http://localhost:8000'
API_MAP = {
    '0-False':'detect_face', # image_class_model
    '0-True':'whoami', # recognition_model
    '67-True':'ocr',
    '67-False':'ocr',
}
class FileCreatedHandler(FileSystemEventHandler):
    def __init__(self, label):
        self.config = DetectorState()
        self.label = label
        self.watch_dir = self.config['capture_dir']
        self.player = QMediaPlayer()
    async def play_voice(self, text):
        voice="ko-KR-SunHiNeural"
        communicate = edge_tts.Communicate(text=text, voice=voice)
        with tempfile.NamedTemporaryFile(
            dir='./tts_temp', 
            delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
            await communicate.save(temp_path)
            # 재생
            url = QUrl.fromLocalFile(temp_path)  # 로컬 MP3 파일 경로
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()
    async def play_voice_by_gtts(self, text):
        tts = gTTS(text=text, lang='ko')  # 'ko'는 한국어
        with tempfile.NamedTemporaryFile(
            dir='./tts_temp', 
            delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
            tts.save(temp_path)
            # 재생
            url = QUrl.fromLocalFile(temp_path)  # 로컬 MP3 파일 경로
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()

    def post(self, url:str, image_file:str):
        print(f'upload file : {image_file}')
        print(f'api url : {url}')
        params = {
            'mode':self.config['mode']
        }
        with open(image_file, 'rb') as img:
            files = {'files':(os.path.basename(image_file), img, 'image/jpeg')}
            response = requests.post(url,files=files, data=params)
        print(response.status_code, response.text)
        return response
    '''
    1. 파일의 클래스 체크
    2. 클래스에 따른 API 호출
    3. AIP 결과 보이스 출력
    '''
    def on_created(self, event):
        if not event.is_directory:
            target_path = event.src_path
            target_file = os.path.basename(target_path)
            cls, id = target_file.split('_')[:2]
            if self.config['recognition_model']:
                cls = f'{cls}-True'
            else:
                cls = f'{cls}-False'
            url = f'{BASE_URL}/{API_MAP[cls]}'
            response = self.post(url,target_path)
            print(response.json())
            if response.status_code == 200:
                result = response.json()[0]['message']
            else:
                result = '인식이 실패 하였습니다. 다시 한번 시도해주세요.'
            self.config['logger'].add_tts_log(id,cls,result)
            asyncio.run(self.play_voice_by_gtts(result))
