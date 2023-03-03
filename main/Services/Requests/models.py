from main.extensions import db

class LoanRequest(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    requested_by=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id"),nullable=False)
    loan_amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    number_of_emi=db.Column(db.Integer())
    EMI_amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    interest_rate=db.Column(db.Float(precision=32,decimal_return_scale=None))
    final_payable_amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    request_loan_type=db.Column(db.Integer(),nullable=False,server_default="0")#Savings-0 ,1-business,2-educaton,3-benefits and 4=pension.
    appied_on=db.Column(db.Date(),nullable=False)
    status=db.Column(db.Integer(),nullable=False,server_default="0")#0=pending,1=approved and 2=rejected.
    approved_on=db.Column(db.Date())
    comments=db.Column(db.String(200))
    action_by_user=db.Column(db.Integer())
    created_on=db.Column(db.DateTime(),server_default=db.func.now())
    pension_monthly_amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    benefit_type_id=db.Column(db.Integer())

    def __repr__(self) -> str:
        return f"<userid:{self.id}>"

