#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from cgi import escape
import sys, os
from flup.server.fcgi import WSGIServer

import subprocess
import testpython

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    yield '<h1>FastCGI Environment</h1>'
    yield subprocess.check_output(["python", "testpython.py"])
    #yield testpython.passVars()

#, "arg1 arg2 arg3 arg4".split(' '))


#yield execfile("testpython.py 1")
#if __name__ == '__main__':
#    from wsgiref.simple_server import make_server
#    srv = make_server('localhost', 8080, app)
#    srv.serve_forever()
WSGIServer(app).run()
