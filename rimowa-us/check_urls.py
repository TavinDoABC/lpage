import re

with open(r'C:\Users\gusta\Desktop\lp\sorvete\rimowa\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

urls = re.findall(r'https?://[^\s\"\'\)\<]+', html)
for u in urls:
    if 'wury' in u:
        print('wury link:', u)
