from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    foto_path = db.Column(db.String(255))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pessoa {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'foto_path': self.foto_path,
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M:%S')
        }