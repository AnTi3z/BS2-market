import json

from peewee import *


with open("config.json") as f:
    cfg = json.load(f)

_LOGIN = cfg['mysql']['login']
_PASS = cfg['mysql']['pass']

db = MySQLDatabase('bs_market', autoconnect=False,
                   user=_LOGIN, password=_PASS,
                   # host='192.168.100.2', port=3306)
                   unix_socket="/tmp/mysql.sock")


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = db


class Resource(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=8, unique=True)

    class Meta:
        table_name = 'resources'


class PriceVolumeData(BaseModel):
    res = ForeignKeyField(column_name='res', field='id', model=Resource)
    ts = DateTimeField()
    price = FloatField()
    volume = IntegerField()

    class Meta:
        primary_key = CompositeKey('res', 'ts')
        table_name = 'price_data'


class User(BaseModel):
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    username = CharField(max_length=32)

    class Meta:
        table_name = 'tg_users'


class TokenStatus(BaseModel):
    id = IntegerField(primary_key=True)
    text = CharField(column_name='status', max_length=10)

    class Meta:
        table_name = 'token_status'


class Token(BaseModel):
    token = FixedCharField(primary_key=True, max_length=16)
    user = ForeignKeyField(column_name='user_id', field='id', model=User)
    status = ForeignKeyField(column_name='status', field='id', model=TokenStatus)
    created = DateTimeField()
    modified = DateTimeField()

    class Meta:
        table_name = 'tokens'
