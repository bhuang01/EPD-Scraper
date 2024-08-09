import requests
from googlesearch import search
import PyPDF2
import io
import asyncio
import time

def find_epd(material: str, manufacturer: str) -> str | None:
    query = f"filetype:pdf \"{material}\" \"{manufacturer}\" \"Environmental Product Declaration\""
    print(f"Searching with query: {query}")
    
    for url in search(query, num_results=10):
        print(f"Checking URL: {url}")
        if url.lower().endswith('.pdf'):
            if verify_pdf_content(url, material, manufacturer):
                return url
        time.sleep(1)
    return None

def verify_pdf_content(url: str, material: str, manufacturer: str) -> bool:
    try:
        print(f"Verifying content of {url}")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            pdf_file = io.BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            for i, page in enumerate(pdf_reader.pages[:5]):
                text = page.extract_text().lower()
                print(f"Checking page {i+1}")
                if material.lower() in text or manufacturer.lower() in text:
                    print("Match found!")
                    return True
        else:
            print(f"Failed to fetch PDF. Status code: {response.status_code}")
        return False
    except Exception as e:
        print(f"Error verifying PDF content: {e}")
        return False

async def main():
    material = input("material name: ")
    manufacturer = input("manufacturer name: ")
    result = find_epd(material, manufacturer)
    if result:
        print(f"Successfully found EPD for {material} by {manufacturer}")
        print(f"EPD URL: {result}")
    else:
        print(f"Could not find a suitable EPD for {material} by {manufacturer}")

if __name__ == "__main__":
    asyncio.run(main())