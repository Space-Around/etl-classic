import requests
from bs4 import BeautifulSoup
import json
import datetime
import uuid


def get_month_data(month: str, year: str):
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'ru,en;q=0.9,es;q=0.8,mt;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://appointment.mfa.gr',
        'Referer': 'https://appointment.mfa.gr/en/reservations/aero/grcon-cyprus/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.940 Yowser/2.5 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'scrubber-name': 'appointment.mfa.gr'
    }

    data = {
        'bid': '56',
        'year': year,
        'month': month,
        'adults': '1',
        'children': '0',
        'rnd': '83',
    }

    datetime_object = datetime.datetime.strptime(month, "%m")
    full_month_name = datetime_object.strftime("%B")

    proxies = {
        'http': 'http://127.0.0.1:8081',
        'https': 'http://127.0.0.1:8081'
    }

    cert = '/home/maxwellviksna/.mitmrpoxy/mitmproxy-ca-cert.pem'

    response = requests.post('https://appointment.mfa.gr/inner.php/en/reservations/aero/calendar', headers=headers,
                             data=data, proxies=proxies, verify=cert)

    soup = BeautifulSoup(response.text, 'lxml')
    cells = soup.find_all(class_='aero_bcal_tdopen')

    result = {full_month_name: {}}
    for cell in cells:
        day = cell.text
        schedule = cell['data-schedule']
        times = schedule.split('@')
        r = {day: {}}
        for data in times:
            data = data.split(';')
            if data[-1] != '':
                time_ = data[0]
                available = data[-1]
                r[day].update({time_: bool(int(available))})

        result[full_month_name].update(r)
    return result


def main():
    filename = str(uuid.uuid4())
    result = {}
    currentMonth = datetime.datetime.now().month
    currentYear = datetime.datetime.now().year
    end = False
    while True:
        data = get_month_data(str(currentMonth), str(currentYear))
        if data[list(data.keys())[0]] == {}:
            end = True

        if end:
            break
        result.update(data)
        if currentMonth < 12:
            currentMonth += 1
        else:
            currentYear += 1
            currentMonth = 1

    with open(f'/home/maxwellviksna/etl-classic/airflow/scrubbers/appointment.mfa.gr/{filename}.json', 'w') as f:
        json.dump(result, f)


if __name__ == '__main__':
    main()
