# -*- coding: UTF-8 -*-
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import sqlite3
import re
import json
from Software_wrapper import Software
from response_gen import generate_response


version_info_path = './version_info.txt'

class HTTPRequstHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
    # try:
        packet = generate_response()
        self.wfile.write(json.dumps(packet).encode('utf-8'))
        print('Response has been sent...')
    # except Exception as e:
        #print(e)



# software info database not used yet, just leave room for further work
conn = sqlite3.connect('./data/software.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Software(name TEXT, local_ver TEXT, latest_ver TEXT)')
httpd = HTTPServer(('localhost', 3333), HTTPRequstHandler)
httpd.serve_forever()