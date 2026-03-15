#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#import sys

#def passVars():
#    variable = "<h1>bla</h1>"
#    return variable

#def main(args):
#    for arg in args:
#        print(arg)

#if __name__ == '__main__':
#    main(sys.argv)
import urlparse
import cgi

par = urlparse.parse_qs(urlparse.urlparse("http://www.test.com/?humidity=30").query)
print par['humidity']

parsed = cgi.parse_qs("temperature=20&humidity=50&wind=30&time=morning")
print parsed['temperature']
print parsed['humidity']
print parsed['wind']
print parsed['time']

print "<h1>Hello world Python!</h1>";
