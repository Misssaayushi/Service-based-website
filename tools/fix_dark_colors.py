import os
import re

html_files = [
    "index.html",
    "about.html",
    "services.html",
    "portfolio.html",
    "contact.html"
]

base_dir = r"c:\Users\aayus\Desktop\service based site"

for file in html_files:
    file_path = os.path.join(base_dir, file)
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix the Hero Gradient blinding light issue
    # Currently: via-white to-white
    # We want: via-white dark:via-[#121212] to-white dark:to-[#121212]
    content = content.replace("via-white to-white", "via-white dark:via-[#121212] to-white dark:to-[#121212]")
    
    # 2. Fix the bg-gray-50 missing dark blocks
    # Currently: class="py-24 bg-gray-50"
    content = re.sub(r'bg-gray-50(?!\s*dark:)', r'bg-gray-50 dark:bg-[#121212]', content)
    
    # 3. Fix the bg-white missing dark blocks
    # Specifically for Who We Are, Portfolio main sections, etc.
    content = re.sub(r'bg-white(?!\s*dark:)', r'bg-white dark:bg-[#121212]', content)
    
    # Wait, some bg-gray-50 dark:bg-[#222] might already exist.
    # We want to standardize the shades:
    # Main Backgrounds: #121212 (almost black)
    # Cards/Elevated: #1e1e1e (lighter dark)
    
    content = content.replace('dark:bg-[#111]', 'dark:bg-[#121212]')
    content = content.replace('dark:bg-[#111]/90', 'dark:bg-[#121212]/90')
    content = content.replace('dark:bg-[#181818]', 'dark:bg-[#1e1e1e]')
    content = content.replace('dark:bg-[#222]', 'dark:bg-[#1e1e1e]')
    
    # Ensure "bg-white dark:bg-[#121212]" on sections is correct, but cards might be better as #1e1e1e.
    # In index.html, cards have: bg-white dark:bg-[#1e1e1e] rounded-2xl
    # The previous script might have added dark:bg-[#181818] to those. 
    # Let's ensure rounded elements get the elevated card color.
    content = re.sub(r'dark:bg-\[#121212\](\s+rounded)', r'dark:bg-[#1e1e1e]\1', content)
    
    # Fix the stats section. It was bg-primary with white text. It should remain bg-primary dark:bg-primary or similar. It doesn't use dark classes so it's fine.
    
    # Ensure the massive purple block issue isn't caused by a missing container.
    # The massive purple block in the screenshot actually looks like the STATS section (`bg-primary`). It's missing text!
    # Wait, the stats section has `text-white` originally. If the JS crash happened, the reveal animation `opacity: 0` makes it invisible!
    # Wait, I fixed `main.js` earlier! If it's fixed, the text should be visible. 
    # But now I'm fixing the colors because user said "text is not visible in dark theme" (which was specifically the "Who We Are" section).
    # And "i don't like this shade" means the `#111` or `#181818` was not appealing. `#121212` and `#1e1e1e` is the standard Material Dark theme and looks much better. 
    
    # Let's make sure text contrast is excellent.
    content = content.replace('text-gray-600 dark:text-gray-400', 'text-gray-600 dark:text-gray-300')
    content = content.replace('text-gray-800 dark:text-gray-200', 'text-gray-800 dark:text-gray-100')
    content = content.replace('text-white/80', 'text-white/90')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Dark Mode shades updated and contrast fixed.")
