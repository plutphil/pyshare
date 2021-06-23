from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import os
import socket
import sys
localhostname=socket.gethostbyname(socket.gethostname())
print(localhostname)
print(socket.gethostbyaddr(localhostname))
print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))
filename=str(sys.argv[1])
port = 4443
from base64 import b64encode
import uuid
randomuuid= str(uuid.uuid4().hex)
if(len(sys.argv)==3):
    if(sys.argv[2]=="-p"):
        randomuuid="pub"
print ("https://"+localhostname+":"+str(port)+"/"+randomuuid)
os.system("openssl req -subj '/O=PyShare/C=US/CN="+localhostname.replace(".","-")+"' -new -newkey rsa:2048 -sha256 -days 365 -nodes -x509 -keyout key.pem -out cert.pem")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if(self.path==("/"+randomuuid)):
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            with open(filename, 'rb') as file:
                self.send_header('Content-Disposition', 'attachment; filename="'+ os.path.basename(filename)+'"')
                self.end_headers()
                blocksize=4096
                while True:
                    data = file.read(blocksize)
                    self.wfile.write(data)
                    if(len(data)!=blocksize):
                        break
                return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')
        
httpd = HTTPServer((localhostname, port), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="key.pem", 
        certfile='cert.pem', server_side=True)
httpd.serve_forever()