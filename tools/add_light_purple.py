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

    # Add primaryLighter to tailwind config if not there
    if "primaryLighter:" not in content:
        content = content.replace("primaryLight: '#a302a3',", "primaryLight: '#a302a3',\n                        primaryLighter: '#d98cd9',")

    # Fix navigation links
    content = content.replace('text-primary font-semibold', 'text-primary dark:text-primaryLighter font-semibold')
    content = content.replace('hover:text-primary transition-colors', 'hover:text-primary dark:hover:text-primaryLighter transition-colors')
    
    # Fix logo
    content = content.replace('text-primary font-bold text-2xl', 'text-primary dark:text-primaryLighter font-bold text-2xl')
    content = content.replace('text-primary mt-1 mr-3', 'text-primary dark:text-primaryLighter mt-1 mr-3')
    content = content.replace('text-primary mr-3 text-lg', 'text-primary dark:text-primaryLighter mr-3 text-lg')
    content = content.replace('text-primary font-bold tracking-wider', 'text-primary dark:text-primaryLighter font-bold tracking-wider')

    # Fix gradient hero text (from-primary to-primaryLight -> dark:from-primaryLighter dark:to-[#eebbee])
    content = content.replace('from-primary to-primaryLight', 'from-primary to-primaryLight dark:from-primaryLighter dark:to-[#f0b3f0]')
    
    # Fix View Service links and 'Explore More' buttons
    content = content.replace('text-primary font-semibold transition-colors', 'text-primary dark:text-primaryLighter font-semibold transition-colors')
    content = content.replace('text-primary font-bold hover:text-primaryLight', 'text-primary dark:text-primaryLighter font-bold hover:text-primaryLight dark:hover:text-[#f0b3f0]')
    content = content.replace('border-primary text-primary font-semibold', 'border-primary dark:border-primaryLighter text-primary dark:text-primaryLighter font-semibold')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated all files with primaryLighter for dark mode visibility.")
