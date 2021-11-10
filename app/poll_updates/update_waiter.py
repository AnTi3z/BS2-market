import json

# import threading
# from threading import Event
# import gevent
from gevent.event import Event
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, event_obj):
        self._event_obj = event_obj
        super().__init__()

    def on_modified(self, event):
        self._event_obj.set()


def update_wait(app, poll_time=30.0):
    updates_file = app.config.get('UPDATES_FILE')
    if not updates_file:
        return None

    new_data_event = Event()
    file_observer = Observer()
    file_observer.schedule(FileModifiedHandler(new_data_event), path=updates_file)
    file_observer.start()

    if new_data_event.wait(poll_time):
        with open(updates_file) as f:
            result_str = f.read()
        return json.loads(result_str, parse_float=lambda x: round(float(x), 3))
    else:
        return None
