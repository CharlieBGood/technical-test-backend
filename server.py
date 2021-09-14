# Run with "python server.py"

from bottle import run, post, get, request, response, app
from models import Note, User
from schemas import NoteSchema, UserSchema, LoginUserSchema
from marshmallow import ValidationError
from datetime import datetime
from bottle_cors_plugin import cors_plugin

import json
import bcrypt
import jwt

# Start your code here, good luck (: ...


@post('/notes')
def add_new_note():
    note_schema = NoteSchema()
    data = note_schema.load(request.POST)
    if data.errors:
        return data.errors
    else:
        payload = jwt.decode(request.POST.get('token'), "charlie", algorithms=["HS256"])
        try:
            user = User.get(User.username==payload['username'])
        except:
            return {'user' : "There is not user register with that username in our database"}
        note = Note.create(title=data.data['title'], content=data.data['content'], user=user)
        return {'success': 'New note created!'}


@get('/notes')
def list_notes():
    token = request.GET.get('token')
    try:
        payload = jwt.decode(request.GET.get('token'), "charlie", algorithms=["HS256"])
    except:
        return {'error': 'Wrong token'}
    try:
        user = User.get(User.username==payload['username'])
    except:
        return {'user' : "There is not user register with that username in our database"}
    
    schema = NoteSchema(many=True)
    result = schema.dumps(user.notes)
    return result.data


@post('/sign-up')
def add_user():
    user_schema = UserSchema()
    data = user_schema.load(request.POST)
    
    if data.errors:
        return data.errors
    else:
        hashed = bcrypt.hashpw(data.data['password'].encode(), bcrypt.gensalt())
        user = User.create(username=data.data['username'], email=data.data['email'], password=hashed, join_date=datetime.today())
        return {'success': 'New user created!'}


@post('/sign-in')
def login():
    
    login_user_schema = LoginUserSchema()
    data = login_user_schema.load(request.POST)

    if data.errors:
        return data.errors
    
    user = User.get(User.username==request.POST.get('username'))
    login_password = data.data['password']
    
    valid = bcrypt.checkpw(login_password.encode(), user.password.encode())
    
    if valid:
        token = jwt.encode({"username": user.username}, "charlie", algorithm="HS256")
        return {'token': token.decode(), 'username': user.username}
    else:
        return {'password': 'Wrong password'}
    

#Confugure the server
app = app()
app.install(cors_plugin('*'))

run(host='localhost', port=8001)