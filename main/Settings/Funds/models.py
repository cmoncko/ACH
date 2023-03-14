from main.extensions import db

class MasterData(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    property=db.Column(db.String(191))
    value=db.Column(db.String(500))

    def __repr__(self):
        return f"<userid:{self.id}>"
