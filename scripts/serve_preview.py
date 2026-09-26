import http.server
import socketserver
import os
import sys

os.chdir(r"D:\tieu-thuyet")
PORT = 8888

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

socketserver.TCPServer.allow_reuse_address = True
try:
    with socketserver.TCPServer(("127.0.0.1", PORT), CustomHandler) as httpd:
        print(f"PREVIEW_SERVER_RUNNING on port {PORT}", flush=True)
        httpd.serve_forever()
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    sys.exit(1)
