Tech Challenge

Tech Challenge é o projeto da fase que englobará os conhecimentos
obtidos em todas as disciplinas da fase. Esta é uma atividade que, a princípio,
deve ser desenvolvida em grupo. Importante atentar-se ao prazo de entrega,
pois trata-se de uma atividade obrigatória, uma vez que sua pontuação se refere
a 90% da nota final.

O problema

Desafio: Criação de uma API Pública para Consulta de Livros
Você foi contratado(a) como Engenheiro(a) de Machine Learning para um
projeto de recomendação de livros. A empresa está em sua fase inicial e ainda
não possui uma base de dados estruturada.
Seu primeiro desafio será montar a infraestrutura de extração,
transformação e disponibilização de dados via API pública para que cientistas de
dados e serviços de recomendação possam usar esses dados com facilidade.
Assim, seu objetivo será desenvolver um pipeline completo de dados e
uma API pública para servir esses dados, pensando na escalabilidade e
reusabilidade futura em modelos de machine learning.

Entregáveis Obrigatórios

1. Repositório do GitHub Organizado
• Código estruturado em módulos (scripts/, api/, data/, etc.).
• README completo contendo:
o Descrição do projeto e arquitetura.
o Instruções de instalação e configuração.
o Documentação das rotas da API.
o Exemplos de chamadas com requests/responses.
o Instruções para execução.
Tech Challenge

2. Sistema de Web Scraping
• Script automatizado para extrair dados de https://books.toscrape.com/
• Dados armazenados localmente em um arquivo CSV.
• Script executável e bem documentado.

3. API RESTful Funcional
• API implementada em Flask ou FastAPI.
• Endpoints obrigatórios (listados a seguir).
• Documentação da API (Swagger).

4. Deploy Público
• API deployada em Heroku, Render, Vercel, Fly.io ou similar.
• Link compartilhável funcional.
• API totalmente operacional no ambiente de produção.

5. Plano Arquitetural
• Diagrama ou documento detalhando:
o Pipeline desde ingestão → processamento → API → consumo.
o Arquitetura pensada para escalabilidade futura.
o Cenário de uso para cientistas de dados/ML.
o Plano de integração com modelos de ML.

6. Vídeo de Apresentação (3-12 minutos)
• Demonstração técnica (no macro apenas, sem aprofundamento).
• Apresentação da arquitetura e pipeline de dados.
• Execução de chamadas reais à API em produção.
• Comentários sobre boas práticas implementadas.

Tech Challenge

Objetivos Técnicos Core
Web Scraping Robusto
• Extrair todos os livros disponíveis no site.
• Capturar: título, preço, rating, disponibilidade, categoria, imagem.
Endpoints Obrigatórios da API
Endpoints Core
• GET /api/v1/books: lista todos os livros disponíveis na base de dados.
• GET /api/v1/books/{id}: retorna detalhes completos de um livro
específico pelo ID.
• GET /api/v1/books/search?title={title}&category={category}: busca
livros por título e/ou categoria.
• GET /api/v1/categories: lista todas as categorias de livros disponíveis.
• GET /api/v1/health: verifica status da API e conectividade com os
dados.
Endpoints Opcionais da API
Endpoints de Insights
• GET /api/v1/stats/overview: estatísticas gerais da coleção (total de
livros, preço médio, distribuição de ratings).
• GET /api/v1/stats/categories: estatísticas detalhadas por categoria
(quantidade de livros, preços por categoria).
• GET /api/v1/books/top-rated: lista os livros com melhor avaliação
(rating mais alto).
• GET /api/v1/books/price-range?min={min}&max={max}: filtra livros
dentro de uma faixa de preço específica.
Desafios Adicionais (Bônus)
Desafio 1: Sistema de Autenticação
Implementar JWT Authentication para proteger rotas sensíveis:
Tech Challenge
• POST /api/v1/auth/login - obter token.
• POST /api/v1/auth/refresh - renovar token.
• Proteger endpoints de admin como /api/v1/scraping/trigger.
Desafio 2: Pipeline ML-Ready
Criar endpoints pensados para consumo de modelos ML:
• GET /api/v1/ml/features - dados formatados para features.
• GET /api/v1/ml/training-data - dataset para treinamento.
• POST /api/v1/ml/predictions - endpoint para receber predições.
Desafio 3: Monitoramento & Analytics
• Logs estruturados de todas as chamadas.
• Métricas de performance da API.
• Dashboard simples de uso (Streamlit recomendado).
Lembre-se de que você poderá apresentar o desenvolvimento do seu
projeto durante as lives com professores(as). Essa é uma boa oportunidade para
discutir as dificuldades encontradas e pegar dicas valiosas com docentes
especialistas e colegas de turma.
Entrega
Subir na plataforma um arquivo no formato .txt com o repositório do seu
github, em que o arquivo README deve conter:
• Descrição completa do projeto (objetivos, como reproduzir, descrição
dos endpoints e afins).
• Link do deploy.
• Link do vídeo.
• -Diagrama (arquitetura) visual do projeto
Tech Challenge
E tem um plus para fortalecer seu aprendizado e ainda ganhar pontos na
nota!
Para dar um up nas suas certificações e ainda ganhar 10 pontos na nota
desse Tech Challenge da Fase 1, desafiamos você a realizar também nessa
fase o curso "Beginner: Introduction to Generative AI Learning Path" da
Google Cloud Skill Boost.
Ganhe o selo de habilidade avançada concluindo o curso, em que você
aprende uma visão geral dos conceitos de Generative AI, desde os fundamentos
de grandes modelos de linguagem até os princípios de responsible AI. Bora
aprender e ainda garantir esses pontos?
Não se esqueça de marcar o time acadêmico para celebrar suas
conquistas no Linkedin. Essa entrega não é obrigatória, mas esses pontos
podem te ajudar na compor a nota, caso não atinja a totalidade da nota nessa
fase.
Passo a passo para conquistar 10 pontinhos no Tech Challenge da Fase
1
Para ganhar os 10 pontos na nota do Tech Challenge, envie para nós um
comprovante de conclusão do curso anexado junto aos entregáveis desse
desafio! Para Fazer o curso, é necessário primeiro realizar o seu cadastro no
programa Google Cloud Career Launchpad, seguindo o passo a passo desse
documento aqui. Depois de se cadastrar no programa, responda esse formulário
para capturarmos o e-mail e RM de vocês e enviarmos o convite do curso!
Após o cadastro no programa e receber o convite de acesso, busque pelo
curso em Explore por "Beginner: Introduction to Generative AI Learning
Path", conforme a figura a seguir:
Tech Challenge
No final após encerrar a conclusão desse curso, clique no seu perfil e
acesse a parte de “Settings”:
E ative a opção “Make profile public”:
Tech Challenge
Agora você consegue compartilhar as suas certificações da Google e suas
badges conquistadas! Adicione seu perfil na entrega do Tech Challenge para
ganhar 10 pontos. Lembrando que se estiver fazendo o Tech Challenge em
grupo, todos os(as) integrantes devem enviar suas badges na entrega.
Não se esqueçam de que o Tech Challenge é um entregável
obrigatório! Se atentem para o prazo de entrega até o final da fase.
Boa sorte!