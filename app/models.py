from peewee import *

from app import db


class Resource(db.Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=8, unique=True)

    class Meta:
        table_name = 'resources'


class PriceVolumeData(db.Model):
    res = ForeignKeyField(column_name='res', field='id', model=Resource)
    ts = DateTimeField()
    price = FloatField()
    volume = IntegerField()

    class Meta:
        primary_key = CompositeKey('res', 'ts')
        table_name = 'price_data'


class User(db.Model):
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    username = CharField(max_length=32)

    def serialize(self):
        return {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username}

    class Meta:
        table_name = 'tg_users'


class TokenStatus(db.Model):
    id = IntegerField(primary_key=True)
    text = CharField(column_name='status', max_length=10)

    class Meta:
        table_name = 'token_status'


class Token(db.Model):
    token = FixedCharField(primary_key=True, max_length=16)
    user = ForeignKeyField(column_name='user_id', field='id', model=User)
    status = ForeignKeyField(column_name='status', field='id', model=TokenStatus)
    created = DateTimeField()
    modified = DateTimeField()

    @classmethod
    def get_by_str(cls, token_str):
        return cls.get_or_none(cls.token == token_str)

    def serialize(self):
        return {'token': self.token,
                'status': self.status.text,
                'created': self.created.isoformat(),
                'status_updated': self.modified.isoformat(),
                'user': self.user.serialize()}

    class Meta:
        table_name = 'tokens'
