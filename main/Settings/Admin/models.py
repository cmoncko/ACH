from main.extensions import db

class CompanyInfo(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    logo=db.Column(db.String(100))
    Address=db.Column(db.String(100),nullable=False)
    district=db.Column(db.String(100),nullable=False)
    state=db.Column(db.String(100),nullable=False)
    pincode=db.Column(db.Integer(),nullable=False)
    mobile_no=db.Column(db.BigInteger(),nullable=False)
    website=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"<userid:{self.id}>"
    
class UserRoleMapping(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    role_id=db.Column(db.Integer(),nullable=False)
    access=db.Column(db.String(100),nullable=False)

    def __repr__(self) :
        return f"<userid:{self.id}>"