from http.server import HTTPServer, BaseHTTPRequestHandler


class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):

        self.path = "/wp1.html"
        try:
            # Reading the file
            file_to_open = open(self.path).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(file_to_open, "utf-8"))


httpd = HTTPServer(("localhost", 8000), WebServer)
httpd.serve_forever()
