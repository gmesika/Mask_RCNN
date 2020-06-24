
def alive(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes("Yes", "utf-8"))


def bad_request(self, error):
    self.send_response(400)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes(error, "utf-8"))


def custom_response(self, error, id):
    self.send_response(id)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(bytes(error, "utf-8"))