from main.extensions import db

class CategorySubcategory(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    TYPE=db.Column(db.String(199),nullable=False)
    CATEGORY=db.Column(db.String(199),nullable=False)
    SUBCATEGORY=db.Column(db.String(199),nullable=False,unique=True)

    def __repr__(self):
        return f"<userid:{self.id}>"
    
class BankAccounts(db.Model):
    id=db.Column(db.Integer(),nullable=False,primary_key=True)
    acc_number=db.Column(db.String(200),unique=True)
    account_name=db.Column(db.String(200))
    branch=db.Column(db.String(200))
    IFSC_code=db.Column(db.String(200))
    created_date=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self) :
        return f"<userid:{self.id}>"
