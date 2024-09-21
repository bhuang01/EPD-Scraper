import requests
from bs4 import BeautifulSoup
import csv

def scrape_epd(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
        
        epd_info = soup.find('div', class_='epd-info')
        if epd_info:
            manufacturer = epd_info.find('p', class_='manufacturer').text.strip() if epd_info.find('p', class_='manufacturer') else 'N/A'
            product_description = epd_info.find('p', class_='description').text.strip() if epd_info.find('p', class_='description') else 'N/A'
        else:
            manufacturer = 'N/A'
            product_description = 'N/A'
        
        return {
            'Title': title,
            'Manufacturer': manufacturer,
            'Product Description': product_description,
        }
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def main():
    base_url = "https://node.epditaly.it/datasetdetail/process.xhtml?"
    uuids = [
        "5650ed85-bb4c-4878-8ce9-00754da269ac",
    ]
    
    results = []
    
    for uuid in uuids:
        url = f"{base_url}uuid={uuid}&version=00.03.000&lang=en"
        data = scrape_epd(url)
        if data:
            results.append(data)
    
    if results:
        keys = results[0].keys()
        with open('epd_data.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
        print("Data has been saved to epd_data.csv")
    else:
        print("No data was collected.")

if __name__ == "__main__":
    main()