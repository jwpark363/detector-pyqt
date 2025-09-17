from watchdog.events import FileSystemEventHandler

class FileCreatedHandler(FileSystemEventHandler):
    def __init__(self, label,watch_dir):
        self.label = label

    def on_created(self, event):
        if not event.is_directory:
            print(f"*** File Event Handler - {event.src_path} 파일이 생성됨")