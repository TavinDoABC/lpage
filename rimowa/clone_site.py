import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

BASE_URL = "https://wuryxrimowa.de/"
TARGET_DIR = r"C:\Users\gusta\Desktop\lp\rimowa"

def download_file(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path):
        return # already downloaded
        
    try:
        print(f"Downloading: {url}")
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        
    print("Fetching HTML...")
    r = requests.get(BASE_URL)
    r.raise_for_status()
    html_content = r.text
    
    with open(os.path.join(TARGET_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Elements with src
    for tag in soup.find_all(['img', 'script', 'source']):
        src = tag.get('src')
        if not src:
            continue
            
        parsed = urlparse(src)
        if parsed.netloc and parsed.netloc != urlparse(BASE_URL).netloc:
            continue # Skip external assets
            
        # Remove query parameters for local filename
        path = parsed.path
        if path.startswith('/'):
            path = path[1:]
            
        if not path:
            continue
            
        local_filepath = os.path.join(TARGET_DIR, path.replace('/', os.sep))
        full_url = urljoin(BASE_URL, src)
        
        download_file(full_url, local_filepath)
        
    # Elements with href (stylesheets, icons)
    for tag in soup.find_all(['link']):
        href = tag.get('href')
        if not href:
            continue
            
        parsed = urlparse(href)
        if parsed.netloc and parsed.netloc != urlparse(BASE_URL).netloc:
            continue # Skip external assets like fonts
            
        path = parsed.path
        if path.startswith('/'):
            path = path[1:]
            
        if not path:
            continue
            
        local_filepath = os.path.join(TARGET_DIR, path.replace('/', os.sep))
        full_url = urljoin(BASE_URL, href)
        
        download_file(full_url, local_filepath)
        
    print("Clone complete.")

if __name__ == '__main__':
    main()
