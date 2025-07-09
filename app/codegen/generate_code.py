import os

def generate_react_app_structure(name: str, ui_code: str) -> str:
    base_path = f"app/codegen/{name}"
    os.makedirs(base_path, exist_ok=True)

    with open(f"{base_path}/App.jsx", "w") as f:
        f.write(ui_code)

    with open(f"{base_path}/index.js", "w") as f:
        f.write("import React from 'react';\nimport ReactDOM from 'react-dom';\nimport App from './App';\n\nReactDOM.render(<App />, document.getElementById('root'));")

    with open(f"{base_path}/index.html", "w") as f:
        f.write("<!DOCTYPE html><html><head><title>AI App</title></head><body><div id='root'></div><script src='index.js'></script></body></html>")

    return base_path
