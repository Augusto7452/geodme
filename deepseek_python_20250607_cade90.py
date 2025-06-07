from flask import Blueprint, request, jsonify, redirect, url_for, current_app
import os
from werkzeug.utils import secure_filename
from src.models.pessoa import db, Pessoa

pessoas_bp = Blueprint('pessoas', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@pessoas_bp.route('/pessoas', methods=['GET'])
def listar_pessoas():
    pessoas = Pessoa.query.all()
    return jsonify([pessoa.to_dict() for pessoa in pessoas])

@pessoas_bp.route('/pessoa', methods=['POST'])
def adicionar_pessoa():
    try:
        nome = request.form.get('nome')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        if not nome or not latitude or not longitude:
            return jsonify({'erro': 'Campos obrigatórios não preenchidos'}), 400
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'erro': 'Coordenadas inválidas'}), 400
        
        foto_path = None
        
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto and allowed_file(foto.filename):
                filename = secure_filename(foto.filename)
                foto_path = os.path.join('uploads', filename)
                foto.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        nova_pessoa = Pessoa(
            nome=nome,
            latitude=latitude,
            longitude=longitude,
            foto_path=foto_path
        )
        
        db.session.add(nova_pessoa)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao adicionar pessoa: {str(e)}')
        return jsonify({'erro': 'Erro interno no servidor'}), 500

# ... (manter as outras rotas como no original, com tratamento similar de erros)