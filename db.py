from models import db, Note, User

# db connection
db.connect()
# Table creation
db.create_tables([Note, User])