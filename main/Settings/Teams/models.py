from main.extensions import db

class Address(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    city=db.Column(db.String(100),nullable=False,unique=True)
    district=db.Column(db.String(100),nullable=False,unique=True)
    state=db.Column(db.String(100),nullable=False)
    country=db.Column(db.String(100))
    pincode=db.Column(db.Integer(),nullable=False)

    def __repr__(self) :
        return f"<userid:{self.id}>"