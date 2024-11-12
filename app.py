from flask import Flask, request, jsonify, render_template, Response, redirect,url_for, session
from flask_cors import CORS
import base64
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='/static')
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


# Rota para alterar a senha
@app.route('/alterar_senha', methods=['POST'])
def alterar_senha():
    dados = request.get_json()
    usuario = dados.get('usuario')
    senha_atual = dados.get('senha_atual')
    nova_senha = dados.get('nova_senha')

    # Conectar ao banco de dados
    conn = connect_db()
    cur = conn.cursor()

    # Verificar se a senha atual está correta
    cur.execute("SELECT senha FROM users WHERE usuario = %s", (usuario,))
    senha_bd = cur.fetchone()

    if senha_bd and check_password_hash(senha_bd[0], senha_atual):
        # Gerar o hash da nova senha
        nova_senha_hash = generate_password_hash(nova_senha)

        # Atualizar a senha no banco de dados
        cur.execute("UPDATE users SET senha = %s WHERE usuario = %s", (nova_senha_hash, usuario))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Senha alterada com sucesso!"}), 200
    else:
        cur.close()
        conn.close()
        return jsonify({"message": "Senha atual incorreta!"}), 400

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

# Rota para listar os animais cadastrados
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
            foto = animal[6]  # A foto é armazenada em formato binário no banco
            
            # Verificando se a foto existe antes de tentar convertê-la
            if foto:
                foto_base64 = base64.b64encode(foto).decode('utf-8')  # Converte para base64
                foto_data_uri = f"data:image/png;base64,{foto_base64}"
            else:
                foto_data_uri = None  # Caso não haja foto, o campo será None
            
            # Monta o dicionário com os dados do animal
            animais_data.append({
                'id': id_animal,
                'nome': animal_nome,
                'sexo': sexo,
                'cor': cor,
                'localizacao': localizacao,
                'observacoes': observacoes,
                'foto': foto_data_uri
            })

        return jsonify(animais_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route('/listar_animais/<user_logado>', methods=['GET'])
def listar_animais(user_logado):
    # Verifica se o 'user_logado' foi passado como parte da URL
    try:
        user_logado = int(user_logado)  # Tenta converter o user_logado para um inteiro
    except ValueError:
        return jsonify({'error': 'ID de usuário inválido'}), 400

    if not user_logado:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    conn = connect_db()
    cur = conn.cursor()
    try:
        # Busca todos os animais com as informações do usuário logado
        cur.execute("SELECT id_resgate, animal, sexo, cor, localizacao, observacoes, foto FROM animals WHERE id_usuario = %s", (user_logado,))
        animais = cur.fetchall()

        animais_data = []
        for animal in animais:
            id_animal = animal[0]
            animal_nome = animal[1]
            sexo = animal[2]
            cor = animal[3]
            localizacao = animal[4]
            observacoes = animal[5]
            foto = animal[6]
            
            # Verificando se a foto existe antes de tentar convertê-la
            if foto:
                foto_base64 = base64.b64encode(foto).decode('utf-8')
                foto_data_uri = f"data:image/png;base64,{foto_base64}"
            else:
                foto_data_uri = None
            
            # Monta o dicionário com os dados do animal
            animais_data.append({
                'id': id_animal,
                'nome': animal_nome,
                'sexo': sexo,
                'cor': cor,
                'localizacao': localizacao,
                'observacoes': observacoes,
                'foto': foto_data_uri
            })

        return jsonify(animais_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()



@app.route('/remover-animal/<int:id>', methods=['DELETE'])
def remover_animal(id):
    try:
        conn = connect_db()
        cur = conn.cursor() 

        # Deleta o animal pelo ID
        cur.execute("DELETE FROM animals WHERE id_resgate = %s", (id,))
        conn.commit()

        cur.close()
        conn.close()

        return '', 204  # Retorna status 204 (sem conteúdo) após a remoção
    except Exception as e:
        print(f"Erro ao remover animal: {e}")
        return 'Erro ao remover animal', 500
    
# Rota principal para renderizar index.html com dados dos animais
@app.route('/')
def index():
    # Chama a função get_animais para obter os dados
    response, status_code = get_animais()

    # Se houver erro, renderiza uma mensagem de erro
    if status_code != 200:
        return render_template('index.html', error="Erro ao carregar dados dos animais.")

    # Renderiza a página inicial com os dados dos animais
    return render_template('index.html', animais=response.get_json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
