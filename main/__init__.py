from .extensions import Flask,db,datetime,scheduler

app=Flask(__name__,instance_relative_config=True)
app.config.from_prefixed_env()

app.config['SECRET_KEY']='cmoncko'
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
from main.Services.Loan.Savings.models import *
from main.Services.Loan.Business.models import *
from main.Services.Loan.Educational.models import *
from main.Services.AccountClosing.models import *

from main.Services.Requests.views import requests
from main.Services.Benefits.views import benefits
from main.Services.Pension.views import pension
from main.Services.Loan.Savings.views import savings_loan
from main.Services.Loan.Business.views import business_loan
from main.Services.Loan.Educational.views import educational_loan
from main.Services.AccountClosing.views import account_closing

app.register_blueprint(requests)
app.register_blueprint(benefits)
app.register_blueprint(pension)
app.register_blueprint(savings_loan)
app.register_blueprint(business_loan)
app.register_blueprint(educational_loan)
app.register_blueprint(account_closing)

#Accounts
from main.Accounts.Deposit.models import *
from main.Accounts.Expense.models import *
from main.Accounts.Income.models import *

from main.Accounts.Income.views import income
from main.Accounts.Expense.views import expense
from main.Accounts.Deposit.views import deposit
from main.Accounts.Withdraw.views import withdraw

app.register_blueprint(income)
app.register_blueprint(expense)
app.register_blueprint(deposit)
app.register_blueprint(withdraw)

#Settings
from main.Settings.Services.models import *
from main.Settings.Accounts.models import *
from main.Settings.Funds.models import *
from main.Settings.Admin.models import *
from main.Settings.Loans.models import *
from main.Settings.Teams.models import *

from main.Settings.Services.views import settingServices
from main.Settings.Accounts.views import settings_accounts
from main.Settings.Funds.views import settingsfunds
from main.Settings.Admin.views import admin
from main.Settings.Teams.views import settingsTeams
from main.Settings.Loans.views import settings_loans

app.register_blueprint(admin)
app.register_blueprint(settingsfunds)
app.register_blueprint(settingServices)
app.register_blueprint(settings_accounts)
app.register_blueprint(settingsTeams)
app.register_blueprint(settings_loans)

#Drop Down & Dashboard
from main.DropDown.views import drop_down
from main.Dashboard.views import dashboard
 
app.register_blueprint(drop_down)
app.register_blueprint(dashboard)

#Auth
from main.Authentication.Auth import auth

app.register_blueprint(auth)

#Records

from main.Records.Export import export
from main.Records.Import import import_csv

app.register_blueprint(export)
app.register_blueprint(import_csv)

#Report

from main.Report.MonthlyCollection.views import collection

app.register_blueprint(collection)

#Schedule job

# app.config['SCHEDULER_API_ENABLED']=True
# app.config['JOBS'] = [{'id': 'job1',
#                        'func': add_BL_penalty,
#                        'trigger': 'cron',
#                        'day': '1',
#                        'hour': '23',
#                        'minute': '5'}]
# scheduler.init_app(app)
# scheduler.start()