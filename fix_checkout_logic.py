import re

html_path = r'C:\Users\gusta\Desktop\lp\sorvete\carry-on\index.html'

def fix_checkout_logic():
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update HTML label
    html = re.sub(
        r'Color: <span id="current-color-name" style="font-weight: 700; color: #000;">.*?</span>',
        'Color: <span id="current-color-name" style="font-weight: 700; color: #d9381e;">Select a color</span>',
        html
    )

    # 2. Update initial JS variable
    # We want it to be null, but we still need _IMGS to load the default Silver images.
    # We change:
    # var currentVariantName = 'Silver';
    # var _IMGS = _VARIANTS[currentVariantName];
    # to:
    # var currentVariantName = null;
    # var _IMGS = _VARIANTS['Silver']; // Load Silver images by default
    html = re.sub(
        r"var currentVariantName = 'Silver';\s*var _IMGS = _VARIANTS\[currentVariantName\];",
        "var currentVariantName = null;\n    var _IMGS = _VARIANTS['Silver'];",
        html
    )

    # 3. Update goToCheckout function
    old_goToCheckout = r"""function goToCheckout\(\) \{
      var url = VARIANT_CHECKOUT_URLS\[currentVariantName\] \|\| VARIANT_CHECKOUT_URLS\['_default'\] \|\| '#';"""
    
    new_goToCheckout = """function goToCheckout() {
      if (!currentVariantName) {
        alert('Please select a color before proceeding to checkout.');
        var selector = document.getElementById('current-color-name');
        if (selector) selector.scrollIntoView({behavior: 'smooth', block: 'center'});
        return;
      }
      var url = VARIANT_CHECKOUT_URLS[currentVariantName] || VARIANT_CHECKOUT_URLS['_default'] || '#';"""
      
    html = re.sub(old_goToCheckout, new_goToCheckout, html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Fixed checkout logic successfully.")

if __name__ == '__main__':
    fix_checkout_logic()
