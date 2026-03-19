import os
import re

html_files = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("portfolio.html", "Portfolio"),
    ("contact.html", "Contact")
]

base_dir = r"c:\Users\aayus\Desktop\service based site"

def get_mobile_nav_html(active_page):
    nav_items = [
        ("Home", "index.html", "ph-house"),
        ("About", "about.html", "ph-info"),
        ("Services", "services.html", "ph-sparkle"),
        ("Portfolio", "portfolio.html", "ph-image"),
        ("Contact", "contact.html", "ph-envelope-simple")
    ]
    
    html = '<nav class="md:hidden fixed bottom-6 left-4 right-4 z-50 bg-white/95 dark:bg-[#121212]/95 border border-gray-200 dark:border-gray-800 rounded-full shadow-[0_8px_32px_rgba(0,0,0,0.5)] flex justify-around items-center px-2 py-3 backdrop-blur-md bg-opacity-95">\n'
    
    for name, link, icon in nav_items:
        is_active = (name == active_page)
        color_class = "text-primary dark:text-primaryLighter" if is_active else "text-gray-500 dark:text-gray-400 hover:text-primary dark:hover:text-gray-200"
        icon_weight = "ph-fill" if is_active else "ph"
        
        html += f'''        <a href="{link}" class="flex flex-col items-center justify-center w-14 transition-colors {color_class}">
            <i class="{icon_weight} {icon} text-2xl mb-1"></i>
            <span class="text-[10px] font-medium tracking-wide">{name}</span>
        </a>\n'''
        
    html += '    </nav>'
    return html

for file_name, active_page in html_files:
    file_path = os.path.join(base_dir, file_name)
    if not os.path.exists(file_path):
        print(f"File not found: {file_name}")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Tailwind config for primaryLighter and darkMode
    config_pattern = r'tailwind\.config\s*=\s*\{.*?\}'
    new_config = '''tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        primary: '#800180',
                        primaryLight: '#a302a3',
                        primaryLighter: '#d98cd9',
                    },
                    fontFamily: {
                        sans: ['Outfit', 'sans-serif'],
                    }
                }
            }
        }'''
    content = re.sub(config_pattern, new_config, content, flags=re.DOTALL)

    # 2. Force light theme by default (override localStorage if not set to dark)
    theme_script_pattern = r'<script>\s*if\s*\(localStorage\.getItem\(\'color-theme\'\)\s*===\s*\'dark\'\s*\|\|.*?\);\}\s*else\s*\{.*?\)\;\}\s*</script>'
    new_theme_script = '''<script>
        if (localStorage.getItem('color-theme') === 'dark') {document.documentElement.classList.add('dark');} else {document.documentElement.classList.remove('dark');}
    </script>'''
    content = re.sub(theme_script_pattern, new_theme_script, content, flags=re.DOTALL)

    # 3. Make header relative and ensure no overlap
    content = content.replace('fixed w-full top-0', 'relative w-full')
    content = content.replace('sticky top-0 w-full', 'relative w-full')
    
    # 4. Remove traditional mobile menu buttons if any left
    hambuger_pattern = r'<button[^>]*class="[^"]*md:hidden[^"]*"[^>]*aria-label="Open Menu".*?</button>'
    content = re.sub(hambuger_pattern, '', content, flags=re.DOTALL)

    # 5. Inject/Update Mobile Nav
    if '<nav class="md:hidden fixed bottom-6' in content:
        content = re.sub(r'<nav class="md:hidden fixed bottom-6.*?</nav>', get_mobile_nav_html(active_page), content, flags=re.DOTALL)
    else:
        # Inject before </body>
        content = content.replace('</body>', get_mobile_nav_html(active_page) + '\n</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Successfully synced mobile bottom nav and theme logic across all pages!")
