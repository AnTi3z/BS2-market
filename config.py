import os
import logging

_DB_LOGIN = os.environ.get('DB_LOGIN')
_DB_PASS = os.environ.get('DB_PASS')
_DB_SOCKET_NAME = os.environ.get('DB_SOCKET') or '/tmp/mysql.sock'


class Config:
    DATABASE = {
        'name': 'bs_market',
        'engine': 'peewee.MySQLDatabase',
        'user': _DB_LOGIN, 'password': _DB_PASS,
        'unix_socket': _DB_SOCKET_NAME,
        # 'host': '192.168.100.2', 'port': 3306,
    }
    JSON_SORT_KEYS = False
    UPDATES_FILE = "/tmp/bs_market_updates"
    DEBUG = False
    LOG_LEVEL = logging.ERROR


class DevConfig(Config):
    DATABASE = {
        'name': 'test.db',
        'engine': 'peewee.SqliteDatabase',
    }
    UPDATES_FILE = ""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProdConfig(Config):
    DATABASE = {
        'name': 'bs_market',
        'engine': 'peewee.MySQLDatabase',
        'user': _DB_LOGIN, 'password': _DB_PASS,
        'unix_socket': _DB_SOCKET_NAME,
        # 'host': '192.168.100.2', 'port': 3306,
    }
    UPDATES_FILE = "/tmp/bs_market_updates"
    DEBUG = False
    LOG_LEVEL = logging.WARNING
