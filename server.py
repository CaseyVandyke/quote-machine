import http.server
import socketserver
import json

PORT = 8000

# Define a request handler class that inherits from BaseHTTPRequestHandler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    # Define a list of quotes (this replaces quote.js on the backend)
    quotes = [
        {"quote": "Life is like a box of chocolates. You never know what you're gonna get.", "author": "- Forrest Gump", "color": "#0D98BA"},
        {"quote": "Be yourself; everyone else is already taken.", "author": "- Oscar Wilde", "color": "#e74d3d"},
        {"quote": "So many books, so little time.", "author": "- Frank Zappa", "color": "#2d3e51"},
        {"quote": "A room without books is like a body without a soul.", "author": "- Marcus Tullius Cicero", "color": "#f29d12"}
    ]

    def do_GET(self):
        if self.path == '/quotes':
            # Respond with JSON data when the /quotes path is requested
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.quotes).encode())
        else:
            # Serve static files (index.html, app.js) for any other request
            super().do_GET()

# Set up the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
