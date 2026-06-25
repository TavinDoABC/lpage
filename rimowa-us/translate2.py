import re

def translate_html_2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    replacements = {
        'Gewicht und Maße variieren je nach Size:': 'Weight and dimensions vary by Size:',
        'wiegt 4,3 kg, fasst 36 Liter und misst 55 × 40 × 23 cm.': 'weighs 4.3 kg, holds 36 liters, and measures 55 × 40 × 23 cm.',
        'wiegt 4,2 kg, fasst 33 Liter und misst 55 × 40 × 20 cm.': 'weighs 4.2 kg, holds 33 liters, and measures 55 × 40 × 20 cm.',
        'für mühelose 360°-Mobilität,': 'for effortless 360° mobility,',
        'Was deckt die lebenslange Garantie ab?': 'What does the lifetime guarantee cover?',
        'TSA Locks lassen sich von der Sicherheitskontrolle mit einem Universal-Generalschlüssel öffnen — ohne das Schloss zu beschädigen. Ihr Koffer bleibt während der gesamten Reise sicher verschlossen und kann an jeder Sicherheitskontrolle dennoch geprüft werden. Besonders praktisch bei Reisen in die USA.': 'TSA Locks can be opened by security control with a universal master key — without damaging the lock. Your suitcase remains securely locked throughout the journey and can still be inspected at any security checkpoint. Especially practical when traveling to the USA.',
        'wiegt 5,3 kg, fasst 60 Liter und misst 70 × 47 × 25 cm.': 'weighs 5.3 kg, holds 60 liters, and measures 70 × 47 × 25 cm.',
        'Reviews mit Photos ansehen': 'View Reviews with Photos',
        'Integrierte TSA Locks für sicheres Reisen weltweit. Kein zusätzliches Vorhängeschloss nötig.': 'Integrated TSA Locks for secure travel worldwide. No additional padlock needed.',
        'wiegt 6,0 kg, fasst 85 Liter und misst 78 × 52 × 27 cm.': 'weighs 6.0 kg, holds 85 liters, and measures 78 × 52 × 27 cm.',
        'Wie funktioniert die Rückgabe?': 'How do returns work?',
        'Was ist im Lieferumfang enthalten?': 'What is included in the box?',
        'Flex Divider-System für eine anpassbare Aufteilung. Alles an seinem Platz.': 'Flex Divider system for a customizable layout. Everything in its place.',
        'Cabin-Größe als Handgepäck zugelassen. Gemacht für Geschäftsreisen.': 'Cabin size approved as carry-on. Made for business trips.',
        'Exklusiv für Deutschland': 'Exclusive to the US',
        'Ihr Koffer wird mit einem gratis Lederanhänger fürs Gepäck und einem RIMOWA Sticker geliefert. Der Flex Divider, die TSA Locks und der stufenlos verstellbare Teleskopgriff sind alle fest integriert.': 'Your suitcase comes with a free leather luggage tag and a RIMOWA sticker. The Flex Divider, TSA Locks, and stageless telescopic handle are all fully integrated.',
        'Für jede Reise.': 'For every journey.',
        'Die ikonischen Rillen seit 1898. Jede Delle erzählt eine Geschichte.': 'The iconic grooves since 1898. Every dent tells a story.',
        'Passt der Cabin als Handgepäck?': 'Does the Cabin fit as carry-on?',
        'Made in Germany. Lifetime Guarantee. Ein Koffer für Generationen.': 'Made in Germany. Lifetime Guarantee. A suitcase for generations.',
        'Wie viel wiegt der Koffer?': 'How much does the suitcase weigh?',
        'für flexibles Packen.': 'for flexible packing.',
        'Zwei integrierte TSA Locks für maximale Sicherheit, wohin Sie auch reisen. Weltweit anerkannt — kein zusätzliches Zubehör nötig.': 'Two integrated TSA Locks for maximum security, wherever you travel. Globally recognized — no additional accessories needed.',
        'für Sicherheit weltweit und dem': 'for worldwide security and the',
        'Woraus besteht der RIMOWA Classic?': 'What is the RIMOWA Classic made of?',
        'Zwei integrierte TSA Locks sorgen für sicheres Reisen überall auf der Welt. Die Schlösser lassen sich von der Sicherheitskontrolle mit einem Universal-Generalschlüssel beschädigungsfrei öffnen — ideal für Reisen in die und aus den USA.': 'Two integrated TSA Locks ensure secure travel anywhere in the world. The locks can be opened by security control with a universal master key without damage — ideal for travel to and from the USA.',
        'Aluminium steckt Stöße weg, die Polycarbonat zerstören würden.': 'Aluminum absorbs shocks that would destroy polycarbonate.',
        'Der RIMOWA Classic ist in drei Farben erhältlich: Silver, Titan und Black. Alle drei bestehen aus demselben hochwertigen eloxierten Aluminium mit echten Lederhenkeln.': 'The RIMOWA Classic is available in three colors: Silver, Titanium, and Black. All three are made of the same high-quality anodized aluminum with genuine leather handles.',
        'Bekommt das Aluminium leicht Dellen?': 'Does the aluminum dent easily?',
        'Vier präzisionsgefertigte Räder sorgen für mühelose 360°-Mobilität auf jedem Untergrund. Das patentierte Multiwheel® System bietet flüsterleisen Lauf und herausragende Stabilität — ob auf Flughafen-Marmor oder Kopfsteinpflaster.': 'Four precision-engineered wheels ensure effortless 360° mobility on any surface. The patented Multiwheel® System offers whisper-quiet operation and outstanding stability — whether on airport marble or cobblestones.',
        'Wie reinige und pflege ich meinen Aluminium-Koffer?': 'How do I clean and care for my aluminum suitcase?',
        'Stufenloser Teleskopgriff': 'Stageless Telescopic Handle'
    }

    for ger, eng in replacements.items():
        html = html.replace(ger, eng)
        
    html = html.replace('Titan', 'Titanium')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Second translation pass successful.")

if __name__ == '__main__':
    translate_html_2(r'C:\Users\gusta\Desktop\lp\sorvete\rimowa-us\index.html')
