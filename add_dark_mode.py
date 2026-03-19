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

toggle_button_html = """
                    <button id="theme-toggle" class="p-2 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none rounded-lg text-sm transition-colors" aria-label="Toggle Dark Mode">
                        <i id="theme-toggle-dark-icon" class="ph-fill ph-moon text-xl hidden"></i>
                        <i id="theme-toggle-light-icon" class="ph-fill ph-sun text-xl hidden"></i>
                    </button>
"""

js_logic = """
    // 4. Dark Mode Toggle
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
    const themeToggleBtn = document.getElementById('theme-toggle');

    if (themeToggleBtn && themeToggleDarkIcon && themeToggleLightIcon) {
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            themeToggleLightIcon.classList.remove('hidden');
            document.documentElement.classList.add('dark');
        } else {
            themeToggleDarkIcon.classList.remove('hidden');
            document.documentElement.classList.remove('dark');
        }

        themeToggleBtn.addEventListener('click', function() {
            themeToggleDarkIcon.classList.toggle('hidden');
            themeToggleLightIcon.classList.toggle('hidden');

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
    }
"""

js_path = os.path.join(base_dir, "js", "main.js")
if os.path.exists(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    if "Dark Mode Toggle" not in js_content:
        js_content = js_content.replace('});', js_logic + '\n});')
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
            r'tailwind\.config\s*=\s*\{',
            "tailwind.config = {\n            darkMode: 'class',",
            content
        )

    fouc_script = """
    <script>
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark')
        }
    </script>
</head>"""
    if "color-theme" not in content and "</head>" in content:
        content = content.replace("</head>", fouc_script)

    if 'id="theme-toggle"' not in content:
        if "<!-- Navigation -->" in content:
            # Add after the </nav>, wrapped in a flex div with the mobile menu.
            # We want: 
            # </nav>
            # <div class="flex items-center space-x-2"> 
            #    toggle_button
            #    mobile_menu
            # </div>
            
            nav_end = r'(</nav>\s*)(<button class="md:hidden[^>]*>[^<]*<i[^>]*></i>\s*</button>)'
            match = re.search(nav_end, content)
            if match:
                replacement = f"{match.group(1)}<div class=\"flex items-center space-x-2\">\n{toggle_button_html}\n{match.group(2)}\n                </div>"
                content = content.replace(match.group(0), replacement)
        
    # Inject dark mode classes
    replacements = [
        ('text-gray-800 antialiased bg-gray-50', 'text-gray-800 dark:text-gray-200 antialiased bg-gray-50 dark:bg-gray-900'),
        ('bg-white/90', 'bg-white/90 dark:bg-gray-900/90'),
        ('text-gray-900', 'text-gray-900 dark:text-white'),
        ('border-gray-100', 'border-gray-100 dark:border-gray-800'),
        ('border-gray-200', 'border-gray-200 dark:border-gray-800'),
        ('border-gray-300', 'border-gray-300 dark:border-gray-700'),
        ('bg-white ', 'bg-white dark:bg-gray-800 '),
        ('bg-white', 'bg-white dark:bg-gray-800'),
        ('hover:bg-gray-50', 'hover:bg-gray-50 dark:hover:bg-gray-700'),
        ('bg-gray-50 rounded-3xl', 'bg-gray-50 dark:bg-gray-800 rounded-3xl'),
    ]
    
    # We only inject if it's not already fully dark-mode injected
    if 'dark:bg-gray-900' not in content:
        for old, new in replacements:
            # We enforce exact replacements or near exact safely to prevent bloating
            content = content.replace(old, new)

        # Fix specific body text
        content = content.replace('dark:bg-gray-800 dark:bg-gray-800', 'dark:bg-gray-800')
        content = content.replace('text-gray-600', 'text-gray-600 dark:text-gray-400')
        content = content.replace('text-gray-700', 'text-gray-700 dark:text-gray-300')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Dark mode script applied.")
