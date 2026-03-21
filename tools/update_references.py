import os
import re

project_root = r"c:\Users\aayus\Desktop\service based site"

# Mapping of old directory patterns to new ones
# We handle both literal spaces and URL encoded %20
mapping = {
    r"assets/Cinema\s+-ads": "assets/cinema-ads",
    r"assets/Cinema%20-ads": "assets/cinema-ads",
    r"assets/Event\s+branding": "assets/event-branding",
    r"assets/Event%20branding": "assets/event-branding",
    r"assets/Gantries\s+and\s+unipoles": "assets/gantries-unipoles",
    r"assets/Gantries%20and%20unipoles": "assets/gantries-unipoles",
    r"assets/Highway\s+hoardings": "assets/highway-hoardings",
    r"assets/Highway%20hoardings": "assets/highway-hoardings",
    r"assets/Hoardings\s+and\s+wall\s+wraps": "assets/hoardings-wall-wraps",
    r"assets/Hoardings%20and%20wall%20%20wraps": "assets/hoardings-wall-wraps",
    r"assets/Hoardings%20and%20wall\s+wraps": "assets/hoardings-wall-wraps",
    r"assets/Logo": "assets/logo",
    r"assets/Mall\s+and\s+cinema\s+branding": "assets/mall-cinema-branding",
    r"assets/Mall%20and%20cinema%20branding": "assets/mall-cinema-branding",
    r"assets/Store\s+branding\s+indooroutdoor": "assets/store-branding",
    r"assets/Store%20branding%20indooroutdoor": "assets/store-branding",
    r"assets/Vehicle\s+branding": "assets/vehicle-branding",
    r"assets/Vehicle%20branding": "assets/vehicle-branding"
}

# Also handle "mall ad/" if it was used anywhere (though my search showed it wasn't, let's be safe)
mapping[r"mall ad/"] = "assets/mall-ad/"

def update_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    new_content = content
    for old, new in mapping.items():
        # Case insensitive match for the directory part
        new_content = re.sub(old, new, new_content, flags=re.IGNORECASE)
    
    # Also replace any remaining spaces in asset paths with hyphens for the filenames themselves if I renamed them? 
    # Wait, I didn't rename the filenames, only the directories. So the filenames still have spaces.
    # HTML uses %20 for spaces in filenames. I should leave them as is if they are %20, or keep spaces if they are spaces.
    
    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

updated_count = 0
for root, dirs, files in os.walk(project_root):
    if "tools" in root or ".git" in root: continue
    for f in files:
        if f.endswith((".html", ".css", ".js")):
            if update_file(os.path.join(root, f)):
                print(f"Updated: {f}")
                updated_count += 1

print(f"Total files updated: {updated_count}")
