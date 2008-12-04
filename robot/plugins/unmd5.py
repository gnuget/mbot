#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re 
import urllib
import urllib2

""" Plugin  for search the unmd5 from some hash using http://gdataonline.com/ for the pepon project"""

class unmd5:
    def __init__(self):
        pass
    
    def set_hash(self,hash):
        self.hash = hash

    def get_code(self):
        
        #request
        headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3'}
        
        request = urllib2.Request('http://gdataonline.com/seekhash.php',{},headers);
        response =  urllib2.urlopen(request)
        
        #data 
        answer = response.read()

        get_form_code = re.compile('\<input\stype\=\"hidden\"\sname\=\"code\"\svalue\=\"[a-zA-Z0-9]+\"\>')
        code = get_form_code.findall(answer)

        clean_string   = re.compile('<input type="hidden" name="code" value="(.*)">')

        
        code= clean_string.search(code[0])
        code = code.group(1)
        
        return  code        

    def main(self):
        #code 
        code = self.get_code()

        #request
        headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) Firefox/3.0.3'}

        #values 
        values = {'code':code,'hash':self.hash,'submit':'Submit'}
        params = urllib.urlencode(values)
        
        request = urllib2.Request('http://gdataonline.com/seekhash.php',params,headers);
        response =  urllib2.urlopen(request)
        
        #data 
        answer = response.read()

        get_string = re.compile('\<b\>[a-zA-Z0-9]+\<\/b\>')
        clean_string   = re.compile(r'<b>(.*)</b>',re.I)
        all = get_string.findall(answer)

        if(len(all) == 0):
            return "No pude encontrar la cadena perteneciente a ese hash de md5"
        all = clean_string.search(all[0])
        all = all.group(1)
        
        return all; 
        
if __name__ == "__main__":
    unmd5 = unmd5()
    unmd5.set_hash("d8578edf8458ce06fbc5bb76a58c5ca4")
    print unmd5.main()
