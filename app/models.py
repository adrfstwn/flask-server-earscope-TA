from app import db

class EarScopeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    dissease_predict = db.Column(db.String(128), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<ExpresionData {self.expresion}>'