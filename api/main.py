import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity
)
import os
from flasgger import Swagger

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# Configuração de Autenticação (Desafio 1)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'sua-chave-secreta-super-segura') 
jwt = JWTManager(app)

# Configuração do Swagger (OpenAPI)
swagger = Swagger(app)

# Simulação de Base de Dados (Em produção, isso viria do CSV gerado pelo Web Scraping)
MOCK_DB = [
    {"id": 1, "title": "A Light in the Attic", "price": 51.77, "rating": 3, "availability": "In stock", "category": "Poetry"},
    {"id": 2, "title": "Tipping the Velvet", "price": 53.74, "rating": 1, "availability": "In stock", "category": "Historical Fiction"},
    {"id": 3, "title": "Soumission", "price": 50.10, "rating": 1, "availability": "In stock", "category": "Fiction"}
]

def get_data():
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'books.csv')
        if not os.path.exists(csv_path):
            csv_path = 'data/books.csv'
        df = pd.read_csv(csv_path)

        if 'id' not in df.columns:
            df['id'] = range(1, len(df) + 1)
        return df.to_dict(orient='records')
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        print(f"Erro ao ler CSV: {e}. Usando dados mock.")
        return MOCK_DB

# --- DESAFIOS ADICIONAIS - SISTEMA DE AUTENTICAÇÃO ---
# --- Desafio 1 ---
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Rota para obter token de acesso.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Tokens de acesso e refresh gerados com sucesso
      401:
        description: Usuário ou senha inválidos
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if username != 'admin' or password != 'admin':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token)

@app.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Rota para renovar token.
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Token renovado com sucesso
    """
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

# --- ENDPOINTS CORE ---
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    Verifica status da API e conectividade.
    ---
    responses:
      200:
        description: API operacional
    """
    return jsonify({"status": "ok", "message": "API is operational"}), 200

@app.route('/api/v1/books', methods=['GET'])
def list_books():
    """
    Lista todos os livros disponíveis na base de dados.
    ---
    responses:
      200:
        description: Lista de livros retornada com sucesso
    """
    return jsonify(get_data()), 200

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Retorna detalhes completos de um livro específico pelo ID.
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do livro
      404:
        description: Livro não encontrado
    """
    books = get_data()
    book = next((item for item in books if item["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"message": "Book not found"}), 404

@app.route('/api/v1/books/search', methods=['GET'])
def search_books():
    """
    Busca livros por título e/ou categoria.
    ---
    parameters:
      - name: title
        in: query
        type: string
      - name: category
        in: query
        type: string
    responses:
      200:
        description: Lista de livros encontrados
    """
    title_query = request.args.get('title', '').lower()
    category_query = request.args.get('category', '').lower()
    
    books = get_data()
    results = []
    
    for book in books:
        match_title = title_query in book['title'].lower() if title_query else True
        match_category = category_query in book['category'].lower() if category_query else True
        
        if match_title and match_category:
            results.append(book)
            
    return jsonify(results), 200

@app.route('/api/v1/categories', methods=['GET'])
def list_categories():
    """
    Lista todas as categorias de livros disponíveis.
    ---
    responses:
      200:
        description: Lista de categorias
    """
    books = get_data()
    categories = list(set([book['category'] for book in books]))
    return jsonify(categories), 200

# --- ENDPOINTS OPCIONAIS DA API ---

@app.route('/api/v1/stats/overview', methods=['GET'])
def stats_overview():
    """
    Estatísticas gerais da coleção.
    ---
    responses:
      200:
        description: Estatísticas gerais
    """
    df = pd.DataFrame(get_data())
    stats = {
        "total_books": int(len(df)),
        "average_price": float(df['price'].mean()),
        "average_rating": float(df['rating'].mean())
    }
    return jsonify(stats), 200

@app.route('/api/v1/stats/categories', methods=['GET'])
def stats_categories():
    """
    Estatísticas detalhadas por categoria.
    ---
    responses:
      200:
        description: Estatísticas por categoria
    """
    df = pd.DataFrame(get_data())
    cat_stats = df.groupby('category').agg({
        'title': 'count', 
        'price': 'mean'
    }).rename(columns={'title': 'count', 'price': 'avg_price'}).to_dict('index')
    return jsonify(cat_stats), 200

@app.route('/api/v1/books/top-rated', methods=['GET'])
def top_rated_books():
    """
    Lista os livros com melhor avaliação.
    ---
    responses:
      200:
        description: Livros com 5 estrelas
    """
    df = pd.DataFrame(get_data())
    # Assumindo rating máximo 5, filtra os maiores ratings
    top_books = df[df['rating'] == df['rating'].max()].to_dict(orient='records')
    return jsonify(top_books), 200

@app.route('/api/v1/books/price-range', methods=['GET'])
def price_range():
    """
    Filtra livros dentro de uma faixa de preço específica.
    ---
    parameters:
      - name: min
        in: query
        type: number
      - name: max
        in: query
        type: number
    responses:
      200:
        description: Livros na faixa de preço
    """
    min_price = float(request.args.get('min', 0))
    max_price = float(request.args.get('max', 1000))
    
    books = get_data()
    filtered = [b for b in books if min_price <= b['price'] <= max_price]
    return jsonify(filtered), 200

# --- ROTA PROTEGIDA (ADMIN) ---
@app.route('/api/v1/scraping/trigger', methods=['POST'])
@jwt_required()
def trigger_scraping():
    """
    Rota protegida para disparar o script de scraping.
    ---
    security:
      - Bearer: []
    responses:
      202:
        description: Processo iniciado
    """
    import subprocess
    import sys
    
    try:
        scraper_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'book_scraper.py')
        process = subprocess.Popen(
            [sys.executable, scraper_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return jsonify({
            "message": "Scraping process started successfully",
            "pid": process.pid,
            "status": "running"
        }), 202
    except Exception as e:
        return jsonify({
            "message": "Error starting scraping process",
            "error": str(e)
        }), 500

@app.route('/api/v1/scraping/logs', methods=['GET'])
def get_scraping_logs():
    """
    Retorna os logs do scraping em tempo real.
    ---
    parameters:
      - name: lines
        in: query
        type: integer
        description: Número de linhas a retornar (padrão: 50)
    responses:
      200:
        description: Logs do scraping
    """
    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'scraping.log')
    lines = request.args.get('lines', 50, type=int)
    
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                return jsonify({
                    "logs": recent_lines,
                    "total_lines": len(all_lines),
                    "status": "running" if len(recent_lines) > 0 and "concluído" not in recent_lines[-1].lower() else "completed"
                }), 200
        else:
            return jsonify({
                "logs": [],
                "total_lines": 0,
                "status": "not_started",
                "message": "Log file not found. Scraping may not have started yet."
            }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "logs": [],
            "status": "error"
        }), 500

# --- ENDPOINTS ML-READY (Desafio 2) ---

@app.route('/api/v1/ml/features', methods=['GET'])
def ml_features():
    """
    Dados formatados para features.
    ---
    responses:
      200:
        description: Features para ML
    """
    df = pd.DataFrame(get_data())
    features = df[['price', 'rating', 'category']].to_dict(orient='records')
    return jsonify(features), 200

@app.route('/api/v1/ml/training-data', methods=['GET'])
def ml_training_data():
    """
    Dataset completo pronto para treinamento.
    ---
    responses:
      200:
        description: Dados de treino
    """
    return jsonify(get_data()), 200

@app.route('/api/v1/ml/predictions', methods=['POST'])
def ml_predictions():
    """
    Endpoint para receber predições (placeholder).
    ---
    parameters:
      - name: body
        in: body
        required: true
    responses:
      200:
        description: Predição realizada
    """
    input_data = request.json
    prediction = {"predicted_rating": 4.5, "input": input_data}
    return jsonify(prediction), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)