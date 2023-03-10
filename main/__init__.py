from flask import Flask
from .extenstions import db

app=Flask(__name__,instance_relative_config=True)
app.config.from_prefixed_env()

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:password@localhost:3306/ACH'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True

db.init_app(app)

#Team
from main.Teams.Members.models import *
from main.Teams.Incharge.models import *

from main.Teams.Members.views import member
from main.Teams.Incharge.views import incharge
from main.Teams.Leader.views import leader

app.register_blueprint(member)
app.register_blueprint(incharge)
app.register_blueprint(leader)


#Funds
from main.Funds.Santha.models import *
from main.Funds.Savings.models import *

from main.Funds.Santha.views import santha
from main.Funds.Savings.views import savings 

app.register_blueprint(santha)
app.register_blueprint(savings)

#Services
from main.Services.Requests.models import *
from main.Services.Benefits.models import *
from main.Services.Pension.models import *

from main.Services.Requests.views import requests
from main.Services.Benefits.views import benefit
from main.Services.Pension.views import pension

app.register_blueprint(requests)
app.register_blueprint(benefit)
app.register_blueprint(pension)

#Loan
from main.Services.Loan.Savings.models import *
from main.Services.Loan.Educational.models import *
from main.Services.Loan.Business.models import*

#Settings
from main.Settings.Services.models import *
from main.Settings.Accounts.models import *
from main.Settings.Teams.models import *
from main.Settings.Admin.models import * 
from main.Settings.Loans.models import *
from main.Settings.Funds.models import *

from main.Settings.Services.views import settingServices

app.register_blueprint(settingServices)

#Accounts
from main.Accounts.Expense.models import *
from main.Accounts.Income.models import *
from main.Accounts.Deposit.models import *#withdraw
