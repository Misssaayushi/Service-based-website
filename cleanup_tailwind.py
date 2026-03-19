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

new_config = '''<script>
        tailwind.config = {
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
        }
    </script>'''

for file_name in html_files:
    file_path = os.path.join(base_dir, file_name)
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match the corrupted script block starting with <script> tailwind.config... </script>
    # We use a non-greedy .*? and re.DOTALL to catch everything between the tags.
    pattern = r'<script>\s*tailwind\.config\s*=\s*\{.*?</script>'
    content = re.sub(pattern, new_config, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Tailwind configurations cleaned up and standardized!")
