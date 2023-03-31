from main.extensions import db

class AccountClosing(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    member_id=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id"),nullable=False)
    status=db.Column(db.Integer(),server_default="0",nullable=False)
    closed_by=db.Column(db.Integer())
    closed_on=db.Column(db.Date())
    remarks=db.Column(db.String(150))
    created_on=db.Column(db.DateTime(),server_default=db.func.now())
    reference_no=db.Column(db.String(150))
    request_id=db.Column(db.BigInteger(),db.ForeignKey("loan_request.id"))

    def __repr__(self):
        return f"<userId:{self.id}"