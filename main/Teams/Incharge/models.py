from main.extenstions import db

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


