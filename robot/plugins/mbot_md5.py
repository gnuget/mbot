#!/usr/bin/env python
# -*- coding: utf-8 -*-

import md5

""" Plugin for get a nice url from http://tinyurl.com  for the pepon proyect"""

class mbot_md5:    

    def __init__(self):
        pass

    def set_string(self,string):
        self.string  =  string
        

    def main(self):
        hash =  md5.md5(self.string).hexdigest()        
        return hash        

if __name__ == "__main__":
    md = mbot_md5()
    md.set_string("qwerty")
    print md.main()
