import os

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

    # The Services section and similar main page blocks should be the darker ambient color (#121212)
    # The cards themselves should be the elevated color (#1e1e1e)
    # We inadvertently changed section containers that had 'relative' to #1e1e1e.
    content = content.replace('bg-white dark:bg-[#1e1e1e] relative', 'bg-white dark:bg-[#121212] relative')
    content = content.replace('bg-white dark:bg-[#1e1e1e] pt-', 'bg-white dark:bg-[#121212] pt-')
    content = content.replace('bg-white dark:bg-[#1e1e1e] overflow-', 'bg-white dark:bg-[#121212] overflow-')
    
    # Portfolio grid items are bg-white dark:bg-[#1e1e1e] but they don't have bg-white classes, they are just images inside divs.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Fixed section background contrast.")
