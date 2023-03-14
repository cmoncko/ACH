from main.extensions import db

class BankTransactions(db.Model):
    id=db.Column(db.BigInteger(),nullable=False,primary_key=True)
    bank_id=db.Column(db.Integer(),db.ForeignKey("bank_accounts.id"),nullable=False)
    transfer_type=db.Column(db.String(100))
    transaction_type=db.Column(db.Integer(),server_default="0")
    transaction_date=db.Column(db.Date(),nullable=False)
    amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    balance=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    deposited_by=db.Column(db.String(200))
    reference_no=db.Column(db.String(200))
    comments=db.Column(db.String(200))
    created_on=db.Column(db.DateTime(),server_default=db.func.now())
    
    def __repr__(self):
        return f"<userid:{self.id}>"
