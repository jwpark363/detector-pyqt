import edge_tts, tempfile, asyncio, os
from watchdog.events import FileSystemEventHandler
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

BASE_URL = 'http://localhost:8000/api'
API_MAP = {
    '0':'person',
    '67':'id'
}
class FileCreatedHandler(FileSystemEventHandler):
    def __init__(self, label, watch_dir):
        self.label = label
        self.watch_dir = watch_dir
        self.player = QMediaPlayer()

    async def play_voice(self, text):
        voice="ko-KR-SunHiNeural"
        communicate = edge_tts.Communicate(text=text, voice=voice)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
            await communicate.save(temp_path)
            # 재생
            url = QUrl.fromLocalFile(temp_path)  # 로컬 MP3 파일 경로
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()
    '''
    1. 파일의 클래스 체크
    2. 클래스에 따른 API 호출
    3. AIP 결과 보이스 출력
    '''
    def on_created(self, event):
        if not event.is_directory:
            target_path = event.src_path
            target_file = os.path.basename(target_path)
            cls = target_file.split('_')[0]
            print(f"*** File Event Handler - {event.src_path} 파일이 생성됨")
            if cls == '0': ## 사람
                self.handle_person(target_file)
            elif cls == '67': ## 핸드폰(사원증)
                self.handle_id(target_file)
            asyncio.run(self.play_voice('음성 테스트'))
    def handle_person(self,image_file):
        cls = '0'
        print(f'api : {BASE_URL}/{API_MAP[cls]}')
        print(f'{self.watch_dir}/{cls}/{image_file}')
    def handle_id(self,image_file):
        cls = '67'
        print(f'api : {BASE_URL}/{API_MAP[cls]}')
        print(f'{self.watch_dir}/{cls}/{image_file}')
            
