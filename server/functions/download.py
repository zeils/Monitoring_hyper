from bs4 import BeautifulSoup
import requests
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

data_path = 'data/'

def download_nvd_cve_html():
    filename = f'{data_path}{config["nvd_filename"]}'
    cve_url = config['cve_nvd_url']
    try:
        response = requests.get(cve_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", {"class": "table table-striped table-hover", "data-testid": "vuln-results-table"})
            with open(filename, "w", encoding="utf-8") as file:
                file.write(str(table))
            
            print(f"CVE уязвимости из NVD успешно сохранены в файл: {filename}")
        else:
            print(f"CVE NVD ошибка. Статус код: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def download_mitr_cve_html():
    filename = f'{data_path}{config["mitre_filename"]}'
    url = config['cve_mitr_url']
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "w") as file:
                file.write(response.text)
            print(f"CVE уязвимости из MITRE успешно сохранены в файл: {filename}")
        else:
            print("CVE MITRE ошибка. Статус код:", response.status_code)
    except Exception as e:
        print("Ошибка:", e)

def download_vmware_cve_html():
    vmware_url = config['cve_vmware_url']
    filename = f'{data_path}{config["vmware_filename"]}'
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
        response = session.get(vmware_url, headers=headers)

        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print("CVE уязвимости VMware успешно сохранены в файл:", filename)
        else:
            print("CVE VMware ошибка. Статус код:", response.status_code)
    except Exception as e:
        print(f"CVE VMware ошибка: {e}")


def download_all_task():
    download_nvd_cve_html()
    download_vmware_cve_html()
    download_mitr_cve_html()