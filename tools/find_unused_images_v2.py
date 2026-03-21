import os

project_root = r"c:\Users\aayus\Desktop\service based site"
image_dirs = ["images", "assets", "mall ad"]
extensions = [".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"]

image_files = []
for d in image_dirs:
    dir_path = os.path.join(project_root, d)
    if os.path.exists(dir_path):
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if any(f.lower().endswith(ext) for ext in extensions):
                    rel_path = os.path.relpath(os.path.join(root, f), project_root)
                    image_files.append(rel_path.replace("\\", "/"))

code_contents = ""
for root, dirs, files in os.walk(project_root):
    if any(image_dir in root for image_dir in image_dirs): continue
    for f in files:
        if f.endswith((".html", ".css", ".js")):
            try:
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    code_contents += file.read() + " "
            except:
                pass

code_contents_unquoted = code_contents.replace("%20", " ")

unused = []
for img in image_files:
    basename = os.path.basename(img)
    if img not in code_contents and img not in code_contents_unquoted and \
       basename not in code_contents and basename not in code_contents_unquoted:
        unused.append(img)

print(f"UNUSED_START")
for img in unused:
    print(img)
print(f"UNUSED_END")
