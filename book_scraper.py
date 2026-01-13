import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os

# URL base do site
BASE_URL = 'http://books.toscrape.com/'

# Dicionário para converter o rating de texto para número
RATING_MAP = {
    'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
}

def get_book_details(book_url):
    """
    Acessa a página de detalhes do livro para extrair a categoria e descrição.
    """
    try:
        response = requests.get(book_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            category = search_category_in_breadcrumb(soup)
            description_book = search_description_in_article(soup)

            return category, description_book
    except Exception as e:
        print(f"Erro ao acessar detalhes: {e}")
    return "Unknown", "No description available"

def search_category_in_breadcrumb(soup):
    """
    Função auxiliar para buscar a categoria na trilha de navegação (breadcrumb).
    """
    try:
        breadcrumb = soup.find('ul', class_='breadcrumb')
        if breadcrumb:
            category = breadcrumb.find_all('li')[2].text.strip()
            return category
        return "Unknown"
    except Exception as e:
        print(f"Erro ao buscar categoria: {e}")
    return "Unknown"


def search_description_in_article(soup):
    """
    Função auxiliar para buscar a descrição do livro na página de detalhes.
    """
    try:
        article = soup.find('article', class_='product_page' )
        if article:
            description_book = article.find_all('p')[3].text
            return description_book
        return "No description available"
    
    except Exception as e:
        print(f"Erro ao buscar descrição: {e}")
    return "No description available"


def scrape_books():
    # Configurar logging
    log_file = os.path.join('data', 'scraping.log')
    os.makedirs('data', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    books_data = []
    url = 'catalogue/page-1.html'
    current_url = BASE_URL + url
    
    logger.info("Iniciando Scraping... isso pode levar alguns minutos.")

    while True:
        logger.info(f"Scraping: {current_url}")
        try:
            response = requests.get(current_url)
            response.raise_for_status()


            soup = BeautifulSoup(response.content, 'lxml')
            products = soup.find_all('article', class_='product_pod')

            for product in products:
                # Extração dos dados: título, preço, rating, disponibilidade, categoria, imagem
                h3 = product.find('h3')
                title = h3.find('a')['title']
                book_relative_url = h3.find('a')['href']
                
                price_text = product.find('p', class_='price_color').text
                price = float(price_text.replace('£', ''))
                
                star_tag = product.find('p', class_='star-rating')
                rating_class = [c for c in star_tag['class'] if c != 'star-rating']
                rating = RATING_MAP.get(rating_class[0], 0)
                
                availability = product.find('p', class_='instock availability').text.strip()
                image_url = BASE_URL + product.find('img')['src'].replace('../', '')

                # Busca da categoria e descrição (requisição adicional)
                if 'catalogue/' in book_relative_url:
                    full_book_url = BASE_URL + book_relative_url
                else:
                    full_book_url = BASE_URL + 'catalogue/' + book_relative_url
                
                category, description  = get_book_details(full_book_url)
                
                # Log progresso a cada 10 livros com porcentagem estimada
                if len(books_data) % 10 == 0:
                    # Estimativa: site tem aproximadamente 1000 livros
                    estimated_total = 1000
                    progress_pct = min(100, int((len(books_data) / estimated_total) * 100))
                    logger.info(f"Progresso: {len(books_data)} livros extraídos ({progress_pct}%)...")

                books_data.append({
                    'id' : len(books_data) + 1,
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'availability': availability,
                    'category': category,
                    'image': image_url,
                    'description': description
                })

            # Lógica do botão Next para paginação
            next_li = soup.find('li', class_='next')
            
            if next_li:
                next_url_relative = next_li.find('a')['href']
                if 'catalogue/' in next_url_relative:
                    current_url = BASE_URL + next_url_relative
                else:
                    current_url = BASE_URL + 'catalogue/' + next_url_relative
            else:
                logger.info("Fim da paginação.")
                break
                
        except Exception as e:
            logger.error(f"Erro crítico: {e}")
            break

    # Salvar em CSV
    df = pd.DataFrame(books_data)
    df.to_csv('data/books.csv', index=False, encoding='utf-8')
    logger.info(f"Scraping concluído! {len(df)} livros salvos em data/books.csv (100%)")

if __name__ == "__main__":
    scrape_books()
