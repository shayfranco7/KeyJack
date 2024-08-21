#!/usr/bin/env python3

"""Simple HTTP Server With Upload."""

__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = "http://li2z.cn/"

directory = ''
import os
import posixpath
import http.server
import urllib.request, urllib.parse, urllib.error
import html
import shutil
import mimetypes
import re
from io import BytesIO
import json
import datetime


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Simple HTTP request handler with GET/HEAD/POST commands.

    This serves files from the current directory and any of its
    subdirectories. The MIME type for files is determined by
    calling the .guess_type() method. And can receive files uploaded
    by the client.
    """
    server_version = "SimpleHTTPWithUpload/" + __version__

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        content_type = self.headers.get('content-type', '')
        content_length = int(self.headers.get('content-length', 0))
        post_data = self.rfile.read(content_length)

        # Generate a unique filename based on the current timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

        try:
            if "multipart/form-data" in content_type:
                self.save_uploaded_file(post_data, content_type, timestamp)
            elif "application/json" in content_type:
                self.save_json_data(post_data, timestamp)
            else:
                self.save_received_data(post_data, timestamp)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "status": "success",
                "message": "Data received and saved successfully"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            error_response = {
                "status": "error",
                "message": str(e)
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def save_uploaded_file(self, data, content_type, timestamp):
        """Save uploaded file."""
        boundary = content_type.split("boundary=")[1].encode()
        parts = data.split(b'--' + boundary)

        for part in parts:
            if b'Content-Disposition:' in part:
                # Extract filename
                disposition_line = re.findall(b'Content-Disposition: .*?filename="(.*?)"', part)
                if disposition_line:
                    filename = f"uploads_files/{timestamp}_{disposition_line[0].decode()}"
                    file_path = os.path.join(self.translate_path(self.path), filename)

                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    # Find the start of the file content and split
                    try:
                        # Locate the start of the file content
                        content_start = part.index(b'\r\n\r\n') + 4
                        file_data = part[content_start:].split(b'\r\n--' + boundary)[0]

                        # Save the file
                        with open(file_path, 'wb') as file:
                            file.write(file_data)

                        print(f"File '{disposition_line[0].decode()}' uploaded successfully to '{file_path}'")
                    except Exception as e:
                        print(f"Error saving file: {e}")
    def save_json_data(self, data, timestamp):
        """Save JSON data."""
        filename = f"uploads_files/{timestamp}_data.json"
        with open(filename, 'w') as file:
            file.write(data.decode('utf-8'))

    def save_received_data(self, data, timestamp):
        """Save other types of data."""
        filename = f"uploads_files/{timestamp}_data.bin"
        with open(filename, 'wb') as file:
            file.write(data)

    def send_head(self):
        """Common code for GET and HEAD commands."""
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html)."""
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = BytesIO()
        displaypath = html.escape(urllib.parse.unquote(self.path))
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(("<html>\n<title>Directory listing for %s</title>\n" % displaypath).encode())
        f.write(("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath).encode())
        f.write(b"<hr>\n")
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write(b"<input name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write(b"<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
            f.write(('<li><a href="%s">%s</a>\n'
                     % (urllib.parse.quote(linkname), html.escape(displayname))).encode())
        f.write(b"</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax."""
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = [_f for _f in words if _f]
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects."""
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file."""
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


def test(HandlerClass=SimpleHTTPRequestHandler,
         ServerClass=http.server.HTTPServer):
    http.server.test(HandlerClass, ServerClass)


def run(dirpath):
    global directory
    directory = dirpath
    test()
