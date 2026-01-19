import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

# Configuração da página
st.set_page_config(
    page_title="Books API Dashboard",
    page_icon="📚",
    layout="wide"
)

# Título principal
st.title("📚 Books API Dashboard")
st.markdown("---")

# Configuração da URL da API
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5001')
if 'api_url' not in st.session_state:
    st.session_state.api_url = API_BASE_URL

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    api_url = st.text_input("URL da API", value=st.session_state.api_url)
    st.session_state.api_url = api_url

# Função para fazer requisições à API
def fetch_data(endpoint):
    """Faz requisição à API e retorna os dados"""
    try:
        response = requests.get(f"{st.session_state.api_url}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Erro {response.status_code}"
    except requests.exceptions.RequestException as e:
        return None, f"Erro de conexão: {str(e)}"

# Verificar saúde da API
health_data, health_error = fetch_data("/api/v1/health")
if health_error:
    st.error(f"❌ API offline: {health_error}")
    st.stop()
else:
    st.success("🟢 API Online")

st.markdown("---")

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "📖 Livros", "🔐 Scraping", "🔍 Busca"])

# Tab 1: Visão Geral
with tab1:
    st.header("📊 Estatísticas Gerais")
    
    stats_data, stats_error = fetch_data("/api/v1/stats/overview")
    
    if stats_error:
        st.error(f"Erro: {stats_error}")
    elif stats_data:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Livros", f"{stats_data.get('total_books', 0):,}")
        with col2:
            st.metric("Preço Médio", f"£{stats_data.get('average_price', 0):.2f}")
        with col3:
            st.metric("Rating Médio", f"{stats_data.get('average_rating', 0):.2f}")
        
        # Gráfico simples
        books_data, _ = fetch_data("/api/v1/books")
        if books_data:
            df = pd.DataFrame(books_data)
            if 'rating' in df.columns:
                rating_counts = df['rating'].value_counts().sort_index()
                fig = px.bar(
                    x=rating_counts.index,
                    y=rating_counts.values,
                    labels={'x': 'Rating', 'y': 'Quantidade'},
                    title="Distribuição de Ratings"
                )
                st.plotly_chart(fig, use_container_width=True)

# Tab 2: Livros
with tab2:
    st.header("📖 Catálogo de Livros")
    
    books_data, books_error = fetch_data("/api/v1/books")
    
    if books_error:
        st.error(f"Erro: {books_error}")
    elif books_data:
        df = pd.DataFrame(books_data)
        
        # Filtros simples
        col1, col2 = st.columns(2)
        with col1:
            if 'category' in df.columns:
                categories = ['Todas'] + sorted(df['category'].dropna().unique().tolist())
                selected_category = st.selectbox("Categoria", categories, key="filter_category")
            else:
                selected_category = 'Todas'
        
        with col2:
            if 'price' in df.columns:
                min_price = float(df['price'].min())
                max_price = float(df['price'].max())
                price_range = st.slider("Faixa de Preço", min_price, max_price, (min_price, max_price))
            else:
                price_range = (0, 1000)
        
        # Aplicar filtros
        filtered_df = df.copy()
        if selected_category != 'Todas' and 'category' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['category'] == selected_category]
        if 'price' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['price'] >= price_range[0]) & 
                (filtered_df['price'] <= price_range[1])
            ]
        
        st.info(f"Mostrando {len(filtered_df)} de {len(df)} livros")
        
        # Opção para exibir imagens
        show_images = st.checkbox("🖼️ Exibir imagens", value=False, key="show_images")
        
        if show_images and 'image' in filtered_df.columns:
            # Começar com 5 livros
            if 'items_to_show' not in st.session_state:
                st.session_state.items_to_show = 5
            
            display_df = filtered_df.head(st.session_state.items_to_show)
            
            # Grid simples de imagens
            cols = st.columns(5)
            for idx, (_, book) in enumerate(display_df.iterrows()):
                col = cols[idx % 5]
                with col:
                    image_url = book.get('image', '')
                    if image_url:
                        st.image(image_url)
                    st.caption(f"{book.get('title', '')[:20]} - £{book.get('price', 0):.2f}")
            
            # Botão para mostrar mais
            if len(filtered_df) > st.session_state.items_to_show:
                if st.button("➕ Mostrar mais", key="show_more"):
                    st.session_state.items_to_show += 5
                    st.rerun()
        else:
            # Tabela (modo padrão)
            if 'id' in filtered_df.columns and 'title' in filtered_df.columns:
                display_cols = ['id', 'title', 'category', 'price', 'rating']
                available_cols = [col for col in display_cols if col in filtered_df.columns]
                st.dataframe(
                    filtered_df[available_cols],
                    height=400,
                    use_container_width=True
                )

# Tab 3: Scraping
with tab3:
    st.header("🔐 Autenticação & Scraping")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        username = st.text_input("Usuário", value="admin", key="username")
        password = st.text_input("Senha", type="password", value="admin", key="password")
        
        if st.button("🔑 Fazer Login", type="primary"):
            try:
                response = requests.post(
                    f"{st.session_state.api_url}/api/v1/auth/login",
                    json={"username": username, "password": password},
                    timeout=5
                )
                
                if response.status_code == 200:
                    tokens = response.json()
                    st.session_state.access_token = tokens.get('access_token')
                    st.session_state.refresh_token = tokens.get('refresh_token')
                    st.success("✅ Login realizado com sucesso!")
                else:
                    st.error(f"❌ Erro: {response.status_code}")
            except Exception as e:
                st.error(f"Erro: {str(e)}")
    
    with col2:
        st.subheader("🚀 Executar Scraping")
        
        if 'access_token' in st.session_state:
            st.success("✅ Token disponível")
            
            if st.button("🚀 Iniciar Scraping", type="primary"):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
                    response = requests.post(
                        f"{st.session_state.api_url}/api/v1/scraping/trigger",
                        headers=headers,
                        timeout=10
                    )
                    
                    if response.status_code == 202:
                        st.success("✅ Scraping iniciado!")
                        # Limpar cache de logs para forçar atualização
                        if 'logs_last_update' in st.session_state:
                            del st.session_state.logs_last_update
                        st.rerun()
                    else:
                        st.error(f"❌ Erro: {response.status_code}")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        else:
            st.warning("⚠️ Faça login primeiro")
    
    # Logs
    st.markdown("---")
    st.subheader("📋 Logs do Scraping")
    
    # Botão para atualizar
    if st.button("🔄 Atualizar Logs", key="refresh_logs_btn"):
        st.rerun()
    
    # Buscar logs
    try:
        response = requests.get(f"{st.session_state.api_url}/api/v1/scraping/logs?lines=100", timeout=5)
        if response.status_code == 200:
            logs_data = response.json()
            logs = logs_data.get('logs', [])
            status = logs_data.get('status', 'unknown')
            
            # Status
            if status == "running":
                st.info("🟢 Scraping em execução...")
            elif status == "completed":
                st.success("✅ Scraping concluído!")
            elif status == "not_started":
                st.warning("⚠️ Scraping não iniciado")
            else:
                st.info(f"Status: {status}")
            
            if logs:
                log_text = "".join(logs[-50:])
                st.text_area("Logs", value=log_text, height=300, disabled=True, key="logs_display")
                st.caption(f"Total de linhas: {len(logs)}")
            else:
                st.info("Nenhum log disponível. Inicie o scraping para ver os logs.")
        elif response.status_code == 404:
            st.warning("⚠️ Endpoint de logs não encontrado. Verifique se a API está atualizada.")
        else:
            st.error(f"Erro ao buscar logs: {response.status_code}")
    except Exception as e:
        st.error(f"Erro: {str(e)}")

# Tab 4: Busca
with tab4:
    st.header("🔍 Buscar Livros")
    
    search_title = st.text_input("Buscar por título", placeholder="Digite o título...")
    
    categories_data, _ = fetch_data("/api/v1/categories")
    if categories_data:
        selected_cat = st.selectbox("Categoria", ['Todas'] + sorted(categories_data), key="search_category")
    else:
        selected_cat = 'Todas'
    
    if st.button("🔍 Buscar", type="primary"):
        params = {}
        if search_title:
            params['title'] = search_title
        if selected_cat != 'Todas':
            params['category'] = selected_cat
        
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            results, error = fetch_data(f"/api/v1/books/search?{query_string}")
        else:
            results, error = fetch_data("/api/v1/books")
        
        if error:
            st.error(f"Erro: {error}")
        elif results:
            st.success(f"✅ Encontrados {len(results)} livro(s)")
            df_results = pd.DataFrame(results)
            if len(df_results) > 0:
                display_cols = ['id', 'title', 'category', 'price', 'rating']
                available_cols = [col for col in display_cols if col in df_results.columns]
                st.dataframe(df_results[available_cols], use_container_width=True)
