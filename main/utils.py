from main.extensions import *
from main.Services.Loan.Business.models import BusinessLoanPayment
from main.Services.Loan.Educational.models import EducationalLoanPayment
from main.Services.Loan.Savings.models import SavingsLoansPayment
import os
import logging
from main import app
from datetime import datetime
from main.Settings.Admin.models import AppUser,UserRoleMapping
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data=request.headers['token']
        if not data:
            loger('warning').warning("token missing.")
            return jsonify({"status":False,"data":"","message":"Token missing","error":""}),200
        try:
            token_check=jwt.decode(data,app.config['SECRET_KEY'],algorithms=["HS256"])
            try:
                current_member=AppUser.query.get(token_check['id'])
            except:
                loger('warning').warning("user not found.")
                return jsonify({"status":False,"data":"","message":"user not found."}),200
        except:
            loger("warning").warning("token is invalid")
            return jsonify({"status":False,"msg":"","error":"token is invalid"}),500
        return f(*args, **kwargs)
    return decorator

def permission_required(arguments):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token=request.headers.get('token')
            data_one=jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
            user=AppUser.query.get(data_one['id'])
            role_id=user.role_id
            role = UserRoleMapping.query.filter_by(id=role_id).first()
            access=str(role.access).split(',')
            if (arguments in access):
                return func(*args,**kwargs)
            loger('warning').warning("You cannot access this content.")
            return jsonify({"Message":"You cannot access this content"}),200
        return wrapper
    return decorator

def monthDates():
    dates=[]
    x=datetime.now()
    date=x.strftime("%Y-%m-%d")
    dates.append(date)
    date_list=date.split('-')
    day=int(date_list[2])
    for i in range(1,day):
        day-=1
        if day<10:
            date=f"{date_list[0]}-{date_list[1]}-0{str(day)}"
        else:
            date=f"{date_list[0]}-{date_list[1]}-{str(day)}"
        dates.append(date) 
    return dates

today = datetime.today()
today_str = today.strftime("%d-%b-%Y")
current_year = today.strftime("%Y")
current_month = today.strftime("%b")
current_day = today.strftime("%d")
#create year folder
def Year():
    directory = current_year
    parent_dir = app.root_path+"/"+"log"+"/"
    path = os.path.join(parent_dir, directory)
    try:
        os.mkdir(path)
        return path
    except FileExistsError:
        return path

#create month folder
def Month():
    month_directory = current_month
    parent_dir = Year()+"/"
    path = os.path.join(parent_dir,month_directory)
    try:
        os.mkdir(path)
        return path
    except:
        return path

#create day folder
def Day():
    day_directory = current_day
    parent_dir = Month()+"/"
    path = os.path.join(parent_dir,day_directory)
    try:
        os.mkdir(path)
        return path
    except:
        return path
def clear_logging(logger):
    # Get a list of the handlers for the logger
    handlers = logger.handlers

    # Remove each handler from the logger
    for handler in handlers: 
        logger.removeHandler(handler)
logger = logging.getLogger(__name__)
def loger(level):
    try:
        clear_logging(logger)
        logger.setLevel(logging.DEBUG)
        if level=="error":
            handler = logging.FileHandler(Day()+"/"+"technical_error.log")
        else:
            handler = logging.FileHandler(Day()+"/"+"technical_info.log")
        handler.setLevel(logging.DEBUG)
        logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
        handler.setFormatter(logging_format)
        logger.addHandler(handler)
        # print("logger",logger)
        return logger
    except Exception as e:
        print(f"Error creating logger: {str(e)}")
        return str(e)

# def add_BL_penalty():
#     try:
#         today = datetime.now()
#         month=today.month
#         year=today.year
#         date=today.day
#         if date == 1:
#             print("hi")
#             all_BL_emis=BusinessLoanPayment.query.filter(BusinessLoanPayment.status==0)
#             print("hola!!")
#             penalty_ids=[]
#             for BL_emi in all_BL_emis:
#                 month=today.month
#                 year=today.year
#                 date=today.day
#                 if BL_emi.month<=month and BL_emi.year==year and date>5:
#                     penalty_ids.append(BL_emi.id)
#             if len(penalty_ids)>0:
#                 for emi_id in penalty_ids:
#                     entry=BusinessLoanPayment.query.get(emi_id)
#                     entry.penalty_amount=200
#                     entry.total_amount=entry.amount+200
#                     # db.session.commit()
#                 # scheduler.shutdown()
#                 return print("completed with adding penalty")
#         # scheduler.shutdown()
#         return print("completed without adding penalty")  
#     except Exception as e:
#         loger("error").error(str(e))
#         return print(str(e))
