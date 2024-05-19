import requests
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask import send_file
from bs4 import BeautifulSoup
import threading
import time
import schedule
import re
from datetime import datetime, timezone, timedelta


app = Flask(__name__)
CORS(app)
refresh_time = 1 #Обновление актуальных угроз раз в refresh_time минут

def download_cve_html():
    url = 'https://nvd.nist.gov/vuln/search/results?results_type=overview&search_type=last3months&form_type=Basic&isCpeNameSearch=false&orderBy=publishDate&orderDir=desc'
    filename = 'cve.html'
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", {"class": "table table-striped table-hover", "data-testid": "vuln-results-table"})

            
            with open(filename, "w", encoding="utf-8") as file:
                file.write(str(table))
            
            print(f"CVE уязвимости успешно сохранены в файл: {filename}")
        else:
            print(f"CVE ошибка. Статус код: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def download_vmware_html():
    url = 'https://www.vmware.com/security/advisories.xml'
    filename = 'vmware.html'
    session = requests.Session()
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print("VMware уязвимости успешно сохранены в файл:", filename)
        else:
            print("VMware ошибка:", response.status_code)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def find_dates_in_vmware_html():
    file_path = 'vmware.html'
    dates = []
    with open(file_path, 'r') as file:
        content = file.read()
        date_pattern = re.compile(r'<pubDate>([A-Za-z]+), (\d{2}) ([A-Za-z]+) (\d{4}) (\d{2}):(\d{2}):(\d{2}) ([A-Z]{3})</pubDate>')
        matches = date_pattern.findall(content)
        most_recent_date = None
        most_recent_date_str = None
        for match in matches:
            day, day_num, month, year, hour, minute, second, timezone_abbr = match
            date_str = f"{day}, {day_num} {month} {year} {hour}:{minute}:{second}"
            date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S")
            if timezone_abbr == 'PDT':
                timezone_offset = timedelta(hours=-7)  # Смещение для PDT
            else:
                timezone_offset = timedelta(hours=0)  # Для других временных зон
            date_obj = date_obj.replace(tzinfo=timezone.utc) + timezone_offset
            if most_recent_date is None or date_obj > most_recent_date:
                most_recent_date = date_obj
                most_recent_date_str = date_str
    log = (f'The latest VMware vulnerability has been published: {most_recent_date}')
    print(log)
    check_and_append_log('vmware.log', log )

def find_dates_in_cve_html():
    filename = 'cve.html'
    with open(filename, 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Ищем все теги <span> с атрибутом data-testid, содержащим "vuln-published-on-"
        date_spans = soup.find_all('span', {'data-testid': lambda x: x and 'vuln-published-on-' in x})

        # Преобразуем даты в объекты datetime
        dates = []
        for span in date_spans:
            date_str = span.text.strip()
            dates.append(datetime.strptime(date_str, '%b %d, %Y; %I:%M:%S %p %z'))

        # Находим самую недавнюю дату
        latest_date = max(dates)
        log = (f'The latest CVE vulnerability has been published: {latest_date}')
        print(log)
        check_and_append_log('cve.log', log )

def check_and_append_log(filename, string):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            last_line = lines[-1].strip() if lines else None
    except FileNotFoundError:
        last_line = None

    if last_line != string:
        with open(filename, 'a') as file:
            file.write(string + '\n')

schedule.every(refresh_time).minutes.do(download_cve_html)
schedule.every(refresh_time).minutes.do(download_vmware_html)
schedule.every(refresh_time).minutes.do(find_dates_in_vmware_html)
schedule.every(refresh_time).minutes.do(find_dates_in_cve_html)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route('/api/cve', methods=['GET'])
def get_cve():
    return send_file('cve.html', mimetype='text/html')


@app.route('/api/vmware', methods=['GET'])
def get_vmware():
    return send_file('vmware.html', mimetype='text/html')


if __name__ == '__main__':
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    download_cve_html()
    download_vmware_html()
    find_dates_in_vmware_html()
    find_dates_in_cve_html()
   
    app.run(debug=True, host='0.0.0.0', port=9000)
