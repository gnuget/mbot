#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime

""" Logging class for pepon proyect"""

class Log:

    def __init__(self):
        self.file = "tmp/logs/log.log"

    def set_file(self):
        pass

    def add(self,message):
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        file = open(self.file,'a')
        file.write(now.__str__() +" - "+ message+'\n')
        file.close()

        return True

if __name__ == "__main__":
    log = Log()
    log.add("Este es un mensaje de logging")
