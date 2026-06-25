import os
import requests
import re
from urllib.parse import urljoin

BASE_URL = "https://www.rockstargames-br.com/"
TARGET_DIR = r"C:\Users\gusta\Desktop\lp\sorvete\gta"

def download_file(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path):
        return
        
    try:
        r = requests.get(url, stream=True, timeout=15)
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {local_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    with open(os.path.join(TARGET_DIR, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    # Find all strings that look like relative paths
    # The original HTTrack usually creates folders like `external/`, `fonts/`, `images/`
    paths = set()
    # Find anything inside quotes that has standard file extensions
    matches = re.findall(r'\"([^\"]+\.(?:png|jpg|jpeg|gif|svg|webp|css|js|woff|woff2|ttf|mp4|webm))\"', html)
    paths.update(matches)
    
    # Also find explicit `external/` or similar
    ext_matches = re.findall(r'\"(external/[^\"]+)\"', html)
    paths.update(ext_matches)

    for path in paths:
        # filter out absolute urls
        if path.startswith('http') or path.startswith('data:'):
            continue
            
        clean_path = path
        if clean_path.startswith('/'):
            clean_path = clean_path[1:]
            
        local_filepath = os.path.join(TARGET_DIR, clean_path.replace('/', os.sep))
        full_url = urljoin(BASE_URL, path)
        
        download_file(full_url, local_filepath)

    print("Asset download complete.")

if __name__ == '__main__':
    main()
