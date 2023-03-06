from main.extensions import db

class BenefitType(db.Model):
    id=db.Column(db.Integer(),nullable=False,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    created_on=db.Column(db.DateTime(),server_default=db.func.now())

    def __repr__(self):
        return f"<userId:{self.id}"