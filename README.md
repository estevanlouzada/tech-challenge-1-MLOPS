# Tech Challenge 1 - MLOPS

## 📋 Descrição do Projeto

Este projeto implementa um sistema completo de **Web Scraping** e **API RESTful** para extrair, armazenar e disponibilizar dados de livros do site [Books to Scrape](https://books.toscrape.com/). O sistema foi desenvolvido com foco em MLOps, preparando a infraestrutura para integração futura com modelos de Machine Learning.

### Objetivos

- Extrair dados de livros de forma automatizada através de web scraping
- Armazenar dados em formato CSV para processamento
- Disponibilizar dados através de uma API RESTful documentada
- Preparar infraestrutura para integração com modelos de ML
- Implementar autenticação e endpoints protegidos

## 🏗️ Arquitetura

```
┌─────────────────┐
│  Web Scraping   │  Extrai dados de books.toscrape.com
│   (Script)      │  → Salva em CSV
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   data/books.csv│  Armazenamento local dos dados
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask API     │  API RESTful com Swagger
│   (main.py)     │  → Endpoints para consulta
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Consumidores   │  Aplicações, ML Models, etc.
│   (Clientes)     │
└─────────────────┘
```

### Componentes Principais

1. **Web Scraping** (`book_scraper.py`)
   - Extração automatizada de dados de livros
   - Navegação por páginas do site
   - Extração de: título, preço, rating, disponibilidade, categoria, imagem, descrição

2. **API RESTful** (`api/main.py`)
   - Framework: Flask
   - Documentação: Swagger (Flasgger)
   - Autenticação: JWT (Flask-JWT-Extended)
   - Endpoints core e opcionais implementados

3. **Armazenamento** (`data/books.csv`)
   - Dados estruturados em CSV
   - Pronto para processamento com pandas

## 📦 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd tech-challenge-1-MLOPS
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # No Windows
   venv\Scripts\activate
   
   # No Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o Web Scraping (opcional)**
   ```bash
   python book_scraper.py
   ```
   > **Nota:** O scraping pode levar alguns minutos. Os dados serão salvos em `data/books.csv`.

## 🚀 Execução

### Executar a API

```bash
cd api
python main.py
```

A API estará disponível em: `http://localhost:5000`

### Acessar a Documentação Swagger

Após iniciar a API, acesse:
- **Swagger UI:** `http://localhost:5000/apidocs/`

## 📚 Documentação das Rotas da API

### Endpoints Core (Obrigatórios)

#### 1. Health Check
```http
GET /api/v1/health
```

**Resposta:**
```json
{
  "status": "ok",
  "message": "API is operational"
}
```

#### 2. Listar Todos os Livros
```http
GET /api/v1/books
```

**Resposta:**
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    "price": 51.77,
    "rating": 3,
    "availability": "In stock",
    "category": "Poetry",
    "image": "http://books.toscrape.com/media/cache/...",
    "description": "..."
  },
  ...
]
```

#### 3. Obter Livro por ID
```http
GET /api/v1/books/{id}
```

**Exemplo:**
```http
GET /api/v1/books/1
```

**Resposta (200):**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "availability": "In stock",
  "category": "Poetry",
  "image": "http://books.toscrape.com/media/cache/...",
  "description": "..."
}
```

**Resposta (404):**
```json
{
  "message": "Book not found"
}
```

#### 4. Buscar Livros
```http
GET /api/v1/books/search?title={title}&category={category}
```

**Parâmetros:**
- `title` (opcional): Busca por título (case-insensitive)
- `category` (opcional): Busca por categoria (case-insensitive)

**Exemplos:**
```http
GET /api/v1/books/search?title=light
GET /api/v1/books/search?category=poetry
GET /api/v1/books/search?title=light&category=poetry
```

**Resposta:**
```json
[
  {
    "id": 1,
    "title": "A Light in the Attic",
    ...
  }
]
```

#### 5. Listar Categorias
```http
GET /api/v1/categories
```

**Resposta:**
```json
[
  "Poetry",
  "Historical Fiction",
  "Fiction",
  "Mystery",
  ...
]
```

### Endpoints Opcionais (Insights)

#### 6. Estatísticas Gerais
```http
GET /api/v1/stats/overview
```

**Resposta:**
```json
{
  "total_books": 1000,
  "average_price": 45.23,
  "average_rating": 3.5
}
```

#### 7. Estatísticas por Categoria
```http
GET /api/v1/stats/categories
```

**Resposta:**
```json
{
  "Poetry": {
    "count": 23,
    "avg_price": 51.77
  },
  "Fiction": {
    "count": 45,
    "avg_price": 48.12
  },
  ...
}
```

#### 8. Top Rated Books
```http
GET /api/v1/books/top-rated
```

**Resposta:**
```json
[
  {
    "id": 5,
    "title": "Book Title",
    "rating": 5,
    ...
  },
  ...
]
```

#### 9. Filtrar por Faixa de Preço
```http
GET /api/v1/books/price-range?min={min}&max={max}
```

**Exemplo:**
```http
GET /api/v1/books/price-range?min=20&max=50
```

**Resposta:**
```json
[
  {
    "id": 3,
    "title": "Book Title",
    "price": 45.50,
    ...
  },
  ...
]
```

### Endpoints de Autenticação

#### 10. Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 11. Refresh Token
```http
POST /api/v1/auth/refresh
Authorization: Bearer {refresh_token}
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Endpoints Protegidos

#### 12. Trigger Scraping (Admin)
```http
POST /api/v1/scraping/trigger
Authorization: Bearer {access_token}
```

**Resposta:**
```json
{
  "message": "Scraping process started successfully"
}
```

### Endpoints ML-Ready

#### 13. Features para ML
```http
GET /api/v1/ml/features
```

**Resposta:**
```json
[
  {
    "price": 51.77,
    "rating": 3,
    "category": "Poetry"
  },
  ...
]
```

#### 14. Training Data
```http
GET /api/v1/ml/training-data
```

**Resposta:** Dataset completo em formato JSON

#### 15. Predictions (Placeholder)
```http
POST /api/v1/ml/predictions
Content-Type: application/json

{
  "price": 50.0,
  "category": "Fiction"
}
```

**Resposta:**
```json
{
  "predicted_rating": 4.5,
  "input": {...}
}
```

## 📝 Exemplos de Uso

### Exemplo 1: Buscar livros com Python (requests)

```python
import requests

# Listar todos os livros
response = requests.get('http://localhost:5000/api/v1/books')
books = response.json()
print(f"Total de livros: {len(books)}")

# Buscar por título
response = requests.get('http://localhost:5000/api/v1/books/search?title=light')
results = response.json()
print(f"Livros encontrados: {len(results)}")

# Obter estatísticas
response = requests.get('http://localhost:5000/api/v1/stats/overview')
stats = response.json()
print(f"Preço médio: ${stats['average_price']:.2f}")
```

### Exemplo 2: Autenticação e acesso protegido

```python
import requests

# Login
login_response = requests.post(
    'http://localhost:5000/api/v1/auth/login',
    json={'username': 'admin', 'password': 'admin'}
)
tokens = login_response.json()
access_token = tokens['access_token']

# Acessar endpoint protegido
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.post(
    'http://localhost:5000/api/v1/scraping/trigger',
    headers=headers
)
print(response.json())
```

### Exemplo 3: Usando cURL

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Listar livros
curl http://localhost:5000/api/v1/books

# Buscar livros
curl "http://localhost:5000/api/v1/books/search?title=light&category=poetry"

# Estatísticas
curl http://localhost:5000/api/v1/stats/overview

# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

## 🔧 Estrutura do Projeto

```
tech-challenge-1-MLOPS/
├── api/
│   ├── main.py              # API Flask principal
│   └── schema/
│       └── book.py           # Modelos Pydantic
├── data/
│   └── books.csv            # Dados extraídos (gerado pelo scraping)
├── book_scraper.py          # Script de web scraping
├── requirements.txt         # Dependências do projeto
├── README.md               # Este arquivo
└── LICENSE                 # Licença do projeto
```

## 🚢 Deploy

### Deploy no Heroku

1. **Instale o Heroku CLI**
2. **Crie um Procfile** (já incluído no projeto):
   ```
   web: gunicorn api.main:app
   ```
3. **Configure variáveis de ambiente:**
   ```bash
   heroku config:set JWT_SECRET_KEY=sua-chave-secreta-super-segura
   ```
4. **Faça o deploy:**
   ```bash
   heroku create nome-da-app
   git push heroku main
   ```

### Deploy no Render

1. Conecte seu repositório GitHub ao Render
2. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn api.main:app`
3. Adicione variável de ambiente `JWT_SECRET_KEY`

## 🔐 Segurança

- **JWT Secret Key:** Configure uma chave segura em produção
- **Autenticação:** Endpoints protegidos requerem token JWT válido
- **CORS:** Configurado para permitir requisições cross-origin

## 📊 Dados Extraídos

O web scraping extrai os seguintes campos de cada livro:

- **id**: Identificador único
- **title**: Título do livro
- **price**: Preço (em libras esterlinas)
- **rating**: Avaliação (1-5 estrelas)
- **availability**: Disponibilidade em estoque
- **category**: Categoria do livro
- **image**: URL da imagem de capa
- **description**: Descrição do livro

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

## 👤 Autor

Tech Challenge 1 - FIAP MLOPS

---

**Nota:** Para mais detalhes sobre a arquitetura e pipeline de dados, consulte o documento `ARQUITETURA.md`.
