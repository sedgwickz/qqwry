from http.server import BaseHTTPRequestHandler
import json
from os.path import join
from qqwry import QQwry
from urllib.parse import urlparse
import ipaddress
import socket


def isIP(ip):
    try:
        ip = ipaddress.ip_address(ip)
        return True
    except:
        return False

# reference
# python3 https://github.com/animalize/qqwry-python3
# nodejs https://github.com/cnwhy/lib-qqwry
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        try:
            search_ip = self.client_address[0]
            query = urlparse(self.path).query.split('=')[-1]
            if query:
                search_ip = query

            q = QQwry()
            q.load_file(join("data", "qqwry.dat"), loadindex=True)
            if not isIP(search_ip):
                search_ip = socket.gethostbyname(search_ip)
            info = q.lookup(search_ip)
            self.wfile.write(json.dumps({'search_ip': search_ip, 'addr': info[0], 'detail': info[1]}).encode())
        except Exception as err:
            self.wfile.write(json.dumps({"msg": str(err)}).encode())
