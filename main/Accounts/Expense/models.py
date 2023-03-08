from main.extensions import db

class Expense(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    paid_to=db.Column(db.String(100))
    ref_no=db.Column(db.String(100))
    category_id=db.Column(db.BigInteger(),db.ForeignKey('category_subcategory.id'),nullable=False)
    description=db.Column(db.String(100))
    paid_date=db.Column(db.Date())
    created_date=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self):
        return f"<userid:{self.id}>"
