#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2

""" Plugin for get a nice url from http://tinyurl.com  for the pepon proyect"""

class tinyUrl:

    def __init__(self):
        pass

    def set_url(self,url):
        self.url  = url  #todo ---> validate to this is a good formed url
    
    def main(self):
        #request
        headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3'}

        #values
        values = {'url' : self.url,'submit':'Make TinyURL!'}        
        params = urllib.urlencode(values)

        request = urllib2.Request("http://tinyurl.com/create.php",params,headers);
        response  = urllib2.urlopen(request)
        
        #data 
        answer = response.read()

        get_tiny =  re.compile("http:\/\/tinyurl\.com\/[a-zA-Z0-9]+")
        all = get_tiny.findall(answer)

        return all[0]

if __name__ == "__main__":
    tiny = tinyUrl()
    tiny.set_url("http://gnuget.org")
    tiny.main()
