import json

from flask import current_app

import threading
from threading import Event
# import gevent
# from gevent.event import Event
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# import uwsgi


class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, event_obj):
        self._event_obj = event_obj
        super().__init__()

    def on_modified(self, event):
        self._event_obj.set()


class UpdateWaiter:
    def __init__(self):
        self.new_data_event = Event()
        self.file_observer = Observer()
        self.file_observer.schedule(FileModifiedHandler(self.new_data_event), path=current_app.config.get('UPDATES_FILE'))
        self.file_observer.start()
        # uwsgi.add_file_monitor(2, app.config.get('UPDATES_FILE'))
        # uwsgi.register_signal(2, "", lambda _: self.new_data_event.set())

    def update_wait(self):
        self.new_data_event.clear()
        current_app.logger.debug(f"new data wait in {threading.current_thread()}")
        result = None
        if self.new_data_event.wait(30.0):
            current_app.logger.debug(f"new data catched in {threading.current_thread()}")
            with open("/tmp/bs_market_updates") as f:
                result_str = f.read()
            result = json.loads(result_str, parse_float=lambda x: round(float(x), 3))
        else:
            current_app.logger.debug(f"new data timeout in {threading.current_thread()}")

        return result
