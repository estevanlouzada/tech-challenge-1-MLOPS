import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL base do site (conforme identificado nos fontes)
BASE_URL = 'http://books.toscrape.com/'

# Dicionário para converter o rating de texto para número [6]
RATING_MAP = {
    'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
}

def get_book_details(book_url):
    """
    Acessa a página de detalhes do livro para extrair a Categoria.
    Necessário pois a categoria não está no card da listagem principal.
    """
    try:
        response = requests.get(book_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            # A categoria geralmente está no breadcrumb (lista de navegação no topo)
            # Ex: Home > Books > Mystery > Title

            category = search_category_in_breadcrumb(soup)
            description_book = search_category_in_breadcrumb(soup)

            return category, description_book
    except Exception as e:
        print(f"Erro ao acessar detalhes: {e}")
    return "Unknown"

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
    books_data = []
    url = 'catalogue/page-1.html' # Começa explicitamente na página 1 ou index.html
    
    current_url = BASE_URL + url
    
    print("Iniciando Scraping... isso pode levar alguns minutos.")

    while True:
        print(f"Scraping: {current_url}")
        try:
            response = requests.get(current_url)
            response.raise_for_status()

            # Save the HTML content of the first page for analysis
            if 'page-1.html' in current_url:
                with open('scraped_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("Saved HTML of the first page to 'scraped_page.html' for analysis.")

            soup = BeautifulSoup(response.content, 'lxml') # lxml é mais rápido [Requisito do requirements.txt]

            # 1. Encontrar todos os livros na página atual
            # Fonte [6]: <article class="product_pod">
            products = soup.find_all('article', class_='product_pod')

            for product in products:
                # --- Extração dos dados descritos no Requisito [2] ---
                
                # Título: Fonte [6] <h3><a title="...">
                h3 = product.find('h3')
                title = h3.find('a')['title'] 
                
                # Link Relativo do Livro (para buscar categoria)
                book_relative_url = h3.find('a')['href']
                
                # Preço: Fonte [10] <p class="price_color">
                price_text = product.find('p', class_='price_color').text
                price = float(price_text.replace('£', ''))
                
                # Rating: Fonte [6] <p class="star-rating Three">
                star_tag = product.find('p', class_='star-rating')
                rating_class = [c for c in star_tag['class'] if c != 'star-rating']
                rating = RATING_MAP.get(rating_class[0], 0)
                
                # Disponibilidade: Fonte [10] <p class="instock availability">
                availability = product.find('p', class_='instock availability').text.strip()
                
                # Imagem: Fonte [6] <img src="...">
                image_url = BASE_URL + product.find('img')['src'].replace('../', '')

                # --- Busca da Categoria (Request Adicional) ---
                # Resolvemos a URL completa do livro tratando caminhos relativos
                if 'catalogue/' in book_relative_url:
                    full_book_url = BASE_URL + book_relative_url
                else:
                    full_book_url = BASE_URL + 'catalogue/' + book_relative_url
                
                category, description  = get_book_details(full_book_url)

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

            # 2. Lógica do Botão Next
            # Fonte [5]: <li class="next"><a href="...">next</a></li>
            next_li = soup.find('li', class_='next')
            
            if next_li:
                next_url_relative = next_li.find('a')['href']
                # Tratamento de URL para garantir que o caminho esteja correto
                if 'catalogue/' in next_url_relative:
                    current_url = BASE_URL + next_url_relative
                else:
                    current_url = BASE_URL + 'catalogue/' + next_url_relative
            else:
                # Se não houver botão next, acabaram as páginas
                print("Fim da paginação.")
                break
                
        except Exception as e:
            print(f"Erro crítico: {e}")
            break

    # 3. Salvar em CSV (Requisito [1])
    df = pd.DataFrame(books_data)
    df.to_csv('data/books.csv', index=False, encoding='utf-8')
    print(f"Scraping concluído! {len(df)} livros salvos em data/books.csv")

if __name__ == "__main__":
    scrape_books()
