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
    
class AppUser(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    name=db.Column(db.String(70),nullable=True)
    role_id=db.Column(db.Integer(),db.ForeignKey("user_role_mapping.id"),nullable=False)
    user_name=db.Column(db.String(70),unique=True,nullable=False)
    image_path=db.Column(db.String(255))
    encrypted_password=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    mobile=db.Column(db.BigInteger(),unique=True,nullable=False)
    created_on=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self):
        return f"<userid:{self.id}>"
    
class UserRoleMapping(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    role=db.Column(db.String(70),nullable=False)
    access=db.Column(db.String(350),nullable=False)

    def __repr__(self) :
        return f"<userid:{self.id}>"