import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Mapping of IDs to medicine names
labels_map = {
    0: "Aciclovir", 1: "Albendazol", 2: "Alopurinol", 3: "Anlodipino",
    4: "Atenolol", 5: "Azitromicina", 6: "Captopril", 7: "Carbamazepina",
    8: "Carvedilol", 9: "Cefalexina", 10: "Ciprofloxacino", 11: "Claritromicina",
    12: "Clindamicina", 13: "Dexametasona", 14: "Dipirona", 15: "Espironolactona",
    16: "Estriol", 17: "Fenobarbital", 18: "Finasterida", 19: "Fluconazol",
    20: "Furosemida", 21: "Glibenclamida", 22: "Gliclazida", 23: "Hidroclorotiazida",
    24: "Ibuprofeno", 25: "Isossorbida", 26: "Ivermectina", 27: "Lactulose",
    28: "Levonorgestrel", 29: "Loratadina", 30: "Metformina", 31: "Metildopa",
    32: "Metoprolol", 33: "Omeprazol", 34: "Paracetamol", 35: "Prednisona",
    36: "Prometazina", 37: "Propranolol", 38: "Sinvastatina", 39: "Varfarina",
    40: "Verapamil"
}

# Base URL templates
base_urls = [
    "https://www.neoquimica.com.br/genericos/{}/",
    "https://germedpharma.com.br/produto/{}/",
    "https://www.uniaoquimica.com.br/produtos/farma/genericos/{}/",
    "https://www.farmalife.com.br/{}/",
    "https://www.farmalife.com.br/{}?page=2",
    "https://www.farmalife.com.br/{}?page=3",
    "https://www.farmalife.com.br/{}?page=4",
    "https://www.bomprecodrogaria.com.br/pesquisa?t={}#/pagina-1",
    "https://www.bomprecodrogaria.com.br/pesquisa?t={}#/pagina-2",
    "https://www.bomprecodrogaria.com.br/pesquisa?t={}#/pagina-3",
    "https://www.bomprecodrogaria.com.br/pesquisa?t={}#/pagina-4"
]

# Headers for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Function to download images from a single URL

def download_images_from_url(med_name, url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")

    for idx, img in enumerate(images, start=1):
        src = img.get('src')
        if not src:
            continue

        # Build absolute URL
        img_url = urljoin(url, src)
        parsed = urlparse(img_url)
        _, ext = os.path.splitext(parsed.path)
        ext = ext or '.jpg'

        # Prepare output path
        folder = os.path.join(os.getcwd(), med_name)
        os.makedirs(folder, exist_ok=True)
        filename = f"{idx}{ext}"
        filepath = os.path.join(folder, filename)

        # Download the image
        try:
            img_data = requests.get(img_url, headers=headers, timeout=10)
            img_data.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(img_data.content)
            print(f"Downloaded {filepath}")
        except requests.RequestException as e:
            print(f"Failed to download {img_url}: {e}")


def main():
    for med in labels_map.values():
        med_lower = med.lower()
        for template in base_urls:
            url = template.format(med_lower)
            print(f"Processing {url}")
            download_images_from_url(med, url)


if __name__ == '__main__':
    main()
