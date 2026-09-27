"""Static server with gzip, to measure like GitHub Pages does."""
import gzip, sys, os, http.server, functools

class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            path = os.path.join(path, 'index.html')
        if not os.path.isfile(path) or 'gzip' not in self.headers.get('Accept-Encoding', ''):
            return super().send_head()
        ctype = self.guess_type(path)
        data = open(path, 'rb').read()
        if ctype.startswith(('text/', 'application/javascript', 'image/svg', 'application/json')) or path.endswith(('.css', '.js', '.html')):
            data = gzip.compress(data, 6)
            self.send_response(200)
            self.send_header('Content-Encoding', 'gzip')
        else:
            self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        import io
        return io.BytesIO(data)

port, root = int(sys.argv[1]), sys.argv[2]
http.server.ThreadingHTTPServer(('', port), functools.partial(H, directory=root)).serve_forever()
