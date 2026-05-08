import os
import glob

template_dir = r"c:\Users\Khushi\OneDrive\Desktop\projects\Techsutra-e-learning-platform\TechSutraapp\templates\TechSutraapp"
html_files = glob.glob(os.path.join(template_dir, "*.html"))

hamburger_html = """
        <div class="hamburger" onclick="toggleMenu()">
            <div class="line1"></div>
            <div class="line2"></div>
            <div class="line3"></div>
        </div>
        <div class="nav-right\""""

for filepath in html_files:
    if filepath.endswith("footer.html"):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if '<div class="nav-right"' in content and 'class="hamburger"' not in content:
        content = content.replace('<div class="nav-right"', hamburger_html)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")
