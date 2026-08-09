"""
Local HTTP Web Server for Climate Indices Interactive App
Port: 8080
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).parent.resolve()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

def main():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/app/index.html"
        print(f"\n=======================================================")
        print(f"🚀 Climate Indices Web App running locally at:")
        print(f"👉 {url}")
        print(f"=======================================================\n")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == '__main__':
    main()
