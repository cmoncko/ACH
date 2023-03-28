from main.extensions import *
import os
import logging
from main import app
from datetime import datetime
from main.Teams.Incharge.models import Employee
from main.Settings.Admin.models import AppUser,UserRoleMapping
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data=request.headers['token']
        if not data:
            return jsonify({
                "message":"Token missing"
            })
        try:
            token_check=jwt.decode(data,app.config['SECRET_KEY'],algorithms=["HS256"])
            try:
                current_member=AppUser.query.get(token_check['id'])
            except:
                return jsonify({
                    "message":"user not found."
                })
        except:
            return jsonify({
                'message':'Token is invalid'
            })
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
            role = UserRoleMapping.query.filter_by(role_id=role_id).first()
            access=str(role.access).split(',')
            if (arguments in access):
                return func(*args,**kwargs)
            return jsonify({"Message":"You cannot access this content"})
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

def loger():
    today = date.today()
    today_str = today.strftime("%d-%b-%Y")

    current_year = today.strftime("%Y")
    current_month = today.strftime("%b")
    current_day = today.strftime("%d")
    #create year folder
    def Year():
        directory = current_year
        parent_dir = app.root_path+"/"+"log"+"/"
        path=os.path.join(parent_dir, directory)

        try:
            os.mkdir(path)
            return parent_dir
        except FileExistsError:
            return parent_dir

    #create_month folder
    def Month():
        month_directory = current_month
        parent_dir_ = Year()+current_year+"/"
        path = os.path.join(parent_dir_, month_directory)

        try:
            os.mkdir(path)
            return parent_dir_
        except:
            return parent_dir_ 

    #create_day folder
    def day():
        month_directory = current_day
        parent_dir_ = Month()+current_month+"/"
        path = os.path.join(parent_dir_, month_directory)

        try:
            os.mkdir(path)
            return  path
        except:
            return  path



    logger=logging.getLogger('hello')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(day()+"/"+"technical_info.log")
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

    handler.setFormatter(logging_format)
    logger.addHandler(handler)

    handler1 = logging.FileHandler(day()+"/"+"technical_error.log")
    handler1.setLevel(logging.ERROR)
    logging_format1 = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler1.setFormatter(logging_format1)
    logger.addHandler(handler1)
