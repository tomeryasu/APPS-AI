import os
import zipfile

def generate_react_app_structure(name: str, ui_code: str) -> str:
    base_path = f"app/codegen/{name}"
    os.makedirs(base_path, exist_ok=True)

    with open(f"{base_path}/App.jsx", "w") as f:
        f.write(ui_code)

    with open(f"{base_path}/index.js", "w") as f:
        f.write("""import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(<App />, document.getElementById('root'));
""")

    with open(f"{base_path}/index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>AI App</title></head>
<body>
<div id='root'></div>
<script src='index.js'></script>
</body>
</html>
""")

    return base_path

def generate_flask_app_structure(name: str, app_py: str, html: str, requirements: str = "flask") -> str:
    base_path = f"app/codegen/{name}"
    templates_path = os.path.join(base_path, "templates")
    os.makedirs(templates_path, exist_ok=True)

    with open(f"{base_path}/app.py", "w") as f:
        f.write(app_py)

    with open(f"{templates_path}/index.html", "w") as f:
        f.write(html)

    with open(f"{base_path}/requirements.txt", "w") as f:
        f.write(requirements)

    return base_path

def zip_app_directory(app_path: str) -> str:
    zip_path = f"{app_path}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(app_path):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, app_path)
                zipf.write(filepath, arcname)
    return zip_path
