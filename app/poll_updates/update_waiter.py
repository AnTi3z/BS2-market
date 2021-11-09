import json
import threading

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
    def __init__(self, event_obj):
        self.new_data_event = event_obj
        self.file_observer = Observer()
        self.logger = None

    def init_app(self, app):
        self.logger = app.logger
        self.file_observer.schedule(FileModifiedHandler(self.new_data_event), path=app.config.get('UPDATES_FILE'))
        self.file_observer.start()
        # uwsgi.add_file_monitor(2, app.config.get('UPDATES_FILE'))
        # uwsgi.register_signal(2, "", lambda _: self.new_data_event.set())

    def update_wait(self):
        self.new_data_event.clear()
        self.logger.debug(f"new data wait in {threading.current_thread()}")
        result = None
        if self.new_data_event.wait(30.0):
            self.logger.debug(f"new data catched in {threading.current_thread()}")
            with open("/tmp/bs_market_updates") as f:
                result_str = f.read()
            result = json.loads(result_str, parse_float=lambda x: round(float(x), 3))
        else:
            self.logger.debug(f"new data timeout in {threading.current_thread()}")

        return result
