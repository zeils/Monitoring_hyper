import json
import os
import requests
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask import send_file
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def fetch_vulnerabilities():
    url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
    response = requests.get(url)

    if response.status_code == 200:
        vulnerabilities_data = response.json()
        script_directory = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_directory, 'vulnerabilities.json')
        
        with open(save_path, 'w') as file:
            json.dump(vulnerabilities_data, file, indent=4)
        
        print(f"Данные об уязвимостях успешно сохранены в {save_path}")
    else:
        print("Ошибка при получении данных об уязвимостях")

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
            
            print(f"Страница успешно сохранена в файл {filename}")
        else:
            print(f"Не удалось скачать страницу. Статус код: {response.status_code}")
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
            print("HTML-контент успешно сохранен в файл:", filename)
        else:
            print("Ошибка при запросе:", response.status_code)
    except Exception as e:
        print(f"Произошла ошибка: {e}")






@app.route('/')
def index():
    with open('vulnerabilities.json', 'r') as file:
        vulnerabilities_data = json.load(file)
    
    return render_template('vulnerabilities.html', vulnerabilities=vulnerabilities_data['vulnerabilities'])

@app.route('/api/cve', methods=['GET'])
def get_cve():
    return send_file('cve.html', mimetype='text/html')


@app.route('/api/vmware', methods=['GET'])
def get_vmware():
    return send_file('vmware.html', mimetype='text/html')


if __name__ == '__main__':
    download_cve_html()
    download_vmware_html()
    app.run(debug=True, host='0.0.0.0', port=9000)