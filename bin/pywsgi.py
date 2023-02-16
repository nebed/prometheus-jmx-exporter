#!/usr/bin/env python

from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
import os
from app import app

http_server = WSGIServer(('0.0.0.0', os.environ.get('PORT', 9000)), app)
http_server.serve_forever()