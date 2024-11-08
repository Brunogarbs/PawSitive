from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'elusively-concrete-boxer.data-1.use1.tembo.io',
    'database': 'pawsitivedb',
    'user': 'postgres',
    'password': 'dK7JKtOFOnaVTKHf'
}

def connect_db():
    conn = psycopg2.connect(**db_config)
    return conn

@app.route('/')
def home():
    return 'Bem-vindo ao servidor Flask!'

@app.route('/favicon.ico')
def favicon():
    return '', 204

# Rota de Cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    nome = data.get('nome')
    usuario = data.get('usuario')
    senha = data.get('senha')

    if not all([nome, usuario, senha]):
        return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

    conn = connect_db()
    cur = conn.cursor()

    try:
        hashed_password = generate_password_hash(senha)  # Hash da senha
        cur.execute("INSERT INTO users (nome, usuario, senha) VALUES (%s, %s, %s)", (nome, usuario, hashed_password))
        conn.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Rota do Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    senha = data.get('senha')

    conn = connect_db()
    cur = conn.cursor()

    try:
        # Obtém o hash da senha do banco de dados
        cur.execute("SELECT * FROM users WHERE usuario = %s", (usuario,))
        user = cur.fetchone()
        
        if user and check_password_hash(user[3], senha):  # Verifica a senha
            return jsonify({'message': 'Login bem-sucedido', 'user': {'id': user[0], 'nome': user[1], 'usuario': user[2]}}), 200
        else:
            return jsonify({'message': 'Usuário ou senha incorretos'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Rota Cadastrar Animais
@app.route('/cadastrar_animal', methods=['POST'])
def cadastrar_animal():
    data = request.json  # Obtém o JSON enviado
    id_usuario = data.get('id_usuario')
    animal = data.get('animal')
    sexo = data.get('sexo')
    cor = data.get('cor')
    localizacao = data.get('localizacao')
    foto = data.get('foto')
    observacoes = data.get('observacoes')

    if not id_usuario:
        return jsonify({'error': 'ID do usuário é obrigatório!'}), 400

    conn = connect_db()
    cur = conn.cursor()

    try:
        if foto:
            foto = foto.split(",")[1]  # Remove o prefixo 'data:image/png;base64,'
            foto_binario = base64.b64decode(foto)
        
        cur.execute("""
            INSERT INTO animals (id_usuario, animal, sexo, cor, localizacao, foto, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_usuario, animal, sexo, cor, localizacao, foto_binario, observacoes))
        
        conn.commit()
        return jsonify({'message': 'Animal cadastrado com sucesso!'}), 201
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar animal: {e}")
        return jsonify({'error': f'Ocorreu um erro no servidor: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/animais', methods=['GET'])
def get_animais():
    conn = connect_db()
    cur = conn.cursor()
    try:
        # Busca todos os animais com suas informações
        cur.execute("SELECT id_resgate, animal, sexo, cor, localizacao, observacoes, foto FROM animals")
        animais = cur.fetchall()

        # Formata os dados para envio como JSON
        animais_data = []
        for animal in animais:
            id_animal = animal[0]
            animal_nome = animal[1]
            sexo = animal[2]
            cor = animal[3]
            localizacao = animal[4]
            observacoes = animal[5]
            foto_base64 = base64.b64encode(animal[6]).decode('utf-8')  # Converte para base64
            
            animais_data.append({
                'id': id_animal,
                'nome': animal_nome,
                'sexo': sexo,
                'cor': cor,
                'localizacao': localizacao,
                'observacoes': observacoes,
                'foto': f"data:image/png;base64,{foto_base64}"
            })

        return jsonify(animais_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
