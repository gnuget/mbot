#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import time

from plugins.log import Log
from plugins.tinyUrl import  tinyUrl
from plugins.awbox import awbox
from plugins.mbot_md5 import mbot_md5
from plugins.unmd5 import unmd5
from plugins.translate import translate
from plugins.help import help
from PyGtalkRobot import GtalkRobot



############################################################################################################################

class mbot(GtalkRobot):
    
    #Regular Expression Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets

    def __init__(self):
        GtalkRobot.__init__(self)
        self.log = Log()


    #overwriting  the replyMessage for use log class
    def replyMessage(self,user,message):
        self.log.add(message)
        GtalkRobot.replyMessage(self,user,message)

    
    #"command_" is the command prefix, "001" is the priviledge num, "setState" is the method name.
    #This method is used to change the state and status text of the bot.
    def command_001_setState(self, user, message, args):
        #the __doc__ of the function is the Regular Expression of this command, if matched, this command method will be called. 
        #The parameter "args" is a list, which will hold the matched string in parenthesis of Regular Expression.
        '''(available|online|on|busy|dnd|away|idle|out|off|xa)( +(.*))?$(?i)'''
        show = args[0]
        status = args[1]
        jid = user.getStripped()

        # Verify if the user is the Administrator of this bot
        if jid == 'ldmiao@gmail.com':
            print("testing") 
            self.setState(show, status)
            self.replyMessage(user, "State settings changed！")

    
    #we need a real command_002

    #this method is for get a tinyUrl from some site
    def command_003_tinyurl(self,user,message,args):
        #tinyurl http://gnuget.org
        '''(^tinyurl)\s+(.*)'''
        
        if(args[1] == ""):
            self.replyMessage(user,"Necesitas darme una dirección Valida") 
        else:
            url =  args[1]

            tiny = tinyUrl()
            tiny.set_url(url)
            url = tiny.main()
            
            self.replyMessage(user,url) 

    def command_004_md5(self,user,message,args):
        #return the md5 hash form some url
        '''(^md5)\s+(.*)'''
        if(args[1] == ""):
            self.replyMessage(user,"Vamos no te voy a generar un md5 hash de una cadena vacia") 
        else:
            md = args[1]
            hash = mbot_md5()
            hash.set_string(md)
            
            hash = hash.main()
            
            self.replyMessage(user,hash)

    def command_005_unmd5(self,user,message,args):
        #retunrs the original string for some hash
        '''(^unmd5)\s+(.*)'''
        if(args[1] == ""):
            self.replyMessage(user,"Me estas pasando una cadena vacia, por ahí algo anda mal") 

        else:
            unmd = args[1]
            word = unmd5()
            word.set_hash(unmd)
            
            word = word.main()
            self.replyMessage(user,word)

    def command_006_translate(self,user,message,args):
        #translate text
        '''(^translate)\s+([a-zA-Z0-9\-]+)\s+(.*)'''
        
        
        language_pair =  args[1].split("-")
        language_pair = language_pair[0]+"|"+language_pair[1]
        
        text = args[2]
        trans = translate()
        trans.set_paragraph(text)
        trans.set_lang(language_pair)
        text = trans.main()
        self.replyMessage(user,text)

    #rado: this methid are under construction
    #this method is used for get the last feed for rss or atom entry
    #def command_007_getfeed(self,user,message,args):
    #'''(^getfeed)\s+(.*)'''
    #if(args[1] == ""):
    #        self.replyMessage(user,"El primer  feed de  la cadena vacia es....   la cadena vacia!") 
    #else:
    #     feed = args[1]
         
    #This method is used to response users.

    def command_008_help(self,user,message,args):
        #help 
        '''(^help)\s+(.*)'''
        
        ayuda =  help()
        ayuda = ayuda.main(args[1])
        
        self.replyMessage(user,ayuda)

    def command_009_awbox(self,user,message,args):
        #awbox
        '''(^awbox)\s+(.+)'''

        if(args[1] == ""):
            self.replyMessage(user,"Necesitas darme una dirección Valida") 
        else:
            url =  args[1]

            tiny = awbox()
            tiny.set_url(url)
            url = tiny.main()
            
            self.replyMessage(user,url)         

    def command_100_default(self, user, message, args):
        '''.*?(?s)(?m)'''
        #self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
        cosa = user.getStripped()
        msg = "Hola, aun soy un pequeño, no entendí lo que quieres que haga intenta con el comando help list"
        self.replyMessage(user,msg)

############################################################################################################################
if __name__ == "__main__":
    bot = mbot()
    bot.setState('available', "mbot  el Robot")
    bot.start("mail","password")
