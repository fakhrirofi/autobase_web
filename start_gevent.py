from gevent.pywsgi import WSGIServer
from autobase import app

http_server = WSGIServer('127.0.0.1:8000', app)
http_server.serve_forever()
