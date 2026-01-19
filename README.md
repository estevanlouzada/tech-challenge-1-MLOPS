# Tech Challenge 1 - MLOPS

Sistema completo de **Web Scraping** e **API RESTful** para extrair, armazenar e disponibilizar dados de livros do site [Books to Scrape](https://books.toscrape.com/). Desenvolvido com foco em MLOps.

## 🌐 Links de Produção

- **API:** https://tech-challenge-mlops-api.onrender.com
- **Dashboard:** https://tech-challenge-mlops-dashboard.onrender.com
- **Swagger:** https://tech-challenge-mlops-api.onrender.com/apidocs/

### ⚠️ Plano Free do Render

A plataforma está deployada na **versão free do Render**:
- Serviços podem "dormir" após 15 minutos de inatividade
- Primeira requisição pode levar 30-60s para "acordar"
- **Sempre acorde a API primeiro**: `https://tech-challenge-mlops-api.onrender.com/api/v1/health`

## 🧪 Testando Online (Produção)

1. **Acorde a API**: https://tech-challenge-mlops-api.onrender.com/api/v1/health
   - Aguarde a resposta (30-60s na primeira vez)

2. **Acesse o Dashboard**: https://tech-challenge-mlops-dashboard.onrender.com
   - Explore: estatísticas, livros, scraping, busca

3. **Teste com Postman**: 
   - Importe `Postman_Collection.json`
   - Execute "Login" para obter token (salvo automaticamente)
   - Teste todos os endpoints

4. **Documentação Swagger**: https://tech-challenge-mlops-api.onrender.com/apidocs/
   - Teste endpoints diretamente no navegador

## 📚 Rotas da API

### Core (Obrigatórios)
- `GET /api/v1/health` - Health check
- `GET /api/v1/books` - Lista todos os livros
- `GET /api/v1/books/{id}` - Detalhes de um livro
- `GET /api/v1/books/search?title={title}&category={category}` - Busca
- `GET /api/v1/categories` - Lista categorias

### Opcionais
- `GET /api/v1/stats/overview` - Estatísticas gerais
- `GET /api/v1/stats/categories` - Estatísticas por categoria
- `GET /api/v1/books/top-rated` - Top rated
- `GET /api/v1/books/price-range?min={min}&max={max}` - Filtrar por preço

### Autenticação
- `POST /api/v1/auth/login` - Obter token (admin/admin)
- `POST /api/v1/auth/refresh` - Renovar token

### Protegidos (requerem token)
- `POST /api/v1/scraping/trigger` - Iniciar scraping
- `DELETE /api/v1/scraping/delete-csv` - Deletar CSV
- `GET /api/v1/scraping/logs` - Logs do scraping

### ML-Ready
- `GET /api/v1/ml/features` - Features para ML
- `GET /api/v1/ml/training-data` - Dataset para treino
- `POST /api/v1/ml/predictions` - Predições

## 🚀 Instalação e Teste Local

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd tech-challenge-1-MLOPS

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Execute scraping (opcional)
python book_scraper.py

# Execute API
cd api && python main.py
```

**URLs locais:**
- API: `http://localhost:5000`
- Swagger: `http://localhost:5000/apidocs/`

**Para testar localmente com Postman:**
- Altere a variável `base_url` na collection para: `http://localhost:5000`

## 🏗️ Estrutura

```
tech-challenge-1-MLOPS/
├── api/main.py          # API Flask
├── book_scraper.py      # Web scraping
├── dashboard.py         # Dashboard Streamlit
├── data/books.csv       # Dados extraídos
└── requirements.txt     # Dependências
```

## 📊 Dados Extraídos

**id**, **title**, **price**, **rating**, **availability**, **category**, **image**, **description**

## 🔐 Segurança

- JWT Authentication para endpoints protegidos
- Credenciais padrão: `admin` / `admin` (altere em produção)
- Configure `JWT_SECRET_KEY` como variável de ambiente

## 📖 Documentação Completa

- **Swagger UI**: https://tech-challenge-mlops-api.onrender.com/apidocs/
- **Arquitetura**: Consulte `ARQUITETURA.md`

---

**Tech Challenge 1 - FIAP MLOPS**
