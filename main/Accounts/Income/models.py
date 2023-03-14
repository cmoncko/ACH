from main.extensions import db

class Income(db.Model):
    id=db.Column(db.BigInteger(),nullable=False,primary_key=True)
    amount=db.Column(db.Float(precision=32,decimal_return_scale=None))
    received_from=db.Column(db.String(100))
    ref_no=db.Column(db.String(100))
    category_id=db.Column(db.Integer(),db.ForeignKey("master_data.id"),nullable=False)
    description=db.Column(db.String(199))
    received_date=db.Column(db.Date(),nullable=False)
    created_date=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self) :
        return f"<userid:{self.id}>"
