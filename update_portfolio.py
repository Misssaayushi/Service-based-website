import os
import re

base_dir = r"c:\Users\aayus\Desktop\service based site\assets"
portfolio_file = r"c:\Users\aayus\Desktop\service based site\portfolio.html"

folder_metadata = {
    "Event branding": {
        "heading": "Event Branding",
        "descs": [
            "Immersive visual experiences that steal the show.",
            "Creating memorable moments for every attendee.",
            "High-impact branding for unforgettable events.",
            "Transforming spaces with dynamic creative assets.",
            "Engaging event setups that capture the audience."
        ]
    },
    "Gantries and unipoles": {
        "heading": "Gantries & Unipoles",
        "descs": [
            "Strategic placements driving mass urban visibility.",
            "Towering above the traffic with a bold message.",
            "High-visibility structural setups for brands.",
            "Commanding attention across busy intersections.",
            "Maximum exposure daily with premium unipoles."
        ]
    },
    "Highway hoardings": {
        "heading": "Highway Hoardings",
        "descs": [
            "Commanding attention on major transport routes.",
            "Unmissable displays targeting daily commuters.",
            "Massive scale branding along the busiest highways.",
            "Strategic outdoor advertising built for scale.",
            "Capturing the eyes of thousands on the open road."
        ]
    },
    "Hoardings and wall  wraps": {
        "heading": "Wall Wraps & Hoardings",
        "descs": [
            "Transformative large-scale outdoor canvases.",
            "Turning bare walls into stunning brand stories.",
            "City-scale advertisements integrated into architecture.",
            "Vast hoardings masking construction with creativity.",
            "Impactful street-level building branding."
        ]
    },
    "Mall and cinema branding": {
        "heading": "Mall & Cinema",
        "descs": [
            "Engaging targeted audiences at premium venues.",
            "Captivating shoppers during their leisure time.",
            "Big screen pre-show advertising experiences.",
            "Strategic retail space promotions and displays.",
            "Interactive and vibrant mall installations."
        ]
    },
    "Store branding indooroutdoor": {
        "heading": "Store Branding",
        "descs": [
            "Creative retail solutions inside and out.",
            "Enhancing the customer journey from the storefront.",
            "Dynamic window displays and interior visual design.",
            "Transforming retail spaces into immersive brand hubs.",
            "Eye-catching store fascias and signage."
        ]
    },
    "Vehicle branding": {
        "heading": "Transit Media",
        "descs": [
            "Taking campaigns effortlessly on the move.",
            "Full vehicle wraps maximizing street presence.",
            "Dynamic transit advertising reaching every neighborhood.",
            "Mobile billboards delivering messages citywide.",
            "High-recall fleet branding that drives visibility."
        ]
    },
}

html_blocks = []

for root, dirs, files in os.walk(base_dir):
    folder_name = os.path.basename(root)
    if folder_name == "Logo":
        continue
        
    meta = folder_metadata.get(folder_name)
    if not meta and folder_name != "assets":
        meta = {
            "heading": folder_name.title(), 
            "descs": [
                "Stunning outdoor branding execution.",
                "Innovative visual storytelling in public.",
                "Premium exposure for forward-thinking brands.",
                "Transforming ordinary spaces into stages.",
                "Captivating audiences wherever they go."
            ]
        }
        
    if not meta:
        continue
        
    descs = meta['descs']
    
    valid_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    for i, f in enumerate(valid_files):
        rel_path = f"assets/{folder_name}/{f}"
        desc = descs[i % len(descs)]
        
        block = f"""
                <div class="group relative block h-72 rounded-2xl overflow-hidden shadow-[0_4px_20px_rgb(0,0,0,0.05)] hover:shadow-[0_20px_40px_rgb(128,1,128,0.15)] transition-all duration-300 transform group-hover:-translate-y-1">
                    <img src="{rel_path.replace(' ', '%20')}" alt="{meta['heading']}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" loading="lazy">
                    <div class="absolute inset-0 bg-gradient-to-t from-gray-900/95 via-gray-900/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                        <h4 class="text-white font-bold text-2xl mb-2 translate-y-4 group-hover:translate-y-0 transition-transform duration-300">{meta['heading']}</h4>
                        <p class="text-white/90 text-sm translate-y-4 group-hover:translate-y-0 transition-transform duration-300 delay-75 line-clamp-2">{desc}</p>
                    </div>
                </div>"""
        html_blocks.append(block)

grid_html = '\n'.join(html_blocks)

with open(portfolio_file, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(<div class="grid grid-cols-1 md:grid-cols-3 gap-6">).*?(</div>\s*</div>\s*</main>)'
new_content = re.sub(pattern, r'\1\n' + grid_html + r'\n            \2', content, flags=re.DOTALL)

with open(portfolio_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {portfolio_file} with {len(html_blocks)} images with varied descriptions.")
