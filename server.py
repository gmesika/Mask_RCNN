import base64

import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import actions
import utilities
#from exception import gsi_exception


class MyServer(BaseHTTPRequestHandler):
    SERVER_logger = utilities.set_logger("Logger", verbose=False)

    # apu_lock = threading.Lock()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        self.SERVER_logger.info(str(self.client_address) + ' ' + str(self.requestline) + " active threads:" +
                                str(threading.active_count()))

        if self.path == '/images':
            try:
                self.SERVER_logger.info('get images request started.')
                from os import listdir
                from os.path import isfile, join
                onlyfiles = [f for f in listdir(os.path.abspath("images/")) if isfile(join(os.path.abspath("images/"), f))]
                send_response(self, 200, {"result": onlyfiles})
                self.SERVER_logger.info('get images request completed.')
            except Exception as e:
                self.SERVER_logger.error('error when handling HTTP request', exc_info=True)
                actions.custom_response(self, str(e), 999)

    def do_POST(self):
        self.SERVER_logger.info(str(self.client_address) + ' ' + str(self.requestline) + " active threads:" +
                                str(threading.active_count()))

        if self.path == '/detect':
            try:
                self.SERVER_logger.info('new detect request started.')

                try:
                    detect_request_json = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                    image_file_path = detect_request_json['image_file_path']
                    show_mask = str2bool(detect_request_json['show_mask'])
                    show_bbox = str2bool(detect_request_json['show_bbox'])
                    show_label = str2bool(detect_request_json['show_label'])
                    show_polygon = str2bool(detect_request_json['show_polygon'])
                    save_detected_fig = str2bool(detect_request_json['save_detected_fig'])
                except Exception as exe:
                    send_response(self, 400, {"error": "{0}".format(exe)})
                    return

                import client
                im = client.load_n_detect_image(image_file_path, show_mask, show_bbox,
                                                show_label, show_polygon, save_detected_fig)

                send_response_image(self, 200, im)
                self.SERVER_logger.info('new detect request completed.')
            except Exception as e:
                self.SERVER_logger.error('error when handling HTTP request', exc_info=True)
                actions.custom_response(self, str(e), 999)
                return

            return

        if self.path == '/alive':
            try:
                actions.alive(self)
            except Exception as e:
                self.SERVER_logger.error('error when handling HTTP request', exc_info=True)
                actions.custom_response(self, str(e), 999)

        actions.bad_request(self, "bad request")

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def send_response(self, status, message):
    self.send_response(status)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Content-type', 'image/PNG')
    self.end_headers()
    message = json.dumps(message)
    self.wfile.write(bytes(message, 'UTF-8'))


def send_response_image(self, status, message):
    self.send_response(status)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Content-type', 'image/PNG')
    self.end_headers()
    self.wfile.write(message)

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    print('Running Threaded server.....')
    print(sys.path)
    print(os.environ)


def run_webServer():
    hostName = str(os.getenv("SERVER_NAME", "0.0.0.0"))
    serverPort = int(os.getenv("SERVER_PORT", "7755"))

    webServer = ThreadingSimpleServer((hostName, serverPort), MyServer)
    # webServer.socket = ssl.wrap_socket(webServer.socket, keyfile='./privkey.pem',certfile='./certificate.pem', server_side=True)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    print("starting server....")
    run_webServer()