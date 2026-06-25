import os
import requests
import re
from urllib.parse import urljoin, urlparse

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
        pass

def main():
    with open(os.path.join(TARGET_DIR, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    paths = set()
    matches = re.findall(r'\"([^\"]+\.(?:png|jpg|jpeg|gif|svg|webp|css|js|woff|woff2|ttf|mp4|webm))\"', html)
    paths.update(matches)
    
    ext_matches = re.findall(r'\"(external/[^\"]+)\"', html)
    paths.update(ext_matches)

    for path in paths:
        if path.startswith('http') or path.startswith('data:') or path.startswith('mailto:') or path.startswith('tel:'):
            continue
            
        # If it's a protocol-relative URL, we should treat it as an external domain and download it
        if path.startswith('//'):
            url = 'https:' + path
            # We want to save it locally. We can create a folder for the domain.
            parsed = urlparse(url)
            local_rel = os.path.join(parsed.netloc, parsed.path.lstrip('/'))
            full_url = url
        else:
            # It's a relative path like external/..., assets/... or /external/...
            clean_path = path.lstrip('/')
            local_rel = clean_path
            full_url = urljoin(BASE_URL, path)
            
        local_filepath = os.path.join(TARGET_DIR, local_rel.replace('/', os.sep))
        download_file(full_url, local_filepath)
        
        # We need to rewrite the HTML to point to the local_rel path
        html = html.replace(path, local_rel.replace(os.sep, '/'))

    with open(os.path.join(TARGET_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Asset download and HTML rewrite complete.")

if __name__ == '__main__':
    main()
