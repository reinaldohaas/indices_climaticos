"""
Local HTTP Web Server for Climate Indices Interactive App
Auto-detects available ports (8080, 8085, 8000, 8088, 8500)
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORTS_TO_TRY = [8080, 8085, 8000, 8088, 8500]
ROOT_DIR = Path(__file__).parent.resolve()

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def do_GET(self):
        # Redirect root / or /index.html directly to /app/index.html
        if self.path in ['/', '/index.html']:
            self.path = '/app/index.html'
        return super().do_GET()

def main():
    os.chdir(ROOT_DIR)
    socketserver.TCPServer.allow_reuse_address = True

    httpd = None
    selected_port = None

    for port in PORTS_TO_TRY:
        try:
            httpd = socketserver.TCPServer(("", port), CustomHandler)
            selected_port = port
            break
        except Exception:
            continue

    if not httpd:
        print("ERRO: Nenhuma porta disponível entre (8080, 8085, 8000, 8088, 8500).")
        sys.exit(1)

    url = f"http://localhost:{selected_port}/app/index.html"
    print(f"\n=======================================================")
    print(f"🚀 Servidor do Explorador de Índices Climáticos Rodando!")
    print(f"👉 Acesse no navegador: {url}")
    print(f"=======================================================\n")
    
    webbrowser.open(url)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor finalizado pelo usuário.")

if __name__ == '__main__':
    main()
