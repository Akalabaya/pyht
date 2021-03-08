#This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
from http.server import HTTPServer , BaseHTTPRequestHandler
import os
import sys
import base64
import cgi
from urllib.parse import urlparse
import mimetypes
import datetime
import time
def getpost():
   import base64
   base64_string = sys.argv[1]
   base64_bytes = base64_string.encode("ascii") 
   dir = {}
   sample_string_bytes = base64.b64decode(base64_bytes) 
   sample_string = sample_string_bytes.decode("ascii") 
   a = sample_string.split("&")
   for x in a:
       dir[x.split("=")[0].replace("+"," ")] = x.split("=")[1].replace("+"," ")
   return dir
def getGET():
   import base64
   base64_string = sys.argv[2]
   base64_bytes = base64_string.encode("ascii") 
   dir = {}
   sample_string_bytes = base64.b64decode(base64_bytes) 
   sample_string = sample_string_bytes.decode("ascii") 
   a = sample_string.split("&")
   for x in a:
       dir[x.split("=")[0].replace("+"," ")] = x.split("=")[1].replace("+"," ")
   return dir
def getuploadedfile(fileobj):
        file_tmp = fileobj
        filename = fileobj[5:].replace(file_tmp.split("_").pop(),"")[:-1]
        mime = mimetypes.guess_type(filename)[0]
        arr = {
                "file_tmp" : file_tmp,
                "file_name" : filename,
                "file_mimetype":mime
        }
        return arr
def save_uploaded_file(file_temp_path , destination):
        try:
                data = open(file_temp_path,"rb").read()
                open(destination,"wb").write(data)
                #os.remove(file_temp_path)
        except Exception as ex:
                pass
        try:
            os.remove(file_temp_path)
        except:
            pass
        return True
class server:
        request_url = ""
        request_link = ""
        request_sp = []
        request_html = []
        media = "0"
        def linkpage(self,url,htmluri):
                server.request_sp.append(url)
                server.request_html.append(htmluri)
        frm = cgi.FieldStorage()


class serve(BaseHTTPRequestHandler):
 def do_POST(self):
         if not os.path.exists(server.request_link + self.path[1:]):
                 file_to_open = "No file found"
                 self.send_response(404)
                
         if self.path[1:].split("/")[len(self.path[1:].split("/")) - 1][0] == "_":
                 self.send_response(403)
                 file_to_open = "error"
         else:
                 try:
                    if self.path[1:].split(".")[len( self.path[1:].split(".") ) - 1] == "html" or mimetypes.guess_type(self.path[1:].split("?")[0])[0] == "text/html":
                           ctype, pdict = cgi.parse_header(
                           self.headers.get('content-type'))
                           if ctype == 'multipart/form-data':
                    
                                   length = int(self.headers['content-length'])
                                   #print(length)
                                   if length > 200000000:
                                      read = 0
                                      while read < length:
                                              read += len(self.rfile.read(min(66556, length - read)))
                                              print("POST REQUEST IS TOO BIG TO HANDLE")
                                              return
                                   else:
                                       self.send_response(200)
                                       form = cgi.FieldStorage(
                                       fp=self.rfile,
                                       headers=self.headers,
                                       environ={'REQUEST_METHOD':'POST',
                                                       'CONTENT_TYPE':self.headers['Content-Type'],
                                                       })
                               
                                       params = ""
                                       for key in form.keys():
                                           if form[key].filename == None:
                                                  if params == "":
                                                          params += str(key) + "=" + form[key].value + "&" 
                                                  else:
                                                          params += str(key) + "=" + form[key].value + "&" 
                                           else:
                                                   fn = 'tmp/' +"_" + os.path.basename(form[key].filename) + "_" + str(int(round(time.time() * 1000)))
                                                   open(fn, 'wb').write(form[key].file.read())  
                                                   if params == "":
                                                           params += str(key) + "="+ fn + "&"    
                                                   else:
                                                           params += str(key) + "="+ fn + "&"   
                                           string = params[:-1]
                                           #print(string)  
                                           #os.remove("test.txt")
                                           sample_string_bytes = string.encode("ascii") 
                                           base64_bytes = base64.b64encode(sample_string_bytes) 
                                           base64_string = base64_bytes.decode("ascii") 
                                           os.system("python exec.py " + server.request_link + "" + self.path[1:] +" >temp.py")
                                           os.system("python temp.py "+base64_string+" > temp.html")
                                           file_to_open = open("temp.html").read()
                                           os.remove("temp.py")
                                           os.remove("temp.html")
                               
                           else:   
                                   length = int(self.headers.get('content-length', 0))
                                   body = self.rfile.read(length)
                                   self.send_response(200)
                                   self.end_headers()
                                   string = str(body)[2:len(str(body)) - 1]
                                   #os.remove("test.txt")
                                   sample_string_bytes = string.encode("ascii") 
                                   base64_bytes = base64.b64encode(sample_string_bytes) 
                                   base64_string = base64_bytes.decode("ascii") 
                                   os.system("python exec.py " + server.request_link + "" + self.path[1:] +" >temp.py")
                                   os.system("python temp.py "+base64_string+" > temp.html")
                                   file_to_open = open("temp.html").read()
                                   os.remove("temp.py")
                                   os.remove("temp.html")
                    else:                   
                                   if "?" in self.path[1:]:
                                      fred = open(server.request_link+self.path[1:].split("?")[0]).read()
                                      file_to_open = fred
                                      self.send_response(200) 
                                   else:      
                                      # For MIME types
                                      mime = mimetypes.guess_type(server.linkpage+self.path[1:])
                                      self.send_header("Content-Type",mime)
                                      fred = open(server.request_link+self.path[1:]).read()
                                      file_to_open = fred
                                      self.send_response(200)   
                            
                 except Exception as e:
                        file_to_open = str(e)
                        print(e)
         self.end_headers()
         self.wfile.write(bytes(file_to_open,'utf-8'))


#POST REQUEST ENDS HERE
#----------------------------------------------------------------------------------------------------------------------
#GET REQUEST STARTS HERE

 def do_GET(self): 
         server.request_url = self.path   
         if not os.path.exists(server.request_link + self.path[1:]):
                 file_to_open = "No file found"
                 self.send_response(404)
                             
         if self.path[1:].split("/")[len(self.path[1:].split("/")) - 1][0] == "_" :
                 self.send_response(403)
                 file_to_open = "<h1 style='font-family:sans-serif;'>Access Forbidden</h1>"
         else:
                 try:  
                        
                        if self.path[1:].split(".")[len( self.path[1:].split(".") ) - 1] == "html" or mimetypes.guess_type(self.path[1:].split("?")[0])[0] == "text/html": 
                               server.media = "0"
                               if "?" in self.path[1:]:
                                       try:
                                     
                                              o = urlparse(self.path[1:]).query
                                              #print(o)
                                              self.send_response(200)
                                              sample_string_bytes = o.encode("ascii") 
                                              base64_bytes = base64.b64encode(sample_string_bytes) 
                                              base64_string = base64_bytes.decode("ascii") 
                                              os.system("python exec.py " + server.request_link + "" + self.path[1:].split("?")[0] +" >temp.py")
                                              os.system("python temp.py "+" None "+base64_string+" > temp.html")
                                              file_to_open = open("temp.html").read() 
                                       except:
                                              print("error")
                               else:                     
                                       os.system("python exec.py " + server.request_link + "" + self.path[1:] + " >temp.py")
                                       os.system("python temp.py > temp.html")
                                       file_to_open = open("temp.html").read()
                                       self.send_response(200)
                                       os.remove("temp.py")
                                       os.remove("temp.html")
                        else:    
                                server.media = "1"
                                try:

                                   if "?" in self.path[1:]:
                                           mime = mimetypes.guess_type(self.path[1:].split("?")[0])
                                           file_to_open = open(self.path[1:].split("?")[0] ,"rb" ).read()
                                           self.send_response(200)
                                           self.send_header('Content-type',mime[0]) 
                                   else:   
                                           mime = mimetypes.guess_type(self.path[1:]) 
                                           file_to_open = open(self.path[1:], 'rb').read()
                                           self.send_response(200)
                                           self.send_header('Content-type',mime[0])   
                                except:
                                        file_to_open = "Error in processing .. the file might not exist !!"
                                        self.send_response(404)                                    

                 except Exception as e:
                         file_to_open = str(e)
                         print(e)
         self.end_headers()
         if server.media == "1":
                 self.wfile.write(bytes(file_to_open)) 
         else:
                 self.wfile.write(bytes(file_to_open,'utf-8'))         



#function for running the server at the given port

def run():
    ip = 'localhost'
    port = 80
    print('Akap Pyweb 2020 Server serving on http://{}:{}'.format(ip,port))
    httpd = HTTPServer((ip,port),serve)
    httpd.serve_forever()
