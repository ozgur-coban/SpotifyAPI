from http.server import HTTPServer , BaseHTTPRequestHandler 
import subprocess


class Serv(BaseHTTPRequestHandler):
    
    def do_GET(self):

            
        try:

            subprocess.Popen(["powershell.exe","C:\\Users\\'location'\\skipsongkeystroke.ps1"])
            self.send_response(200) #successful
            self.handle
            
            
        except:
            
            self.send_response(404)
        self.end_headers()
        
        
httpd=HTTPServer(('0.0.0.0',8080),Serv)
httpd.serve_forever()