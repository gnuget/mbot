#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2

""" Plugin for  get a nice url from  awbox"""

class awbox:
    def __init__(self):
        pass

    def set_url(self,url):
        self.url = url

    def main(self):
        #headers 
        headers  = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3'}
        
        values = {'url' : self.url}
        params = urllib.urlencode(values)
        
        request = urllib2.Request("http://awbox.com/new?"+params,{},headers);
        response = urllib2.urlopen(request)

        answer = response.read()

        return answer

if __name__ == "__main__":
    mini = awbox()
    mini.set_url("http://gnuget.org")
    print mini.main()
        


