import re

with open(r'C:\Users\gusta\Desktop\lp\sorvete\gta\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

exts = re.findall(r'"external/[^"]+"', html)
print(f'Found {len(exts)} external/ paths')
if exts:
    print(exts[:5])
