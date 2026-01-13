# Plano Arquitetural - Tech Challenge 1 MLOPS

## 📐 Visão Geral da Arquitetura

Este documento detalha a arquitetura do sistema, o pipeline de dados, e o plano de escalabilidade e integração com Machine Learning.

## 🔄 Pipeline de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                        PIPELINE DE DADOS                         │
└─────────────────────────────────────────────────────────────────┘

1. INGESTÃO
   ┌─────────────────────┐
   │  books.toscrape.com │
   │   (Fonte Externa)   │
   └──────────┬──────────┘
              │
              │ HTTP Requests
              │ (BeautifulSoup)
              ▼
   ┌─────────────────────┐
   │  book_scraper.py    │
   │  (Web Scraping)     │
   └──────────┬──────────┘
              │
              │ Extração de dados
              │ (título, preço, rating, etc.)
              ▼
   ┌─────────────────────┐
   │   data/books.csv    │
   │  (Armazenamento)    │
   └──────────┬──────────┘

2. PROCESSAMENTO
              │
              │ Leitura via pandas
              ▼
   ┌─────────────────────┐
   │   api/main.py       │
   │  (Flask API)        │
   └──────────┬──────────┘
              │
              │ Transformação/Validação
              │ (Pydantic Models)
              ▼

3. API & CONSUMO
   ┌─────────────────────┐
   │   REST Endpoints    │
   │  (JSON Responses)   │
   └──────────┬──────────┘
              │
              ├──► Aplicações Web/Mobile
              ├──► Cientistas de Dados
              ├──► Modelos de ML
              └──► Dashboards/BI
```

## 🏗️ Arquitetura Detalhada

### Componentes Principais

#### 1. Camada de Ingestão (Data Ingestion)

**Responsabilidade:** Extrair dados da fonte externa

- **Tecnologia:** Python + BeautifulSoup + Requests
- **Script:** `book_scraper.py`
- **Processo:**
  1. Navegação por páginas do site
  2. Extração de dados de cada livro
  3. Requisições adicionais para obter detalhes (categoria, descrição)
  4. Persistência em CSV

**Características:**
- ✅ Tratamento de erros
- ✅ Rate limiting (time.sleep implícito)
- ✅ Paginação automática
- ✅ Extração de todos os campos obrigatórios

#### 2. Camada de Armazenamento (Storage)

**Responsabilidade:** Persistir dados extraídos

- **Formato:** CSV (atual)
- **Localização:** `data/books.csv`
- **Estrutura:**
  ```csv
  id,title,price,rating,availability,category,image,description
  ```

**Evolução Futura:**
- Migração para banco de dados (PostgreSQL, MongoDB)
- Implementação de cache (Redis)
- Armazenamento em cloud (S3, GCS)

#### 3. Camada de API (API Layer)

**Responsabilidade:** Expor dados através de endpoints RESTful

- **Framework:** Flask
- **Documentação:** Swagger (Flasgger)
- **Autenticação:** JWT (Flask-JWT-Extended)
- **Validação:** Pydantic Models

**Endpoints:**
- Core: Health, List, Get, Search, Categories
- Opcionais: Stats, Top Rated, Price Range
- ML-Ready: Features, Training Data, Predictions

#### 4. Camada de Consumo (Consumption)

**Responsabilidade:** Fornecer dados para diferentes consumidores

**Tipos de Consumidores:**
1. **Aplicações Web/Mobile:** JSON via REST
2. **Cientistas de Dados:** Endpoints específicos para ML
3. **Modelos de ML:** Features pré-processadas
4. **Dashboards:** Dados agregados (stats)

## 📈 Arquitetura para Escalabilidade

### Cenário Atual (MVP)

```
┌──────────────┐
│   Flask API  │
│  (Single)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  CSV File    │
│  (Local)     │
└──────────────┘
```

### Arquitetura Escalável (Futuro)

```
                    ┌─────────────┐
                    │  Load       │
                    │  Balancer   │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌────▼────┐
   │ Flask   │       │  Flask    │      │  Flask  │
   │ API #1  │       │  API #2   │      │  API #3 │
   └────┬────┘       └─────┬─────┘      └────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │   Redis     │
                    │   (Cache)   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ PostgreSQL  │
                    │  (Database) │
                    └─────────────┘
```

### Melhorias para Escalabilidade

1. **Horizontal Scaling**
   - Múltiplas instâncias da API
   - Load balancer (Nginx, AWS ALB)
   - Containerização (Docker, Kubernetes)

2. **Cache Layer**
   - Redis para queries frequentes
   - Cache de resultados de estatísticas
   - TTL configurável

3. **Database**
   - Migração de CSV para PostgreSQL/MongoDB
   - Índices para busca otimizada
   - Replicação para alta disponibilidade

4. **Message Queue**
   - RabbitMQ/Kafka para processamento assíncrono
   - Scraping em background
   - Notificações de atualizações

5. **Monitoring & Logging**
   - Prometheus + Grafana
   - ELK Stack (Elasticsearch, Logstash, Kibana)
   - APM (Application Performance Monitoring)

## 🔬 Cenário de Uso para Cientistas de Dados

### Workflow Típico

```
1. EXPLORAÇÃO DE DADOS
   ┌─────────────────────────┐
   │ GET /api/v1/books       │
   │ GET /api/v1/stats/...   │
   └──────────┬──────────────┘
              │
              ▼
2. EXTRAÇÃO DE FEATURES
   ┌─────────────────────────┐
   │ GET /api/v1/ml/features │
   └──────────┬──────────────┘
              │
              ▼
3. PREPARAÇÃO DO DATASET
   ┌─────────────────────────┐
   │ GET /api/v1/ml/         │
   │    training-data        │
   └──────────┬──────────────┘
              │
              ▼
4. TREINAMENTO DO MODELO
   ┌─────────────────────────┐
   │ Modelo ML (Python)      │
   │ - Feature Engineering   │
   │ - Model Training        │
   └──────────┬──────────────┘
              │
              ▼
5. DEPLOY DO MODELO
   ┌─────────────────────────┐
   │ POST /api/v1/ml/        │
   │    predictions          │
   └─────────────────────────┘
```

### Endpoints Específicos para ML

#### `/api/v1/ml/features`
- Retorna features numéricas e categóricas
- Pronto para feature engineering
- Formato padronizado

#### `/api/v1/ml/training-data`
- Dataset completo
- Formato JSON para fácil conversão
- Compatível com pandas, scikit-learn

#### `/api/v1/ml/predictions`
- Endpoint para receber predições
- Integração com modelos treinados
- Extensível para diferentes tipos de ML

## 🤖 Plano de Integração com Modelos de ML

### Fase 1: Preparação (Atual)
- ✅ Estrutura de dados padronizada
- ✅ Endpoints ML-ready
- ✅ Features extraídas

### Fase 2: Modelo de Predição de Preço
**Objetivo:** Prever preço baseado em características do livro

**Features:**
- Rating (1-5)
- Categoria (encoded)
- Disponibilidade (encoded)
- Título (TF-IDF ou embeddings)

**Endpoint:**
```
POST /api/v1/ml/predict/price
{
  "rating": 4,
  "category": "Fiction",
  "availability": "In stock"
}
```

### Fase 3: Sistema de Recomendação
**Objetivo:** Recomendar livros similares

**Features:**
- Embeddings de títulos
- Categoria
- Rating
- Preço

**Endpoint:**
```
GET /api/v1/ml/recommendations/{book_id}?limit=5
```

### Fase 4: Análise de Sentimento (Descrições)
**Objetivo:** Analisar sentimento das descrições

**Features:**
- Texto da descrição
- Título
- Categoria

**Endpoint:**
```
POST /api/v1/ml/sentiment
{
  "description": "..."
}
```

### Arquitetura de ML em Produção

```
┌─────────────────┐
│   Flask API     │
└────────┬────────┘
         │
         ├──► Model Serving
         │    ┌──────────────┐
         │    │  MLflow      │
         │    │  Model Store │
         │    └──────┬───────┘
         │           │
         │           ▼
         │    ┌──────────────┐
         │    │  TensorFlow  │
         │    │  Serving     │
         │    └──────────────┘
         │
         └──► Feature Store
              ┌──────────────┐
              │  Feast/      │
              │  Tecton      │
              └──────────────┘
```

## 🔄 Fluxo de Dados Completo

### 1. Ingestão Contínua
```
Schedule (Cron/APScheduler)
    │
    ▼
Trigger Scraping (POST /api/v1/scraping/trigger)
    │
    ▼
Execute book_scraper.py
    │
    ▼
Update data/books.csv
    │
    ▼
Notify API (Webhook/Event)
    │
    ▼
Invalidate Cache
```

### 2. Processamento de Requisições
```
Client Request
    │
    ▼
Load Balancer
    │
    ▼
Flask API Instance
    │
    ├──► Check Cache (Redis)
    │    │
    │    ├──► Hit: Return Cached
    │    └──► Miss: Continue
    │
    ▼
Read Data (CSV/DB)
    │
    ▼
Process & Transform
    │
    ▼
Validate (Pydantic)
    │
    ▼
Return JSON Response
    │
    ▼
Update Cache
```

## 📊 Métricas e Monitoramento

### Métricas de Negócio
- Total de livros indexados
- Taxa de atualização dos dados
- Categorias mais populares
- Preço médio por categoria

### Métricas Técnicas
- Latência de API (p50, p95, p99)
- Taxa de erro (4xx, 5xx)
- Throughput (requests/segundo)
- Uso de recursos (CPU, memória)

### Alertas
- API down
- Scraping falhou
- Alta latência
- Erro rate > 1%

## 🚀 Roadmap de Evolução

### Curto Prazo (1-2 meses)
- [ ] Migração para banco de dados
- [ ] Implementação de cache (Redis)
- [ ] Deploy em produção (Heroku/Render)
- [ ] Monitoramento básico

### Médio Prazo (3-6 meses)
- [ ] Containerização (Docker)
- [ ] CI/CD Pipeline
- [ ] Modelo ML de predição
- [ ] Testes automatizados

### Longo Prazo (6+ meses)
- [ ] Kubernetes deployment
- [ ] Feature Store
- [ ] Sistema de recomendação
- [ ] Análise de sentimento
- [ ] Dashboard de analytics

## 🔒 Segurança e Compliance

- **Autenticação:** JWT para endpoints protegidos
- **Rate Limiting:** Implementar para prevenir abuso
- **HTTPS:** Obrigatório em produção
- **Validação:** Input validation em todos os endpoints
- **Logging:** Logs estruturados (sem dados sensíveis)

## 📝 Conclusão

Esta arquitetura foi projetada para:
1. ✅ Atender requisitos atuais do Tech Challenge
2. ✅ Ser escalável para crescimento futuro
3. ✅ Facilitar integração com ML
4. ✅ Manter simplicidade inicial
5. ✅ Permitir evolução incremental

A arquitetura atual é um MVP funcional que pode evoluir gradualmente conforme as necessidades do projeto crescem.
