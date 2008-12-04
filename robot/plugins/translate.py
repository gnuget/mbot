#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re 
import urllib
import urllib2
import simplejson

""" Plugin for  translate some words using google api  for pepon project """

class translate:
    def __init__(self):
        pass
    def set_paragraph(self,paragraph):
        self.paragraph  =  paragraph
        
    def set_lang(self,lang_pair):
        self.lang_pair = lang_pair
        
    def main(self):
        #headers
        headers = {            
            'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3',
            'Referer' : 'http://pepon.gnuget.org'                             
        }
        
        values = {'q' : self.paragraph,'langpair':self.lang_pair} 
        params = urllib.urlencode(values);
        
        request = urllib2.Request("http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&"+params,None,headers)
        response = urllib2.urlopen(request)
        
        answer = response.read()
        answer = simplejson.loads(answer) 
        return answer['responseData']['translatedText']
        
        
if __name__ == "__main__":
    translate = translate()
    translate.set_paragraph("hello world")
    translate.main()