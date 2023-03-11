from main.extensions import db

class Savings(db.Model):
    id=db.Column(db.BigInteger(),nullable=False,primary_key=True)
    member_id=db.Column(db.BigInteger(),nullable=False)
    transaction_date=db.Column(db.Date(),nullable=False)
    year=db.Column(db.Integer())
    month=db.Column(db.Integer())
    week=db.Column(db.Integer())
    transaction_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    transaction_type=db.Column(db.Integer(),server_default='0',nullable=False)
    final_balance=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    created_on=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self):
        return f"<userId:{self.id}"
