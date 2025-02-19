from app import db

class ExpresionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    expresion = db.Column(db.String(128), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<ExpresionData {self.expresion}>'