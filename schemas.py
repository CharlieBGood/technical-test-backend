from marshmallow import Schema, fields, validates, ValidationError
from models import User

#Define Note schema
class NoteSchema(Schema):
    
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    token = fields.Str(required=True)

class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    join_date = fields.DateTime()
    
    @validates("username")
    def validate_username(self, value):
        try:
            user = User.get(User.username==value)
        except:
            return True
        raise ValidationError("The username already exists in our database")
    
    @validates("password")
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must contain at least 7 letters.")
        if len(value) > 30:
            raise ValidationError("Password can't contain more than 7 letters.")
        
class LoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    
    @validates("username")
    def validate_username(self, value):
        try:
            user = User.get(User.username==value)
        except:
            raise ValidationError("There is not user register with that username in our database")
    
        