from main.extensions import db

class Benefits(db.Model):
    id =db.Column(db.BigInteger(),nullable=False,primary_key=True)
    member_id=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id"),nullable=False)
    status=db.Column(db.Integer(),nullable=False,server_default='0')#0=pending,1=approved and 2=Rejected.
    benefit_type_id=db.Column(db.Integer(),db.ForeignKey("benefit_type.id"),nullable=False)
    approved_on=db.Column(db.Date(),nullable=False)
    approved_by=db.Column(db.Integer())
    issued_on=db.Column(db.Date())
    remarks=db.Column(db.String(150))
    created_on=db.Column(db.DateTime(),server_default=db.func.now())
    reference_no=db.Column(db.String(150))
    approval_no=db.Column(db.BigInteger(),db.ForeignKey("loan_request.id"))


    def __repr__(self) :
        return f"<userId:{self.id}"
