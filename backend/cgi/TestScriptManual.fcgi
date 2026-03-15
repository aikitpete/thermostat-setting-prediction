#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#from cgi import escape
import sys, os
from flup.server.fcgi import WSGIServer

import subprocess
import testpython
import urlparse
import cgi
import datetime
import time
import json
import MySQLdb

def app(environ, start_response):
    
    connection = MySQLdb.connect(host="localhost", # your host, usually localhost
                         user="root", # your username
                          passwd="REDACTED", # your password
                          db="azure_machine_learning") # name of the data base
    
    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cursor = connection.cursor()
                          
    start_response('200 OK', [('Content-Type', 'text/html')])
    #yield environ['REQUEST_METHOD']
    #yield environ['QUERY_STRING']
    #yield environ['SCRIPT_NAME']+environ['PATH_INFO']+environ['QUERY_STRING']

    #yield environ['QUERY_STRING']

    if len(str(environ['QUERY_STRING'])) > 0:
        
        parsed = cgi.parse_qs(environ['QUERY_STRING'])
    
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
        parsed['Morning']=[]
        parsed['Noon']=[]
        parsed['Evening']=[]
        parsed['Midnight']=[]
        parsed['AC Setting']=[]
    
        if parsed['Time'][0]=="morning":
            parsed['Morning'].append('1')
            parsed['Noon'].append('0')
            parsed['Evening'].append('0')
            parsed['Midnight'].append('0')
        elif parsed['Time'][0]=="noon":
            parsed['Morning'].append('0')
            parsed['Noon'].append('1')
            parsed['Evening'].append('0')
            parsed['Midnight'].append('0')
        elif parsed['Time'][0]=="evening":
            parsed['Morning'].append('0')
            parsed['Noon'].append('0')
            parsed['Evening'].append('1')
            parsed['Midnight'].append('0')
        elif parsed['Time'][0]=="midnight":
            parsed['Morning'].append('0')
            parsed['Noon'].append('0')
            parsed['Evening'].append('0')
            parsed['Midnight'].append('1')
    
        response = subprocess.check_output(["python", "RequestResponse.py", str(parsed["Temperature"][0]), str(parsed["Wind"][0]), str(parsed["Humidity"][0]), str(parsed["Temperature Preference"][0]), str(parsed["Morning"][0]), str(parsed["Noon"][0]), str(parsed["Evening"][0])])
        response = json.loads(response)
        
        parsed['AC Setting'].append(str(response['Results']['output1']['value']['Values'][0][7]))
        #yield response
    
        cursor.execute("""INSERT INTO online_interface VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(st, str(parsed["Temperature"][0]), str(parsed["Wind"][0]), str(parsed["Humidity"][0]), str(parsed["Temperature Preference"][0]), str(parsed["Morning"][0]), str(parsed["Noon"][0]), str(parsed["Evening"][0]), str(parsed["Midnight"][0]), str(parsed["AC Setting"][0])))
        connection.commit()
    # Use all the SQL you like
    cursor.execute("""SELECT * FROM online_interface ORDER BY Timestamp DESC""")
    
    yield json.dumps(cursor.fetchall())
    #yield "["
    #for row in cursor.fetchall() :
    #    yield "["
    #    for k in row:
    #        yield '"'+k+'"'
    #        yield ","
    #    yield "],"
    #yield "]"
    
    #yield json.dumps(parsed)
    #yield parsed['temperature'][0]
    #yield parsed['humidity'][0]
    #yield parsed['wind'][0]
    #yield parsed['time'][0]
    
    # close the cursor object
    #cursor.close()
    # close the connection
    connection.close()
    

WSGIServer(app).run()
