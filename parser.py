import requests
from bs4 import BeautifulSoup
import csv

CSV = 'ScopusArticle.csv'
HOST = 'https://www.scopus.com/'
URL = 'https://www.scopus.com/authid/detail.uri?authorId=56565613500'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.79'
}



def get_html1(url, params=''):
    r1 = requests.get(url, headers=HEADERS,params=params)
    return r1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='col-19')
    article = []

    for item in items:
        article.append(
            {
                'article-name': item.find('a', class_='list-title').get_text(strip=True),
                'article-url' : item.find('a', href = True),
                'authors': item.find('div', class_='author-list').find_all('span').get_text(strip=True),
                'document-source': item.find('a', class_='source-link').find('span').get_text(strip=True),
                'document-meta': item.find('div', class_='text-meta text-width-34').find('span', class_='text-meta').get_text(strip=True),
            }
        )
        art_url = item.find('a', href =True)
        get_html2(art_url)
        article.append(
            {
                'doi' : item.find('dl', class_='stack stack--xxs stack--mode-container stack--vertical stack--start margin-size-0').get_text(strip=True),
            }
        )
        return article


def get_html2(art_url, params=''):
    r2 = requests.get(art_url, headers=HEADERS, params=params)
    return r2

def save_csv(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название статьи', 'Ссылка на статью', 'Авторы', 'Место публикации', 'Доп. данные', 'DOI'])
        for item in items:
            writer.writerow([item['article-name'], item['aricle-url'], item['authors'], item['document-source'],item['document-meta'], item['doi']])


def parser():
    pagenation = 1 #Ввод количества страниц, которые будут парситься
    pagenation = int(pagenation.strip)
    html = get_html1(URL)
    if html.status_code == 200:
        article = []
        for page in range(1, pagenation):
            html = get_html1(URL, params={'page': page})
            article.extend(get_content(html.text))
            save_csv(article, CSV)
    else:
        print('Connect error')


parser()