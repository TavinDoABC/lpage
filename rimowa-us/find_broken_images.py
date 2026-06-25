import re
from collections import Counter

with open(r'C:\Users\gusta\Desktop\lp\sorvete\rimowa\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'images/[^\s\"\'\)\<]+', html)
print(Counter(matches).most_common(20))
