import requests
from bs4 import BeautifulSoup
import re
import csv
import time

url = 'https://dom.com.cy/en/catalog/sale/'

# функция для получения ссылок на все карточки объектов

cert = '/home/maxwellviksna/.mitmproxy/mitmproxy-ca-cert.pem'
proxies = {
    'http': 'http://127.0.0.1:8081',
    'https': 'http://127.0.0.1:8081'
}


def get_data(url):

    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        'scrubber-name': "bom.cy.com"
    }

    project_urls = []
    print('Начинаю собирать ссылки.')

    for item in range(1, 5):
        time.sleep(1)

        req = requests.get(url + f'?PAGEN_1={item}', headers=headers, proxies=proxies, verify=cert)

        #with open('projects.html', 'w') as file:
        #   file.write(req.text)

        #with open('projects.html') as file:
        #    src = file.read()

        soup = BeautifulSoup(req.text, 'lxml')
        articles = soup.find_all('div', class_ = 'search-item js-filter-search')

        for article in articles:
            project_url = 'https://dom.com.cy' + article.find('div', class_ = 'info').find('a').get('href')
            project_urls.append(project_url)

        print('Получено', len(project_urls), 'объектов.')

    print('Всего найдено', len(project_urls), 'объектов.')
    return project_urls

# функция для получения информации с каждой карточки объекта

def get_information_from_links(project_urls):

    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        'scrubber-name': "bom.cy.com"
    }

    project_data_final = []

    for project_url in project_urls:
        time.sleep(1)
        req = requests.get(project_url, headers=headers, proxies=proxies, verify=cert)
        project_name = project_url.split('/')[-2]

        #with open(f"data/{project_name}.html", 'w') as file:
        #   file.write(req.text)

        #with open(f'data/{project_name}.html') as file:
        #    src = file.read()

        soup = BeautifulSoup(req.text, 'lxml')
        project_data = soup.find('div', class_ = 'col-md-5 info_block_main')

        try:
            project_id = project_data.find(text = re.compile('Object ')).parent.find('strong').text
        except Exception:
            project_id = 'No data about id'

        try:
            project_type = project_data.find(text = re.compile('Type:')).parent.find('strong').text
        except Exception:
            project_type = 'No data about type'

        try:
            project_city = project_data.find(text = re.compile('City:')).parent.find('strong').find('a').text
        except Exception:
            project_city = 'No data about city'

        try:
            project_area = project_data.find(text = re.compile('Area:')).parent.find('strong').find('a').text
        except Exception:
            project_area = 'No data about area'

        try:
            project_bedrooms = project_data.find(text = re.compile('Bedrooms:')).parent.find('strong').text
        except Exception:
            project_bedrooms = 'No data about bedrooms'

        try:
            project_bathrooms = project_data.find(text = re.compile('Bathrooms:')).parent.find('strong').text
        except Exception:
            project_bathrooms = 'No data about bathrooms'

        try:
            project_living_area = project_data.find(text = re.compile('Living area:')).parent.find('strong').text
        except Exception:
            project_living_area = 'No data about living area'

        try:
            project_total_area = project_data.find(text = re.compile('Total area:')).parent.find('strong').text
        except Exception:
            project_total_area = 'No data about total area'

        try:
            project_plot = project_data.find(text = re.compile('Plot: ')).parent.find('strong').text
        except Exception:
            project_plot = 'No data about plot'

        try:
            project_storeys = project_data.find(text = re.compile('Storeys:')).parent.find('strong').text
        except Exception:
            project_storeys = 'No data about storeys'

        try:
            project_windows = project_data.find(text = re.compile('Windows:')).parent.find('strong').text
        except Exception:
            project_windows = 'No data about windows'

        try:
            project_parking = project_data.find(text = re.compile('Parking:')).parent.find('strong').text
        except Exception:
            project_parking = 'No data about parking'

        try:
            project_year_of_construction = project_data.find(text = re.compile('Year of construction:')).parent.find('strong').text
        except Exception:
            project_year_of_construction = 'No data about year_of_construction'

        try:
            project_new_building = project_data.find(text = re.compile('New building:')).parent.find('strong').text
        except Exception:
            project_new_building = 'No data about new or not new building'

        try:
            project_distance_to_sea = project_data.find(text = re.compile('Distance to the sea:')).parent.find('strong').text
        except Exception:
            project_distance_to_sea = 'No data about distance to the sea'

        try:
            project_cost_detail = project_data.find('div', class_ = 'cost-detail').find('span', itemprop = 'price').text
        except Exception:
            project_cost_detail = 'No data about cost'

        try:
            project_name_of_manager = project_data.find('div', class_ = 'manager-data-first').text.strip()
        except Exception:
            project_name_of_manager = 'No data about name of manager'

        try:
            project_mail_of_manager = project_data.find('a', class_ = 'object-email').text.strip()
        except Exception:
            project_mail_of_manager = 'No data about mail of manager'

        try:
            project_phone_of_manager = project_data.find('a', class_ = 'show_phones_variants').text.strip()
        except Exception:
            project_phone_of_manager = 'No data about phone of manager'

        try:
            project_description_first = project_data.find('div', class_ = 'container desc_container').find('div', class_ = 'row').text.split('\n')
            project_description = str(project_description_first[3])
        except Exception:
            project_description = 'No data about description'

        project_data_final.append(
            {
                'ID': project_id,
                'Type': project_type,
                'City': project_city,
                'Area': project_area,
                'Bedrooms': project_bedrooms,
                'Bathrooms': project_bathrooms,
                'Living area': project_living_area,
                'Total area': project_total_area,
                'Plot': project_plot,
                'Storeys': project_storeys,
                'Windows': project_windows,
                'Parking': project_parking,
                'Year of construction': project_year_of_construction,
                'New or not new building': project_new_building,
                'Distance to sea': project_distance_to_sea,
                'Cost': project_cost_detail,
                'Name of manager': project_name_of_manager,
                'Mail of manager': project_mail_of_manager,
                'Phone of manager': project_phone_of_manager,
                'Description': project_description
            }
        )

        print('Парсинг объекта №', project_id, 'прошел успешно. Продолжим)')

    return project_data_final


# функция для записи в csv

def write_to_csv(project_data_final):
    with open('/home/maxwellviksna/etl-classic/airflow/scrubbers/bom.cy.com/data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'ID',
                'Type',
                'City',
                'Area',
                'Bedrooms',
                'Bathrooms',
                'Living area',
                'Total area',
                'Plot',
                'Storeys',
                'Windows',
                'Parking',
                'Year of construction',
                'New or not new building',
                'Distance to sea',
                'Cost',
                'Name of manager',
                'Mail of manager',
                'Phone of manager',
                'Description'
            )
        )

        for element in project_data_final:
            writer.writerow(
                (
                    element['ID'],
                    element['Type'],
                    element['City'],
                    element['Area'],
                    element['Bedrooms'],
                    element['Bathrooms'],
                    element['Living area'],
                    element['Total area'],
                    element['Plot'],
                    element['Storeys'],
                    element['Windows'],
                    element['Parking'],
                    element['Year of construction'],
                    element['New or not new building'],
                    element['Distance to sea'],
                    element['Cost'],
                    element['Name of manager'],
                    element['Mail of manager'],
                    element['Phone of manager'],
                    element['Description']
                )
            )

project_urls = get_data('https://dom.com.cy/en/catalog/sale/')
project_data_final = get_information_from_links(project_urls)

write_to_csv(project_data_final)
