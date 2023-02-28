from main import db

class SanthaPayments(db.Model):
    id=db.Column(db.BigInteger(),nullable=False,primary_key=True)
    member_id=db.Column(db.BigInteger(),nullable=False)
    santha_for_year=db.Column(db.Integer(),nullable=False)
    santha_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    received_amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    received_date=db.Column(db.Date())
    created_on=db.Column(db.DateTime(),server_default=db.func.now())


    def __repr__(self):
        return f"<userId:{self.id}"