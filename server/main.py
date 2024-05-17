import json
import os
import requests
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask import send_file

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

@app.route('/')
def index():
    with open('vulnerabilities.json', 'r') as file:
        vulnerabilities_data = json.load(file)
    
    return render_template('vulnerabilities.html', vulnerabilities=vulnerabilities_data['vulnerabilities'])

@app.route('/api/cve', methods=['GET'])
def get_vulnerabilities():
    with open('vulnerabilities.json', 'r') as file:
        vulnerabilities_data = json.load(file)
    
    return jsonify(vulnerabilities_data)


@app.route('/api/vmware', methods=['GET'])
def get_vmware():
    return send_file('advisories.html', mimetype='text/html')


if __name__ == '__main__':
    fetch_vulnerabilities()
    app.run(debug=True, host='0.0.0.0', port=9000)