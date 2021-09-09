import requests
from bs4 import BeautifulSoup as BS


HOST = 'https://www.avito.ru'
URL = 'https://www.avito.ru/rossiya/komnaty/prodam-ASgBAgICAUSQA7wQ'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}


def get_html(url, params):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BS(html, 'html.parser')
    #clean_content = unicodedata.normalize("NFKD", content.text)
    items = soup.select('[data-marker="item"]')
    #items = content.find_all('div', class_='iva-item-root-Nj_hb')
    estate = []
    if len(items):
        for el in items:
            #title = el.select('[data-marker="item-title"]')
            price = el.select('[data-marker="item-price"]')
            id = el.select('[data-marker="item-view/item-id"]')
            link = el.find('a')
            #address = el.select('[data-marker="item-address"] > .geo-root-H3eWU > .geo-address-QTv9k > span')
            #title = el.find('div', class_='iva-item-content-UnQQ4').find_next('div', class_='iva-item-body-R_Q9c').find_next('div', class_='iva-item-titleStep-_CxvN').find_next('a').get('title')
            #price = el.find('div', class_='iva-item-content-UnQQ4').find_next('div', class_='iva-item-body-R_Q9c').find_next('div', class_='iva-item-priceStep-QN8Kl').find_next('span').get_text()
            #print(title[0].text)
            # address = el.select('[data-marker="item/address"]')
            estate.append({
                #'title': title[0].text.replace('\xa0', ''),
                'id': id[0].text.replace('№ ', ''),
                'price': price[0].text.replace('\xa0', ''),
                'link': HOST + link.get('href')
                #'address': address[0].text
            })
        for user in estate:
            html = get_html(user['link'], params=0)
            #r = requests.get(user['link'], headers=HEADERS)
            user_soup = BS(html.text, 'html.parser')
            user_items = user_soup.select('.item-view-content')
            for el in user_items:
                address = el.select('[itemprop="address"] > span')
                name = el.select('[data-marker="seller-info/name"]')
            user['address'] = address[0].text.replace('\n', ''),
            user['name'] = name[0].text.replace('\n', '')
        print(estate)
    else:
        print('Конец')


def parse():
    page = 1
    while True:
        params = 'p=' + str(page)
        #full_url = URL + '?p=' + str(page)
        html = get_html(URL, params)
        if html.status_code == 200:
            get_content(html.text)
            page+=1
        else:
            break


parse()
# while True:
#     r = requests.get("https://m.avito.ru/kopeysk/nedvizhimost?radius=0")
#     html = BS(r.content, "html.parser")
#     items = html.select(".TGepJ")
#     if(len(items)):
#         for el in items:
#             title = el.select('[data-marker="item/title"]')
#             price = el.select('[data-marker="item/price"]')
#             adress = el.select('[data-marker="item/address"]')
#             phone = el.select('[data-marker="phone-popup/phone-number"]')
#             print('Название: ', title[0].text)
#             print('Адрес: ', adress[0].text)
#             print('Цена: ', price[0].text)
#     else:
#         break