import json
from datetime import datetime

import gevent
import gevent.event
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app import app
from app.market.services import get_raw_data


class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_direcory:
            new_data_event.set()


new_data_event = gevent.event.Event()
file_observer = Observer()
file_observer.schedule(FileModifiedHandler(), path=app.config.get('UPDATES_FILE'))


def get_update(from_datetime: datetime):
    filtered_res = ('wood', 'stone', 'food', 'horses')
    result = {}
    for res_name in filtered_res:
        new_data = get_raw_data(res_name, 10000, from_datetime)
        if new_data:
            result[res_name] = new_data
    return result


def update_wait():
    new_data_event.clear()
    file_observer.start()
    app.logger.debug(f"new data wait in {gevent.getcurrent()}")
    result = None
    if new_data_event.wait(30.0):
        app.logger.debug(f"new data catched in {gevent.getcurrent()}")
        with open("/tmp/bs_market_updates") as f:
            result_str = f.read()
        result = json.loads(result_str, parse_float=lambda x: round(float(x), 3))
    else:
        app.logger.debug(f"new data timeout in {gevent.getcurrent()}")

    file_observer.stop()
    file_observer.join()
    return result
