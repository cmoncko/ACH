from main.extensions import db
from datetime import datetime

class Employee(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    employee_type=db.Column(db.Integer(),server_default="0",nullable=False)
    status=db.Column(db.Integer(),server_default="0",nullable=False)
    name=db.Column(db.String(100),nullable=False)
    dob=db.Column(db.Date(),nullable=False)
    gender=db.Column(db.Integer(),server_default="0",nullable=False)
    image_path=db.Column(db.String(255))
    address=db.Column(db.String(255),nullable=False)
    city=db.Column(db.String(255),nullable=False)
    district=db.Column(db.String(255),nullable=False)
    state=db.Column(db.String(255),nullable=False)
    pincode=db.Column(db.Integer(),nullable=False)
    aadhar=db.Column(db.BigInteger(),nullable=False)
    mobile=db.Column(db.BigInteger(),nullable=False)
    join_date=db.Column(db.Date(),nullable=False)
    salary=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    relieving_date=db.Column(db.String(10))
    created_on=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self):
        return f"<userId:{self.id}"
    
    def to_json(self):
        dob=self.DOB
        dob_date_list=str(dob).split('-') #it return ['year','month','date']
        day=datetime.now().strftime("%Y-%m-%d")# date of today
        date_now=day.split("-") #it return ['year','month','date']
        dyear=int(dob_date_list[0]) # convert string to integer
        dmonth=int(dob_date_list[1]) # '''
        ddate=int(dob_date_list[2]) # '''
        nyear=int(date_now[0]) # '''
        nmonth=int(date_now[1]) # '''
        ndate=int(date_now[2]) # '''

        # check the month and date grater than or equal to dob month and date
        if (nmonth>= dmonth) & (ndate>=ddate): 
            age=nyear-dyear # if true return absoult value
        else:
            age=nyear-dyear
        return {
           "id":self.id,
           "name":self.name, 
           "age":age,
           "gender":self.gender,
           "city":self.city,
           "mobile_no":self.mobile_no,
           "incharge_id":self.incharge_id
        }
    def profile(self):
        dob=self.DOB
        dob_date_list=str(dob).split('-') #it return ['year','month','date']
        day=datetime.now().strftime("%Y-%m-%d")# date of today
        date_now=day.split("-") #it return ['year','month','date']
        dyear=int(dob_date_list[0]) # convert string to integer
        dmonth=int(dob_date_list[1]) # '''
        ddate=int(dob_date_list[2]) # '''
        nyear=int(date_now[0]) # '''
        nmonth=int(date_now[1]) # '''
        ndate=int(date_now[2]) # '''

        # check the month and date grater than or equal to dob month and date
        if (nmonth>= dmonth) & (ndate>=ddate): 
            age=nyear-dyear # if true return absoult value
        else:
            age=nyear-dyear
        return {"name":self.name,
                "id":self.id,
                "DOB":dob, 
                "age":age,
                "gender":self.gender,
                "city":self.city,
                "state":self.state,
                "district":self.district,
                "address":self.address,
                "relieving_date":self.relieving_date,
                "image_path":self.image_path,
                "aadhar_number":self.aadhar,
                "mobile_no":self.mobile,
                }
    def emp_export(self):
        return {"name":self.name,
                "id":self.id,
                "employee_type":self.employee_type,
                "DOB":self.dob,
                "gender":self.gender,
                "city":self.city,
                "state":self.state,
                "district":self.district,
                "address":self.address,
                "pincode":self.pincode,
                "status":self.status,
                "join_date":self.join_date,
                "salary":self.salary,
                "relieving_date":self.relieving_date,
                "image_path":self.image_path,
                "aadhar_number":self.aadhar,
                "mobile_no":self.mobile
                }