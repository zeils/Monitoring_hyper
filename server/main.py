from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask import send_file
import threading
import time
import schedule
import json
from functions.download import download_all_task
from functions.find import find_all_task
from functions.find import find_dates_in_nvd_cve_html
from functions.find import find_dates_in_mitr_cve_html
from functions.find import find_dates_in_vmware_cve_html


app = Flask(__name__)
CORS(app)
data_path = './data/'
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/api/download/nvd_cve', methods=['GET'])
def get_cve():
    return send_file(f'{data_path}{config['nvd_filename']}', mimetype='text/html')

@app.route('/api/download/vmware_cve', methods=['GET'])
def get_vmware():
    return send_file(f'{data_path}{config['vmware_filename']}', mimetype='text/html')

@app.route('/api/download/mitre_cve', methods=['GET'])
def get_mitr_cve():
    return send_file(f'{data_path}{config['mitre_filename']}', mimetype='text/html')

@app.route('/api/last_cve/all', methods=['GET'])
def last_all_cve():
    last_nvd_timestamp = find_dates_in_nvd_cve_html()
    last_mitre_timestamp = find_dates_in_mitr_cve_html()
    last_vmware_timestamp = find_dates_in_vmware_cve_html()
    return jsonify({
        "last_nvd_cve": int(last_nvd_timestamp.timestamp()),
        "last_mitre_cve": int(last_mitre_timestamp.timestamp()),
        "last_vmware_cve": int(last_vmware_timestamp.timestamp())
    })

@app.route('/api/last_cve/nvd', methods=['GET'])
def last_nvd():
    last_nvd_timestamp = find_dates_in_nvd_cve_html()
    if last_nvd_timestamp:
        return jsonify({"last_nvd_cve": int(last_nvd_timestamp.timestamp())})
    else:
        return jsonify({"last_nvd_cve": "No data available"})

@app.route('/api/last_cve/mitre', methods=['GET'])
def last_mitre():
    last_mitre_timestamp = find_dates_in_mitr_cve_html()
    if last_mitre_timestamp:
        return jsonify({"last_mitre_cve": int(last_mitre_timestamp.timestamp())})
    else:
        return jsonify({"last_mitre_cve": "No data available"})

@app.route('/api/last_cve/mvware', methods=['GET'])
def last_vmware():
    last_vmware_timestamp = find_dates_in_vmware_cve_html()
    if last_vmware_timestamp:
        return jsonify({"last_vmware_cve": int(last_vmware_timestamp.timestamp())})
    else:
        return jsonify({"last_vmware_cve": "No data available"})

refresh_time = config['refresh_time']
schedule.every(refresh_time).minutes.do(download_all_task)
schedule.every(refresh_time).minutes.do(find_all_task)

if __name__ == '__main__':
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    download_all_task()
    find_all_task()
   
    app.run(debug=True, host='0.0.0.0', port=9000)
