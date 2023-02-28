from main.extenstions import db

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
        return {
           "user_id":self.user_id,
           "name":self.name,
           "DOB":self.DOB,
           "image_path":self.image_path,
           "gender":self.gender,
           "address":self.address,
           "city":self.city,
           "district":self.district,
           "state":self.state,
           "pincode":self.pincode,
           "auth_type_id":self.auth_type_id,
           "auth_data":self.auth_data,
           "auth_path":self.auth_path,
           "mobile_no":self.mobile_no,
           "join_date":self.join_date,
           "is_leader":self.is_leader,
           "leader_id":self.leader_id,
           "incharge_id":self.incharge_id,
           "status":self.status,
           "last_status_change_date":self.last_status_change_date,
           "comments":self.comments,
           "nominee_name":self.nominee_name,
           "nominee_adhaarno":self.nominee_adhaarno,
           "nominee_DOB":self.nominee_DOB,
           "nominee_mobileno":self.nominee_mobileno,
           "nominee_relation":self.nominee_relation,
           "created_on":self.created_on
        }
