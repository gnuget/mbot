#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" help class for  pepon """

class help:
    def __init__(self):
        pass

    def main(self,plugin):        
        if plugin == "tinyurl":
            return "(tinyurl  <texto>) -- Regresa la tinyurl de una url dada"

        elif plugin == "md5":
            return "(md5 <texto>) -- Regresa el md5 hash de una cadena dada"
        
        elif plugin == "unmd5":
            return "(unmd5 <hash>) -- Regresa la cadena  que genera el hash recibido"

        elif plugin == "translate":
            return "Para usar translate siga la siguiente sintaxis   'translate  en-es  hello word' "

        else:
            return "Prueba usar help tinyUrl o md5 o  unmd5 o translate"
        

if __name__ == "__main__":
    help = help()
    print help.main("tinyurl")
        
    
   

        
