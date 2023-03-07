from main.extensions import db

class Pension(db.Model):
    id = db.Column(db.BigInteger(),nullable=False,primary_key=True)
    member_id=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id"),nullable=False)
    status=db.Column(db.Integer(),nullable=False,server_default="0")#0-pending,1-active,2-rejected,4-closed.
    pension_monthly=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    start_date=db.Column(db.Date())
    end_date=db.Column(db.Date())
    approved_by=db.Column(db.Integer())
    remarks=db.Column(db.String(150))
    created_on=db.Column(db.DateTime(),server_default=db.func.now())
    reference_no=db.Column(db.String(150))
    approval_no=db.Column(db.BigInteger(),db.ForeignKey("loan_request.id"))
    approved_on=db.Column(db.Date())
    issued_on=db.Column(db.Date())
    total_amount_issued=db.Column(db.Float(precision=32,decimal_return_scale=None))

    def __repr__(self):
        return f"<userid:{self.id}>"
    
class PensionPayment(db.Model):
    id=db.Column(db.BigInteger(),nullable=False,primary_key=True)
    member_id=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id"))
    pension_id=db.Column(db.BigInteger(),db.ForeignKey("pension.id"))
    month=db.Column(db.Integer(),nullable=False)
    year=db.Column(db.Integer(),nullable=False)
    paid_date=db.Column(db.Date())
    amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    created_on=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self) -> str:
        return f"<userid:{self.id}>"

