from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column( db.Integer, primary_key = True, autoincrement = True )
    nome = db.Column( db.String(100), nullable = False )
    descricao = db.Column( db.String(200), nullable = True )
    comprado = db.Column( db.Boolean, default=False )
    quantidade = db.Column(db.Integer, nullable=False, default=0 )

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'comprado': self.comprado,
            'quantidade': self.quantidade
        }