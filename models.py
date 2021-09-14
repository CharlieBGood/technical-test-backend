from peewee import *

db = SqliteDatabase('notes.db')

class User(Model):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField() 
    
    class Meta:
        database = db

class Note(Model):
    title = CharField(max_length=256)
    content = TextField()
    user = ForeignKeyField(User, backref='notes')

    class Meta:
        database = db 