# from http.server import HTTPServer, BaseHTTPRequestHandler

# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(b"<h1>Hello, World!</h1>")
#         self.wfile.write(b'<img src=".stock_F.png">')
#         self.wfile.write(b'<img src=".stock_INTC.png">')

# def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     print(f"Starting httpd server on port {port}")
#     httpd.serve_forever()

# if __name__ == '__main__':
#     run()

# import http.server
# import socketserver

# PORT = 8080
# DIRECTORY = "."  # Serve files from the current directory

# class Handler(http.server.SimpleHTTPRequestHandler):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, directory=DIRECTORY, **kwargs)

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print(f"Serving at port {PORT}")
#     print(f"Open your browser to http://localhost:{PORT}/.stock_F.png")
#     httpd.serve_forever()

import http.server
import socketserver

PORT = 8002

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
