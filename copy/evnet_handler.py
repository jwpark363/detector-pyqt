import os
from typing import List, Dict, Union, Callable
from watchdog.observers import Observer
from watchdog.events import DirCreatedEvent, FileCreatedEvent, FileSystemEventHandler

class DetectorHandler(FileSystemEventHandler):
    def __init__(self, target_directory:str, action_map:Dict[str,Callable]) -> None:
        super().__init__()
        self.action_map = action_map
        self.observers = []
        self.target_directories = []
        for path in action_map:
            self.target_directories.append(os.path.join(target_directory,path))
        self.initialize_directory(self.target_directories)
    
    ## when new file created, do something
    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        print(event)
        if event.is_directory:
            return None
        else:
            print(f'new file created : {event.src_path}')
            ## follow action map
            directory_path = os.path.dirname(event.src_path)
            action_key = os.path.basename(directory_path)
            print(f'*** {action_key} action start...')
            if action_key in self.action_map:
                self.action_map[action_key](event.src_path)           
    
    ## initialize directories
    def initialize_directory(self, target_directories:Union[List[str], None]):
        if target_directories is None:
            return False
        if not isinstance(target_directories, list):
            return False
        for path in target_directories:
            if not os.path.exists(path):
                os.mkdir(path)
            observer = Observer()
            observer.schedule(self,path,recursive=False)
            self.observers.append(observer)
        return True