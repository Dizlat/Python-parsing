import requests
import csv
from bs4 import BeautifulSoup


URL = 'https://kg.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki'
page="?sort=popular&page="

def get_html(url):
    get = requests.get(url)
    return get.content

def get_total_page(html):
    soup = BeautifulSoup(html, 'lxml')
    page_ol = soup.find('div', class_="pager i-pager")
    total_page = page_ol.find_all('a')[-2]
    return int(total_page.text)

def write_file(data):
    with open('Data.scv', 'a') as scv_file:
        writer = csv.writer(scv_file, delimiter='/')
        writer.writerow((data['name'], data['char'], data['price']))


def get_total_products(html):
    soup = BeautifulSoup(html, 'lxml')
    product_list = soup.find('div', class_="catalog_main_table")
    products = product_list.find_all('div', class_="dtList-inner")
    for i in products:
        #name, char, price
        try:
            price = i.find('div', class_="j-cataloger-price").find('span', class_="price").find('ins', class_="lower-price").text
            
        except:
            price = ''
        try: 
            a = i.find('div', class_="dtlist-inner-brand-name").find('strong', class_="brand-name c-text-sm").text
            name = a.replace('/', '')
        except:
            name = ''
        try:
            char = i.find('div', class_="dtlist-inner-brand-name").find('span', class_="goods-name c-text-sm").text
        except:
            char= ''
        data = {'name': name, 'char': char, 'price': price}
        write_file(data)

    
        





def main():
    pages = get_total_page(get_html(URL))
    for i in range(1, pages +1):
        url = URL + page + str(pages)
        html = get_html(url)
        get_total_products(html)

main()