import os
import re

project_root = r"c:\Users\aayus\Desktop\service based site"
image_dirs = ["images", "assets", "mall ad"]
extensions = [".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"]

# Get all image files
image_files = []
for d in image_dirs:
    dir_path = os.path.join(project_root, d)
    if os.path.exists(dir_path):
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if any(f.lower().endswith(ext) for ext in extensions):
                    # Store relative path from project root
                    rel_path = os.path.relpath(os.path.join(root, f), project_root)
                    # Normalize to forward slashes and handle URL encoding if needed (though grep search showed space-encoded stuff)
                    image_files.append(rel_path.replace("\\", "/"))

# Scan for references in HTML, CSS, JS
used_images = set()
for root, dirs, files in os.walk(project_root):
    # Skip image dirs themselves to avoid matching the files in their own directories if we are looking at them
    if any(image_dir in root for image_dir in image_dirs):
        continue
    
    for f in files:
        if f.endswith((".html", ".css", ".js")):
            file_path = os.path.join(root, f)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as content_file:
                content = content_file.read()
                # Unquote URL encoded spaces
                content_unquoted = content.replace("%20", " ")
                for img in image_files:
                    # Match by basename or full path
                    basename = os.path.basename(img)
                    if img in content or img in content_unquoted or basename in content or basename in content_unquoted:
                        used_images.add(img)

unused_images = [img for img in image_files if img not in used_images]

print(f"Total images found: {len(image_files)}")
print(f"Used images: {len(used_images)}")
print(f"Unused images: {len(unused_images)}")
print("\nUnused Images:")
for img in unused_images:
    print(img)
