from flask import Flask
from main.extenstions import db

app=Flask(__name__,instance_relative_config=True)

app.config.from_prefixed_env()

app.config['SQLALCHEMY_DATABASE_URI']='sql+mysql://root:password@localhost:3306/main'
app.conig['SQLALCHEMY_TRACK_MODIFICATION']=True

db.init_app(app)

from main.teams.members.model import *

from main.teams.members.views import member

app.register_blueprint(member)