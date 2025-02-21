from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config
from models.item import db
from routes.item import item_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

migrate= Migrate(app, db)

with app.app_context():
    db.create_all()

# bp = Blueprint('bp', __name__)

@app.route('/hello')
def hello():
    return jsonify({
        'message': 'Hello World!'
    })

# Registrando as rotas
app.register_blueprint(item_bp)

if __name__ == "__main__":
    app.run(debug=True)
