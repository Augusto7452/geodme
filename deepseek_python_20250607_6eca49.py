from flask import Flask, render_template
from src.models.pessoa import db
from src.routes.pessoas import pessoas_bp
import os
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa o banco de dados
    db.init_app(app)
    
    # Registra blueprints
    app.register_blueprint(pessoas_bp)
    
    # Cria as tabelas
    with app.app_context():
        db.create_all()
        # Garante que a pasta de uploads existe
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Rota principal
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Tratamento de erros
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])