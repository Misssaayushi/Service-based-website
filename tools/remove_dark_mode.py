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

# Remove from JS main.js
js_path = os.path.join(base_dir, "js", "main.js")
if os.path.exists(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Find the block starting with // 4. Dark Mode Toggle
    # up to the end of the file.
    # Since we injected it right before the last });
    # Let's use regex to strip it.
    block_pattern = r'\s*// 4\. Dark Mode Toggle.*?\}\n'
    if "Dark Mode Toggle" in js_content:
        # Just find the end of the document
        js_content = re.sub(block_pattern, '\n', js_content, flags=re.DOTALL)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)


for file in html_files:
    file_path = os.path.join(base_dir, file)
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove FOUC script
    fouc_script = r'[ \t]*<script>\s*if \(localStorage\.getItem\(\'color-theme\'\).*?</script>\n?'
    content = re.sub(fouc_script, '', content, flags=re.DOTALL)

    # 2. Remove darkMode config
    content = content.replace("            darkMode: 'class',\n", "")

    # 3. Remove toggle button block
    # Toggle block was wrapped inside `<div class="flex items-center space-x-2">` along with the mobile menu.
    # We will search for the entire block and replace it with just the mobile menu button.
    # The structure: 
    # <div class="flex items-center space-x-2">
    #     <button id="theme-toggle"...
    #         <i ...
    #         <i ...
    #     </button>
    #     <button class="md:hidden...
    #         <i class="ph ph-list text-3xl"></i>
    #     </button>
    # </div>
    toggle_pattern = r'<div class="flex items-center space-x-2">\s*(<button id="theme-toggle".*?</button>)\s*(<button class="md:hidden.*?</button>)\s*</div>'
    match = re.search(toggle_pattern, content, flags=re.DOTALL)
    if match:
        content = content.replace(match.group(0), match.group(2))

    # 4. Remove dark:* classes globally within class="..."
    def remove_dark_classes(m):
        class_str = m.group(1)
        # removes dark:* classes
        new_class_str = re.sub(r'\s*dark:[\w\-\/]+', '', class_str)
        # remove single spacing issues
        new_class_str = " ".join(new_class_str.split())
        return 'class="' + new_class_str + '"'

    content = re.sub(r'class="([^"]+)"', remove_dark_classes, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Reverted dark mode injections.")
