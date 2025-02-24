import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Arquivo alterado: {event.src_path}")
            subprocess.run(["flet", "run", "main.py", "--web", "--reload"])

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=".", recursive=True)

observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
