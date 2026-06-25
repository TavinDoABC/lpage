import re
import json

HTML_PATH = r'C:\Users\gusta\Desktop\lp\sorvete\rimowa-us\index.html'
def translate_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # --- 1. Global replacements for UI elements and short strings ---
    replacements = {
        'Kostenloser Versand in ganz Deutschland — immer. Lieferung in 6–14 Werktagen.': 'Free shipping across the United States — always. Delivery in 6–14 business days.',
        'Kostenlose Rückgabe innerhalb von 30 Tagen nach Erhalt. Der Koffer muss in Originalverpackung und im Originalzustand zurückgesendet werden.': 'Free returns within 30 days of receipt. The suitcase must be returned in its original packaging and condition.',
        '🇩🇪 Exklusives Angebot für Deutschland — streng limitiert. Gültig bis': '🇺🇸 Exclusive offer for the United States — strictly limited. Valid until',
        'In den Warenkorb': 'Add to Cart',
        'Auf Lager': 'In Stock',
        'Farbe:': 'Color:',
        'Größe:': 'Size:',
        'Silber': 'Silver',
        'Schwarz': 'Black',
        'Kundenbewertungen': 'Customer Reviews',
        'Bewertungen': 'Reviews',
        'Bewertung schreiben': 'Write a Review',
        'Mehr Bewertungen laden': 'Load More Reviews',
        'Alle Bewertungen': 'All Reviews',
        'Verifiziert': 'Verified',
        'Foto': 'Photo',
        'Alle Rechte vorbehalten.': 'All rights reserved.',
        'Datenschutz': 'Privacy Policy',
        'Impressum': 'Imprint',
        'Lebenslange Garantie': 'Lifetime Guarantee',
        'Kostenloser Versand': 'Free Shipping',
        '30 Tage Rückgaberecht': '30-Day Returns',
        'Jetzt kaufen': 'Buy Now',
        'Nur noch — Stück verfügbar — exklusives Deutschland-Angebot': 'Only — pieces left in stock — exclusive US offer',
        'Gewicht:': 'Weight:',
        'Abmessungen:': 'Dimensions:',
        'Material:': 'Material:',
        'Garantie:': 'Warranty:',
        'Ideal für 3–4 Tage Reise': 'Ideal for a 3-4 day trip',
        'Ideal für 1–2 Wochen Reise': 'Ideal for a 1-2 week trip',
        'Ideal für über 2 Wochen Reise': 'Ideal for a 2+ week trip',
        'Ideal für längere Reisen': 'Ideal for longer trips',
        'Multiwheel®-System': 'Multiwheel® System',
        'TSA-Schlösser': 'TSA Locks',
        'Flex-Divider': 'Flex Divider',
        'Eloxiertes Aluminium': 'Anodized Aluminum',
        'Produktdetails': 'Product Details',
        'Produktinformationen': 'Product Information',
        'Produktvideo abspielen': 'Play Product Video',
        'Ansicht': 'View',
        'Häufig gestellte Fragen': 'Frequently Asked Questions',
        'Vergleichen Sie die Größen': 'Compare Sizes',
        'Was ist in der Box?': 'What\'s in the box?',
        'Pflegehinweise': 'Care Instructions',
        'Materialien': 'Materials',
        'Entdecken Sie die RIMOWA Classic Kollektion.': 'Discover the RIMOWA Classic Collection.',
        'Der RIMOWA Classic ist die Stilikone unter den Reisekoffern. Gefertigt aus hochwertigem eloxiertem Aluminium mit charakteristischen Lederhenkeln und dem unverkennbaren Rillendesign, das seit 1898 den Maßstab setzt.': 'The RIMOWA Classic is the style icon among suitcases. Crafted from high-quality anodized aluminum with characteristic leather handles and the unmistakable groove design that has set the standard since 1898.',
        'Der RIMOWA Classic ist der definitive Ausdruck deutscher Koffer-Ingenieurskunst. Seit 1898 steht RIMOWA für kompromisslose Qualität — und der Classic verkörpert dieses Erbe in seiner reinsten Form.': 'The RIMOWA Classic is the definitive expression of German suitcase engineering. Since 1898, RIMOWA has stood for uncompromising quality — and the Classic embodies this heritage in its purest form.',
        'Gefertigt aus hochwertigem eloxiertem Aluminium mit charakteristischen Lederhenkeln und dem legendären Rillendesign, das die Marke seit 1898 prägt. Jeder Koffer wird in Deutschland entworfen und mit höchster Präzision gebaut.': 'Crafted from high-quality anodized aluminum with characteristic leather handles and the legendary groove design that has shaped the brand since 1898. Each suitcase is designed in Germany and built with the highest precision.',
        'Vier präzisionsgefertigte Räder sorgen für mühelose 360°-Mobilität auf jedem Untergrund. Das patentierte Multiwheel®-System bietet flüsterleisen Lauf und herausragende Stabilität — ob auf Flughafen-Marmor oder Kopfsteinpflaster.': 'Four precision-engineered wheels ensure effortless 360° mobility on any surface. The patented Multiwheel® system offers whisper-quiet operation and outstanding stability — whether on airport marble or cobblestones.',
        'Zwei integrierte TSA-Schlösser sorgen für sicheres Reisen überall auf der Welt. Die Schlösser lassen sich von der Sicherheitskontrolle mit einem Universal-Generalschlüssel beschädigungsfrei öffnen — ideal für Reisen in die und aus den USA.': 'Two integrated TSA locks ensure secure travel anywhere in the world. The locks can be opened by security control with a universal master key without damage — ideal for travel to and from the USA.',
        'Das flexible Trennsystem lässt Sie die Innenaufteilung für jede Art von Reise individuell gestalten. Businesskleidung auf der einen, Freizeitkleidung auf der anderen Seite, oder kompaktes Packen für einen Wochenendtrip — der Flex Divider passt sich Ihren Bedürfnissen an.': 'The flexible divider system allows you to customize the interior layout for any type of trip. Business attire on one side, casual wear on the other, or compact packing for a weekend trip — the Flex Divider adapts to your needs.',
        'Der stufenlose Teleskopgriff lässt sich auf jede Höhe einstellen und bietet mit ergonomischem Ledereinsatz maximalen Komfort — selbst auf den längsten Wegen durch das Flughafenterminal.': 'The stageless telescopic handle can be adjusted to any height and offers maximum comfort with an ergonomic leather insert — even on the longest walks through the airport terminal.',
        'Jeder RIMOWA Classic wird nach höchsten deutschen Qualitätsstandards gefertigt. Mit der lebenslangen Garantie steht RIMOWA für die Langlebigkeit seiner Produkte ein — ein Koffer, der Generationen überdauert.': 'Every RIMOWA Classic is manufactured to the highest German quality standards. With a lifetime guarantee, RIMOWA stands for the longevity of its products — a suitcase that outlasts generations.',
        'Der RIMOWA Classic besteht aus hochwertigem eloxiertem Aluminium. Das Innenfutter ist aus Polyester, die Henkel aus echtem Leder und die Räder aus Hartkunststoff. Die Fächer des Flex Dividers sind ebenfalls aus Polyester.': 'The RIMOWA Classic is made of high-quality anodized aluminum. The interior lining is made of polyester, the handles are genuine leather, and the wheels are hard plastic. The compartments of the Flex Divider are also made of polyester.',
        'Ihr Koffer wird mit einem gratis Lederanhänger fürs Gepäck und einem RIMOWA Sticker geliefert. Der Flex Divider, die TSA-Schlösser und der stufenlos verstellbare Teleskopgriff sind alle fest integriert.': 'Your suitcase comes with a free leather luggage tag and a RIMOWA sticker. The Flex Divider, TSA locks, and stageless telescopic handle are all fully integrated.',
        'Wischen Sie die Oberfläche mit einem weichen, feuchten Tuch ab. Vermeiden Sie scheuernde Reinigungsmittel oder aggressive Chemikalien. Bei hartnäckigen Flecken empfiehlt RIMOWA eine milde Seife mit warmem Wasser.': 'Wipe the surface with a soft, damp cloth. Avoid abrasive cleaners or harsh chemicals. For stubborn stains, RIMOWA recommends a mild soap with warm water.',
        'Aluminium ist von Natur aus weicher als Polycarbonat und kann bei grober Behandlung Dellen bekommen. Bei RIMOWA gehört das zum Charakter — jede Delle erzählt eine Reisegeschichte. Dennoch ist das Material extrem robust und schützt Ihre Sachen zuverlässig.': 'Aluminum is naturally softer than polycarbonate and can dent with rough handling. At RIMOWA, this is part of its character — every dent tells a travel story. Nevertheless, the material is extremely robust and reliably protects your belongings.',
        'Der RIMOWA Classic ist in drei Farben erhältlich: Silber, Titan und Schwarz. Alle drei bestehen aus demselben hochwertigen eloxierten Aluminium mit echten Lederhenkeln.': 'The RIMOWA Classic is available in three colors: Silver, Titanium, and Black. All three are made of the same high-quality anodized aluminum with genuine leather handles.',
        'Ja. Der RIMOWA Classic Cabin (55 × 40 × 23 cm) erfüllt die IATA-Handgepäckempfehlungen und passt in die Gepäckfächer der meisten großen Fluggesellschaften wie Lufthansa, Eurowings, Condor und Discover Airlines. Für Billigflieger mit strengeren Maßvorgaben (z. B. Ryanair oder Wizz Air) empfehlen wir den Cabin S (55 × 40 × 20 cm).': 'Yes. The RIMOWA Classic Cabin (55 × 40 × 23 cm) meets the IATA cabin baggage recommendations and fits in the overhead compartments of most major airlines like Delta, United, and American Airlines. For budget airlines with stricter size limits (e.g., Spirit or Frontier), we recommend the Cabin S (55 × 40 × 20 cm).',
        'TSA-Schlösser lassen sich von der Sicherheitskontrolle mit einem Universal-Generalschlüssel öffnen — ohne das Schloss zu beschädigen. Ihr Koffer bleibt während der gesamten Reise sicher verschlossen und kann an jeder Sicherheitskontrolle dennoch geprüft werden. Besonders praktisch bei Reisen in die USA.': 'TSA locks can be opened by security control with a universal master key — without damaging the lock. Your suitcase remains securely locked throughout the journey and can still be inspected at any security checkpoint. Especially practical when traveling to the USA.',
        'Sie haben 30 Tage ab Erhalt Zeit, den Koffer in Originalverpackung und im Originalzustand zurückzusenden. Der Rückversand ist kostenlos. Sobald wir den Artikel erhalten haben, prüfen wir ihn und erstatten den Betrag innerhalb von 5–7 Werktagen.': 'You have 30 days from receipt to return the suitcase in its original packaging and condition. Return shipping is free. Once we receive the item, we will inspect it and refund the amount within 5–7 business days.',
        'RIMOWA gewährt eine lebenslange Garantie auf alle Koffer der Classic Collection. Sie deckt Herstellungsfehler und Materialversagen bei normalem Gebrauch ab. Normale Gebrauchsspuren oder durch Fluggesellschaften verursachte Schäden sind nicht abgedeckt.': 'RIMOWA offers a lifetime guarantee on all suitcases in the Classic Collection. It covers manufacturing defects and material failure under normal use. Normal wear and tear or damage caused by airlines are not covered.',
        'Die lebenslange Garantie deckt Herstellungsfehler und Materialversagen bei normalem Gebrauch ab.': 'The lifetime guarantee covers manufacturing defects and material failure under normal use.',
        'Leicht, robust und unverkennbar. Die ikonischen Rillen sind nicht nur Design — sie verstärken die Struktur.': 'Lightweight, robust, and unmistakable. The iconic grooves aren\'t just design — they reinforce the structure.',
        'Premium-Aluminium mit dem legendären Rillendesign. Leicht, langlebig und unverkennbar — ein Koffer, der Charakter entwickelt.': 'Premium aluminum with the legendary groove design. Lightweight, durable, and unmistakable — a suitcase that develops character.',
        'Zwei integrierte TSA-Schlösser für maximale Sicherheit, wohin Sie auch reisen. Weltweit anerkannt — kein zusätzliches Zubehör nötig.': 'Two integrated TSA locks for maximum security, wherever you travel. Globally recognized — no additional accessories needed.',
        'Integrierte TSA-Schlösser für sicheres Reisen weltweit. Kein zusätzliches Vorhängeschloss nötig.': 'Integrated TSA locks for secure travel worldwide. No additional padlock needed.',
        'Das flexible Trennsystem passt sich Ihrem Packstil an. Geschäftsreise oder Wochenendtrip — für jede Reise die passende Aufteilung.': 'The flexible divider system adapts to your packing style. Business trip or weekend getaway — the right layout for every journey.',
        'Flex-Divider-System für eine anpassbare Aufteilung. Alles an seinem Platz.': 'Flex-Divider system for a customizable layout. Everything in its place.',
        'Vier präzisionsgefertigte Räder für mühelose 360°-Mobilität. Flüsterleise, grundsolide und zuverlässig auf jedem Untergrund.': 'Four precision-engineered wheels for effortless 360° mobility. Whisper-quiet, rock-solid, and reliable on any surface.',
        'Vier leichtgängige Räder für 360°-Mobilität. Flüsterleise und mühelos auf jedem Untergrund.': 'Four smooth-rolling wheels for 360° mobility. Whisper-quiet and effortless on any surface.',
        'Volumen — genug für ein langes Wochenende, kompakt genug fürs Handgepäckfach.': 'Volume — enough for a long weekend, compact enough for the overhead compartment.',
        'wiegt 6,0 kg, fasst 100 Liter und misst 75 × 47 × 36 cm. Alle werden aus hochwertigem eloxiertem Aluminium mit Lederhenkeln gefertigt.': 'weighs 6.0 kg, holds 100 liters, and measures 75 × 47 × 36 cm. All are crafted from high-quality anodized aluminum with leather handles.',
        'Schritt 01': 'Step 01',
        'Schritt 02': 'Step 02',
        'Schritt 03': 'Step 03',
        'Schritt 04': 'Step 04',
        'Familienurlaub': 'Family Vacation',
        'Ausgestattet mit dem': 'Equipped with the',
        'Original Classic Cabin': 'Original Classic Cabin',
        'Bewertungsfoto': 'Review Photo',
        'Kostenlose Lieferung': 'Free Delivery'
    }

    for ger, eng in replacements.items():
        html = html.replace(ger, eng)

    # Convert Euro currency formatting to USD
    # e.g., 229,00 € -> $229.00
    # 1.625,00 € -> $1,625.00
    html = re.sub(r'(\d+)\.(\d{3}),(\d{2})\s*€', r'$\1,\2.\3', html) # e.g. 1.625,00 €
    html = re.sub(r'(\d+),(\d{2})\s*€', r'$\1.\2', html) # e.g. 229,00 €
    
    # Optional: adjust date formats for US (DD.MM.YYYY to MM/DD/YYYY if they exist in plain text)
    # Most dates are generated by JS so we can tweak the JS.

    # --- 2. Translate REVIEWS_DATA ---
    # Since REVIEWS_DATA is a JSON string embedded in JS, we can parse it, translate, and put it back.
    # To be safe, we'll extract it using regex.
    reviews_match = re.search(r'var REVIEWS_DATA = (\[.*?\]);', html, re.DOTALL)
    if reviews_match:
        reviews_str = reviews_match.group(1)
        
        # Translate the reviews using simple string replacement for the known 22 reviews
        # (This is tedious, but we can do a quick mapping or just replace some key phrases)
        review_replacements = {
            'Einmal anfassen und man versteht es': 'Touch it once and you understand',
            'Sobald man einen RIMOWA einmal gerollt hat, versteht man es — man begreift genau, warum er kostet, was er kostet. Die Räder gleiten auf praktisch jedem Untergrund wie Butter, und ihn durch einen vollen Flughafen zu manövrieren macht richtig Spaß. Nach einem Leben mit normalem Gepäck war das ein echter Wow-Moment — der Unterschied ist sofort spürbar. Und die Langlebigkeit ist kein Witz: Als das Innenfutter bei un': 'Once you\'ve rolled a RIMOWA, you understand — you realize exactly why it costs what it costs. The wheels glide like butter on practically any surface, and maneuvering it through a crowded airport is actually fun. After a lifetime of normal luggage, this was a real wow moment — the difference is immediately noticeable. And the durability is no joke: When the lining un',
            'Endlich — und keine Sekunde bereut': 'Finally — and haven\'t regretted a second',
            'Ich habe so lange von diesem Koffer geträumt und endlich zugeschlagen. Die Qualität ist jeden Cent wert.': 'I dreamed of this suitcase for so long and finally bought it. The quality is worth every penny.',
            'Das perfekte Handgepäck — für immer': 'The perfect carry-on — forever',
            'Das perfekte Handgepäck. Ich reise viel beruflich und brauchte etwas Verlässliches. Der Classic Cabin sieht nicht nur extrem professionell aus, er hält auch, was er verspricht. Die Verarbeitung ist absolut makellos.': 'The perfect carry-on. I travel a lot for work and needed something reliable. The Classic Cabin doesn\'t just look extremely professional, it also delivers on its promises. The craftsmanship is absolutely flawless.',
            'Einfach perfekt': 'Simply perfect',
            'Der RIMOWA Cabin ist schlicht und einfach perfekt. Das Design ist zeitlos, das Material unverwüstlich. Jeden Euro wert.': 'The RIMOWA Cabin is plain and simply perfect. The design is timeless, the material indestructible. Worth every dollar.',
            'Kein anderer Koffer kommt da ran': 'No other suitcase comes close',
            'Wenn man einmal einen RIMOWA benutzt hat, will man nie wieder etwas anderes. Unglaubliches Produkt.': 'Once you\'ve used a RIMOWA, you never want anything else. Incredible product.',
            'Unglaublich geschmeidig': 'Incredibly smooth',
            'Ich liebe meinen RIMOWA. Er ist geräumig und rollt unglaublich geschmeidig.': 'I love my RIMOWA. It\'s spacious and rolls incredibly smoothly.',
            'Liebe auf den ersten Blick': 'Love at first sight',
            'Ich habe mir vor Kurzem einen RIMOWA gegönnt — und ich bin völlig hin und weg. Das elegante Aluminium-Design zieht Blicke auf sich, ist dabei aber kratzfest und unglaublich robust. Die Räder rollen mühelos, die Innenaufteilung ist durchdacht und praktisch. Ja, er ist nicht billig — aber glaubt mir, er ist jeden Cent wert.': 'I recently treated myself to a RIMOWA — and I am completely blown away. The elegant aluminum design turns heads, but is also scratch-resistant and incredibly robust. The wheels roll effortlessly, the interior layout is thoughtful and practical. Yes, it\'s not cheap — but believe me, it\'s worth every cent.',
            'Beweist mir das Gegenteil': 'Prove me wrong',
            'RIMOWA ist einfach unglaublich. Ich bin mit diesem Koffer um die halbe Welt gereist — und er steckt alles weg. Die Qualität ist unübertroffen, und die Räder sind mit Abstand die besten der Branche: Sie gleiten selbst auf rauen Oberflächen wie auf Schienen. Stilvoll, robust und bereit für jedes Abenteuer. Ich habe nirgendwo besseres Gepäck gefunden. Beweist mir das Gegenteil.': 'RIMOWA is simply incredible. I\'ve traveled halfway around the world with this suitcase — and it handles everything. The quality is unsurpassed, and the wheels are by far the best in the industry: They glide like they\'re on rails, even on rough surfaces. Stylish, robust, and ready for any adventure. I haven\'t found better luggage anywhere. Prove me wrong.',
            '11 Koffer später — keine Reue': '11 suitcases later — no regrets',
            'Meinen ersten RIMOWA habe ich 2019 bekommen und mich sofort verliebt. Ja, sie sind teuer — aber in 7 Jahren Reisen ist mir nie auch nur ein einziger Koffer kaputtgegangen. Allein das ist es wert. Und die Räder... die sind einfach in einer eigenen Liga.\\n\\nDie meisten habe ich auf Reisen gekauft, vor allem hier in Deutschland und im europäischen Ausland. Inzwischen sind es 11 — 9 behalte ich, 2 habe ich meinen Eltern geschenkt. Einmal RIMOWA, immer RIMOWA.': 'I got my first RIMOWA in 2019 and fell in love immediately. Yes, they are expensive — but in 7 years of traveling, I haven\'t had a single suitcase break. That alone is worth it. And the wheels... they are simply in a league of their own.\\n\\nI bought most of them while traveling, especially here in Germany and other European countries. Now I have 11 — I kept 9, gave 2 to my parents. Once RIMOWA, always RIMOWA.',
            'Die Investition, die sich wirklich auszahlt': 'The investment that really pays off',
            'Unglaubliches Produkt. Zeitloses Design, makellose Qualität. Beim Preis habe ich zuerst gezögert — aber jetzt weiß ich, dass es absolut die richtige Entscheidung war. RIMOWA hält. Davor habe ich immer billige Koffer gekauft, die auseinanderfielen — abbrechende Räder, aufplatzende Reißverschlüsse, splitternde Schalen. Der ständige Ersatz hat am Ende mehr gekostet. Mit meinen RIMOWAs bin ich schon mehrfach um die Welt gereist. Diese 4 Spinner-Räder sind ein absoluter Traum — Reisen fühlt sich so mühelos an.': 'Incredible product. Timeless design, flawless quality. I hesitated at the price at first — but now I know it was absolutely the right decision. RIMOWA lasts. Before this, I always bought cheap suitcases that fell apart — breaking wheels, bursting zippers, splintering shells. The constant replacements ended up costing more. I\'ve traveled around the world several times with my RIMOWAs. These 4 spinner wheels are an absolute dream — traveling feels so effortless.',
            'Für immer. Keine Übertreibung.': 'Forever. No exaggeration.',
            'Ja, es lohnt sich. Dieser Koffer hält ein Leben lang. RIMOWA steht hinter seinen Produkten, bietet eine großzügige Garantie und repariert oder ersetzt Mängel ohne jeden Aufwand. Einfach kaufen und nie wieder daran denken.': 'Yes, it\'s worth it. This suitcase lasts a lifetime. RIMOWA stands behind its products, offers a generous warranty, and repairs or replaces defects with zero hassle. Just buy it and never think about it again.',
            '100% Empfehlung — keine Frage': '100% recommendation — no question',
            'Diese Koffer sind einfach fantastisch. Super praktisch, unglaublich geschmeidig zu rollen 🤩 Außerdem leicht und wunderschön — die Leute bleiben am Flughafen tatsächlich stehen und schauen. 100% Empfehlung!': 'These suitcases are just fantastic. Super practical, incredibly smooth to roll 🤩 Also lightweight and beautiful — people actually stop and look at the airport. 100% recommendation!',
            'So gut, dass ich gleich mehrere gekauft habe': 'So good that I bought several',
            'Ich bin absolut verliebt in meinen neuen Cabin. Der Griff ist der bequemste, den ich je an einem Koffer hatte — und die Räder rollen unglaublich geschmeidig. Ich war so begeistert, dass ich direkt zurückgegangen bin und noch ein paar für meine Familie gekauft habe.': 'I am absolutely in love with my new Cabin. The handle is the most comfortable I\'ve ever had on a suitcase — and the wheels roll incredibly smoothly. I was so thrilled that I went straight back and bought a few more for my family.',
            'Einmal kaufen — für immer besitzen': 'Buy once — own forever',
            'RIMOWA-Produkte sehen nicht nur fantastisch aus, sie sind nach höchsten Standards gefertigt. Sie funktionieren makellos und kommen mit lebenslanger Garantie — das macht es zu einem einmaligen Kauf, der den Preis völlig rechtfertigt.': 'RIMOWA products don\'t just look fantastic, they are manufactured to the highest standards. They function flawlessly and come with a lifetime guarantee — making it a one-time purchase that completely justifies the price.',
            'Dezent. Aber jeder erkennt es.': 'Subtle. But everyone recognizes it.',
            'Das ultimative Reise-Statussymbol für alle, die es lieber zurückhaltend mögen. Man muss kein Wort sagen — der Koffer sagt alles.': 'The ultimate travel status symbol for those who prefer to keep it low-key. You don\'t have to say a word — the suitcase says it all.',
            'Zeitlose Ikonen — deutsche Ingenieurskunst vom Feinsten': 'Timeless icons — German engineering at its finest',
            '2022 habe ich mir den Original Cabin geholt und meinem Partner den Classic Cabin. Beide sind seitdem treue Begleiter auf unzähligen Reisen. RIMOWA macht einfach zeitlose Ikonen — deutsche Ingenieurskunst auf absolutem Höchstniveau.': 'In 2022, I got the Original Cabin and my partner the Classic Cabin. Both have been faithful companions on countless trips since then. RIMOWA simply makes timeless icons — German engineering at the absolute highest level.',
            'Schön, geräumig, jeden Euro wert': 'Beautiful, spacious, worth every dollar',
            'Der Kauf war reibungslos — einfach und unkompliziert. Mein RIMOWA Cabin ist geräumig, öffnet und schließt mühelos, sieht absolut umwerfend aus und ist den Preis komplett wert.': 'The purchase was smooth — simple and uncomplicated. My RIMOWA Cabin is spacious, opens and closes effortlessly, looks absolutely stunning, and is completely worth the price.',
            'Die besten Koffer der Welt — Punkt.': 'The best suitcases in the world — period.',
            'RIMOWA macht einfach das beste Gepäck — da gibt es nichts zu diskutieren. Riesiges Volumen und trotzdem leicht. Dreht und rollt wie ein Traum. Hält ein Leben lang. Jeden Euro wert — und noch mehr!': 'RIMOWA simply makes the best luggage — there is nothing to discuss. Huge volume and yet lightweight. Turns and rolls like a dream. Lasts a lifetime. Worth every dollar — and more!',
            'Begeistert schon vor der ersten Reise': 'Thrilled even before the first trip',
            'Ich wollte nur meine ersten Eindrücke von meinem neuen RIMOWA Cabin teilen. Ich hatte noch keine Gelegenheit, ihn auf eine Reise mitzunehmen — aber ich bin jetzt schon ehrlich begeistert. Die Verarbeitungsqualität, das Gefühl des Aluminiums, die Handwerkskunst insgesamt — genau das, was ich mir erhofft hatte. Alles daran strahlt Langlebigkeit und durchdachtes Design aus.\\n\\nIch kann es kaum erwarten, ihn endlich auf einer Reise zu nutzen — aber schon vom ersten Eindruck her ist klar: Das ist ein Koffer, der bleibt.': 'I just wanted to share my first impressions of my new RIMOWA Cabin. I haven\'t had a chance to take it on a trip yet — but I am honestly thrilled already. The build quality, the feel of the aluminum, the overall craftsmanship — exactly what I had hoped for. Everything about it radiates durability and thoughtful design.\\n\\nI can\'t wait to finally use it on a trip — but from the first impression alone it\'s clear: This is a suitcase that stays.',
            'Mein erster RIMOWA — definitiv nicht mein letzter': 'My first RIMOWA — definitely not my last',
            'Mein erster RIMOWA — und was für ein Einstieg. Der Cabin hat die perfekte Größe und die Qualität ist einfach erstklassig. Der Versand war schnell und das Tracking hat mich bei jedem Schritt auf dem Laufenden gehalten. Ja, er ist nicht billig — aber ich plane schon, mir bald die nächstgrößere Variante zu holen. Absolute Empfehlung!': 'My first RIMOWA — and what a start. The Cabin is the perfect size and the quality is simply first class. Shipping was fast and the tracking kept me updated every step of the way. Yes, it\'s not cheap — but I\'m already planning to get the next larger version soon. Absolute recommendation!',
            'Kaum zu übersehen — aus gutem Grund': 'Hard to miss — for good reason',
            'RIMOWA ist eine ikonische Gepäckmarke, an der man einfach nicht vorbeikommt, wenn man es ernst meint mit wirklich gutem Gepäck.': 'RIMOWA is an iconic luggage brand that you simply cannot ignore if you are serious about truly good luggage.',
            'Man bekommt, wofür man bezahlt': 'You get what you pay for',
            'Der Bestellvorgang und das Tracking waren hervorragend! Man bekommt hier wirklich genau das, wofür man bezahlt. Absolut jeden Cent wert!': 'The ordering process and tracking were outstanding! You really get exactly what you pay for here. Absolutely worth every cent!'
        }

        for ger, eng in review_replacements.items():
            reviews_str = reviews_str.replace(ger, eng)

        html = html.replace(reviews_match.group(1), reviews_str)
        
    # Translate JS date formatter: `new Date(d).toLocaleDateString('de-DE'` -> `new Date(d).toLocaleDateString('en-US'`
    html = html.replace("toLocaleDateString('de-DE'", "toLocaleDateString('en-US'")
    
    # Translate months if any
    html = html.replace('Januar', 'January').replace('Februar', 'February').replace('März', 'March').replace('Mai', 'May').replace('Juni', 'June').replace('Juli', 'July').replace('Oktober', 'October').replace('Dezember', 'December')
    
    # Currency in specific script elements where it might be raw
    html = html.replace('229,00 €', '$229.00').replace('1.625,00 €', '$1,625.00')

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("HTML translation applied successfully.")

if __name__ == '__main__':
    translate_html(HTML_PATH)
