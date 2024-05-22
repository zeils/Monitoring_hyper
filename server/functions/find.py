from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import re
import json
from server.functions.logger import check_and_append_log


with open('../config.json', 'r') as config_file:
    config = json.load(config_file)

data_path = '../data/'
log_path = '../data/log/'

def find_dates_in_vmware_cve_html():
    filename = f'{data_path}{config['vmware_filename']}'
    dates = []
    with open(filename, 'r') as file:
        content = file.read()
        date_pattern = re.compile(r'<pubDate>([A-Za-z]+), (\d{2}) ([A-Za-z]+) (\d{4}) (\d{2}):(\d{2}):(\d{2}) ([A-Z]{3})</pubDate>')
        matches = date_pattern.findall(content)
        latest_date = None
        most_recent_date_str = None
        for match in matches:
            day, day_num, month, year, hour, minute, second, timezone_abbr = match
            date_str = f"{day}, {day_num} {month} {year} {hour}:{minute}:{second}"
            date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S")
            if timezone_abbr == 'PDT':
                timezone_offset = timedelta(hours=-7)  
            else:
                timezone_offset = timedelta(hours=0)  
            date_obj = date_obj.replace(tzinfo=timezone.utc) + timezone_offset
            if latest_date is None or date_obj > latest_date:
                latest_date = date_obj
                most_recent_date_str = date_str
    log = (f'The latest VMware vulnerability has been published: {latest_date}')
    print(log)
    check_and_append_log(f'{log_path}vmware_cve.log', log )
    return latest_date

def find_dates_in_nvd_cve_html():
    filename = f'{data_path}{config['nvd_filename']}'
    with open(filename, 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        date_spans = soup.find_all('span', {'data-testid': lambda x: x and 'vuln-published-on-' in x})
        dates = []
        for span in date_spans:
            date_str = span.text.strip()
            dates.append(datetime.strptime(date_str, '%b %d, %Y; %I:%M:%S %p %z'))

        latest_date = max(dates)
        log = (f'The latest CVE vulnerability has been published: {latest_date}')
        print(log)
        check_and_append_log(f'{log_path}nvd_cve.log', log )
        return latest_date

def find_dates_in_mitr_cve_html():
    filename = f'{data_path}{config['mitre_filename']}'
    try:
        with open(filename, 'r') as file:
            cve_data = json.load(file)
        latest_date = None
        for cve_entry in cve_data:
            published_date_str = cve_entry.get('Published', '')
            published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
            
            if latest_date is None or published_date > latest_date:
                latest_date = published_date
        
        log = (f'The latest MITRE CVE vulnerability has been published: {latest_date}')
        print(log)
        check_and_append_log(f'{log_path}mitr_cve.log', log )
        return latest_date

    except Exception as e:
        print(f"Error: {e}")
        return None
    
def find_all_task():
    find_dates_in_vmware_cve_html()
    find_dates_in_nvd_cve_html()
    find_dates_in_mitr_cve_html()  