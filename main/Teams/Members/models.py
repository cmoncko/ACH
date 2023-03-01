from ...extenstions import db
from datetime import datetime

class MemberProfile(db.Model):
    id=db.Column(db.BigInteger,primary_key=True)
    user_id=db.Column(db.String(50),nullable=False,unique=True)
    name=db.Column(db.String(50),nullable=False)
    DOB=db.Column(db.Date(),nullable=False)
    image_path=db.Column(db.String(250))
    gender=db.Column(db.Integer(),server_default="0")
    address=db.Column(db.String(255),nullable=False)
    city=db.Column(db.String(120),nullable=False)
    district=db.Column(db.String(120),nullable=False)
    state=db.Column(db.String(120),nullable=False)
    pincode=db.Column(db.Integer(),nullable=False)
    auth_type_id=db.Column(db.Integer(),server_default="0")
    auth_data=db.Column(db.String(100),nullable=False)
    auth_path=db.Column(db.String(255))
    mobile_no=db.Column(db.BigInteger(),nullable=False)
    join_date=db.Column(db.Date(),nullable=False)
    is_leader=db.Column(db.Integer(),server_default='0')
    leader_id=db.Column(db.BigInteger())
    incharge_id=db.Column(db.BigInteger())
    status=db.Column(db.Integer(),nullable=False,server_default="0")
    last_status_change_date=db.Column(db.Date())
    comments=db.Column(db.String(255))
    nominee_name=db.Column(db.String(255))
    nominee_DOB=db.Column(db.Date())
    nominee_relation=db.Column(db.String(255))
    nominee_mobileno=db.Column(db.BigInteger())
    nominee_adhaarno=db.Column(db.BigInteger())
    created_on=db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<UserId:{self.id}>'
    
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
           "is_leader":self.is_leader,
           "leader_id":self.leader_id,
           "incharge_id":self.incharge_id
        }