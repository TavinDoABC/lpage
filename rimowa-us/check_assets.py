import re

with open(r'C:\Users\gusta\Desktop\lp\sorvete\rimowa\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('Total wury:', len(re.findall(r'wury', html, re.IGNORECASE)))
print('Sample wury context:')
for m in re.findall(r'.{0,30}wury.{0,30}', html, re.IGNORECASE)[:5]:
    print(m)
    
print('Total /assets:', len(re.findall(r'[\"\']/assets', html)))
print('Total assets/:', len(re.findall(r'[\"\']assets/', html)))
