from main.extensions import db

class BusinessLoans(db.Model):
    id = db.Column(db.BigInteger(),nullable=False,primary_key=True)
    member_id=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id"),nullable=False)
    status=db.Column(db.Integer(),nullable=False,server_default="0")
    loan_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    EMI_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    monthly_penalty_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)  
    number_of_emi=db.Column(db.Integer(),nullable=False)
    EMI_start_date=db.Column(db.Date(),nullable=False)
    loan_end_date=db.Column(db.Date(),nullable=False)
    comments=db.Column(db.String(200))
    loan_approved_by=db.Column(db.Integer())
    loan_approved_date=db.Column(db.Date())
    ref_no=db.Column(db.String(100))
    approval_no=db.Column(db.BigInteger(),db.ForeignKey("loan_request.id"))
    issued_on=db.Column(db.Date())
    created_on=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self):
        return f"<userid:{self.id}>"

class BusinessLoanPayment(db.Model):
    id=db.Column(db.BigInteger(),nullable=False,primary_key=True)
    member_id=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id"),nullable=False)
    loan_id=db.Column(db.BigInteger(),db.ForeignKey("business_loans.id"),nullable=False)
    status=db.Column(db.Integer(),server_default="0")
    month=db.Column(db.Integer(),nullable=False)
    year=db.Column(db.Integer(),nullable=False)
    emi_count=db.Column(db.Integer(),nullable=False)
    paid_date=db.Column(db.Date())
    amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    penalty_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),server_default="0")
    total_amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    created_on=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self):
        return f"<userid:{self.id}>"
