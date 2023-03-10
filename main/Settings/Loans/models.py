from main.extensions import db

class LoanCriteria(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    minimum_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    maximum_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    loan_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)

    def __repr__(self):
        return f"<userid:{self.id}>"