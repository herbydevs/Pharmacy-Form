import http.server
import socketserver
import os

# Define the directory to serve
DIRECTORY = "./dist"
PORT = 80

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Check if the requested file exists
        file_path = os.path.join(DIRECTORY, self.path.lstrip("/"))
        if not os.path.exists(file_path) or os.path.isdir(file_path):
            # Redirect all unknown routes to index.html
            self.path = "/index.html"
        return super().do_GET()

# Create the server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving {DIRECTORY} on port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")