import json
import os
import requests
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask import send_file
from bs4 import BeautifulSoup


def download_vmware_html():
    url = 'https://www.vmware.com/security/advisories.xml'
    filename = 'vmware.xml'
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
            print(response.text)
        else:
            print("Ошибка при запросе:", response.status_code)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


download_vmware_html()