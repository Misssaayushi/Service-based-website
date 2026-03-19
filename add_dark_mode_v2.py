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

toggle_button_desktop = """
                    <button id="theme-toggle-desktop" type="button" class="text-gray-600 dark:text-gray-400 hover:text-primary transition-colors text-2xl mr-6 outline-none focus:outline-none flex items-center justify-center translate-y-0.5" aria-label="Toggle dark mode">
                        <i id="theme-toggle-dark-icon-desktop" class="ph ph-moon hidden"></i>
                        <i id="theme-toggle-light-icon-desktop" class="ph ph-sun hidden"></i>
                    </button>
"""

toggle_button_mobile = """
                    <button id="theme-toggle-mobile" type="button" class="md:hidden text-gray-600 dark:text-gray-400 hover:text-primary transition-colors text-2xl outline-none focus:outline-none" aria-label="Toggle dark mode">
                        <i id="theme-toggle-dark-icon-mobile" class="ph ph-moon hidden"></i>
                        <i id="theme-toggle-light-icon-mobile" class="ph ph-sun hidden"></i>
                    </button>
"""

js_logic = """
    // 4. Dark Mode Toggle
    const themeToggleDarkIcons = document.querySelectorAll('#theme-toggle-dark-icon-desktop, #theme-toggle-dark-icon-mobile');
    const themeToggleLightIcons = document.querySelectorAll('#theme-toggle-light-icon-desktop, #theme-toggle-light-icon-mobile');
    const themeToggleBtns = document.querySelectorAll('#theme-toggle-desktop, #theme-toggle-mobile');

    if (themeToggleBtns.length > 0) {
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            themeToggleLightIcons.forEach(icon => icon.classList.remove('hidden'));
            document.documentElement.classList.add('dark');
        } else {
            themeToggleDarkIcons.forEach(icon => icon.classList.remove('hidden'));
            document.documentElement.classList.remove('dark');
        }

        themeToggleBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                themeToggleDarkIcons.forEach(icon => icon.classList.toggle('hidden'));
                themeToggleLightIcons.forEach(icon => icon.classList.toggle('hidden'));

                if (localStorage.getItem('color-theme')) {
                    if (localStorage.getItem('color-theme') === 'light') {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('color-theme', 'dark');
                    } else {
                        document.documentElement.classList.remove('dark');
                        localStorage.setItem('color-theme', 'light');
                    }
                } else {
                    if (document.documentElement.classList.contains('dark')) {
                        document.documentElement.classList.remove('dark');
                        localStorage.setItem('color-theme', 'light');
                    } else {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('color-theme', 'dark');
                    }
                }
            });
        });
    }
"""

js_path = os.path.join(base_dir, "js", "main.js")
if os.path.exists(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    if "Dark Mode Toggle" not in js_content:
        last_idx = js_content.rfind('});')
        if last_idx != -1:
            js_content = js_content[:last_idx] + js_logic + '\n' + js_content[last_idx:]
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_content)


for file in html_files:
    file_path = os.path.join(base_dir, file)
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "darkMode: 'class'" not in content:
        content = re.sub(
            r'tailwind\.config\s*=\s*\{\s*theme:',
            "tailwind.config = {\n            darkMode: 'class',\n            theme:",
            content
        )

    fouc_script = """
    <script>
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {document.documentElement.classList.add('dark');} else {document.documentElement.classList.remove('dark');}
    </script>
</head>"""
    if "color-theme" not in content and "</head>" in content:
        content = content.replace("</head>", fouc_script)

    # Add Desktop Toggle inside <nav> before the Contact Us button.
    # We find the nav block explicitly to avoid replacing CTA contact elements.
    nav_pattern = r'(<nav class="hidden md:flex space-x-8 items-center">.*?)(<a href="contact\.html"[^>]*>Contact Us</a>\s*</nav>)'
    if 'id="theme-toggle-desktop"' not in content:
        content = re.sub(nav_pattern, r'\1' + toggle_button_desktop + r'\n                    \2', content, flags=re.DOTALL)

    # Add Mobile Toggle before mobile menu button
    mobile_menu_re = r'(<button class="md:hidden[^>]*>[^<]*<i class="ph ph-list text-3xl"></i>\s*</button>)'
    if 'id="theme-toggle-mobile"' not in content:
        match = re.search(mobile_menu_re, content)
        if match:
            # Wrap the toggle and button inside a flex div
            replacement = f'<div class="flex items-center space-x-4">\n{toggle_button_mobile}\n                    {match.group(1)}\n                </div>'
            content = content.replace(match.group(0), replacement)

    # Inject dark mode classes based on reference screenshot
    content = content.replace('bg-gray-50 flex', 'bg-gray-50 dark:bg-[#111] flex', 1)
    content = content.replace('bg-white backdrop-blur-md', 'bg-white dark:bg-[#111]/90 backdrop-blur-md')
    content = content.replace('border-gray-100', 'border-gray-100 dark:border-gray-800')
    content = content.replace('border-gray-200', 'border-gray-200 dark:border-gray-800')
    content = content.replace('text-gray-800 antialiased', 'text-gray-800 dark:text-gray-200 antialiased', 1)
    content = content.replace('text-gray-900', 'text-gray-900 dark:text-white')
    content = content.replace('text-gray-800', 'text-gray-800 dark:text-gray-200')
    content = content.replace('text-gray-700', 'text-gray-700 dark:text-gray-300')
    content = content.replace('text-gray-600', 'text-gray-600 dark:text-gray-400')
    
    # Target generic white blocks
    content = re.sub(r'bg-white(\s+rounded|\s+p-|\s+pt-|\s+overflow-|\s+relative)', r'bg-white dark:bg-[#181818]\1', content)
    
    # Target gray-50 generic blocks
    content = content.replace('bg-gray-50 rounded', 'bg-gray-50 dark:bg-[#222] rounded')
    content = content.replace('bg-gray-50 border', 'bg-gray-50 dark:bg-[#222] border')
    content = content.replace('focus:border-transparent', 'focus:border-transparent dark:focus:border-primary')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Seamless dark mode logic applied.")
