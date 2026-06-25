import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.rockstargames-br.com/"
TARGET_DIR = r"C:\Users\gusta\Desktop\lp\sorvete\gta"

def download_file(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path):
        return # already downloaded
        
    try:
        print(f"Downloading: {url} to {local_path}")
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    print("Fetching HTML...")
    r = requests.get(BASE_URL)
    r.raise_for_status()
    html_content = r.text
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    tags_attributes = [
        ('img', 'src'),
        ('script', 'src'),
        ('source', 'src'),
        ('video', 'src'),
        ('link', 'href')
    ]
    
    for tag_name, attr in tags_attributes:
        for tag in soup.find_all(tag_name):
            val = tag.get(attr)
            if not val:
                continue
            
            # Skip fb tracking or absolute external domains not matching target
            if val.startswith('http') and urlparse(BASE_URL).netloc not in val:
                continue
                
            parsed = urlparse(val)
            path = parsed.path
            
            if not path or path == '/':
                continue
                
            if path.startswith('/'):
                path = path[1:] # remove leading slash
                
            local_filepath = os.path.join(TARGET_DIR, path.replace('/', os.sep))
            full_url = urljoin(BASE_URL, val)
            
            download_file(full_url, local_filepath)
            
            # Update HTML tag to point to local relative path
            # Instead of absolute, use relative to gta/ folder
            tag[attr] = path
            
    # Save the modified HTML
    with open(os.path.join(TARGET_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(str(soup))
        
    print("Clone complete.")

if __name__ == '__main__':
    main()
