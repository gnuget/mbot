#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyGtalkRobot: A simple jabber/xmpp bot framework using Regular Expression Pattern as command controller
# Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>
#
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
#
# Homepage: http://code.google.com/p/pygtalkrobot/
#

import sys, traceback
import xmpp
import urllib
import re
import inspect
import time

from plugins.log import Log
from plugins.tinyUrl import  tinyUrl
from plugins.awbox import awbox
from plugins.mbot_md5 import mbot_md5
from plugins.unmd5 import unmd5
from plugins.translate import translate
from plugins.help import help



"""A simple jabber/xmpp bot framework

This is a simple jabber/xmpp bot framework using Regular Expression Pattern as command controller.
Copyright (c) 2008 Demiao Lin <ldmiao@gmail.com>

To use, subclass the "GtalkRobot" class and implement "command_NUM_" methods
(or whatever you set the command_prefix to), like sampleRobot.py.

"""

def print_info(obj):
    for (name, value) in inspect.getmembers(obj):
        print((name,value))

class GtalkRobot:

    ########################################################################################################################
    conn = None
    show = "available"
    status = "Mbot the robot!"
    commands = None
    command_prefix = 'command_' 
    GO_TO_NEXT_COMMAND = 'go_to_next'
    patterns  = {
                    'tinyurl'           : '(^tinyurl)\s+(.*)',
                    'md5'               : '(^md5)\s+(.*)',
                    'unmd5'             : '(^unmd5)\s+(.*)',
                    'translate'         : '(^translate)\s+([a-zA-Z0-9\-]+)\s+(.*)',
                    'c_translate'       : '(^translate)\s+(.*)',
                    'awbox'             : '(^awbox)\s+(.+)'
                }
    ########################################################################################################################
    
    #Pattern Tips:
    # I or IGNORECASE <=> (?i)      case insensitive matching
    # L or LOCALE <=> (?L)          make \w, \W, \b, \B dependent on the current locale
    # M or MULTILINE <=> (?m)       matches every new line and not only start/end of the whole string
    # S or DOTALL <=> (?s)          '.' matches ALL chars, including newline
    # U or UNICODE <=> (?u)         Make \w, \W, \b, and \B dependent on the Unicode character properties database.
    # X or VERBOSE <=> (?x)         Ignores whitespace outside character sets
    
    #This method is the default action for all pattern in lowest priviledge
    #def command_999_default(self, user, message, args):
    #    """.*?(?s)(?m)"""
    #    self.replyMessage(user, message)

    ########################################################################################################################
    #These following methods can be only used after bot has been successfully started

    #show : xa,away---away   dnd---busy   available--online
    def set_state(self, show, status_text):
        if show:
            show = show.lower()
        if show == "online" or show == "on" or show == "available":
            show = "available"
        elif show == "busy" or show == "dnd":
            show = "dnd"
        elif show == "away" or show == "idle" or show == "off" or show == "out" or show == "xa":
            show = "xa"
        else:
            show = "available"
        
        self.show = show

        if status_text:
            self.status = status_text
        
        if self.conn:
            pres=xmpp.Presence(priority=5, show=self.show, status=self.status)
            self.conn.send(pres)

    def getState(self):
        return self.show, self.status

    def replyMessage(self, user, message):
        self.conn.send(xmpp.Message(user, message))

    def getRoster(self):
        return self.conn.getRoster()

    def getResources(self, jid):
        roster = self.getRoster()
        if roster:
            return roster.getResources(jid)

    def getShow(self, jid):
        roster = self.getRoster()
        if roster:
            return roster.getShow(jid)

    def getStatus(self, jid):
        roster = self.getRoster()
        if roster:
            return roster.getStatus(jid)

    def authorize(self, jid):
        """ Authorise JID 'jid'. Works only if these JID requested auth previously. """
        self.getRoster().Authorize(jid)
    
    ########################################################################################################################
    #deprecated
    def initCommands(self):
        if self.commands:
            self.commands.clear()
        else:
            self.commands = list()
        
        for (function,expresion) in list(self.patterns.items()):
            for (name, value) in inspect.getmembers(self):
                if inspect.ismethod(value) and name == self.command_prefix + function:
                    self.commands.append({'expresion':expresion,'value':value,'plugin':function})


    def controller(self,conn,message):
        text = message.getBody()
        user = message.getFrom()

        if text:
            text = text.encode('utf-8','ignore') #change the encoding

            for element  in  self.commands:
                pattern = element['expresion']  #regular expresion
                function = element['value'] #function callable
                plugin =  element['plugin'] #plugin name
                match = re.match(pattern,text)
                      
                if(match):
                    args = match.groups()
                    try:
                        return_value =  function(user,text,match.groups())
                        break
                    except:
                        print_info(sys.exc_info())
                        self.replyMessage(user,traceback.format_exc())

    #Accepting All request for all users (anyone can add this bot as  a friend)
    def presenceHandler(self, conn, presence):
        if presence:
            print("-"*100)
            print(presence.getFrom(), presence.getFrom().getResource(), presence.getType(), presence.getStatus(), presence.getShow(),sep=",")
            print("~"*100)

            if presence.getType()=='subscribe':
                jid = presence.getFrom().getStripped()
                self.authorize(jid)

    def StepOn(self):
        try:
            self.conn.Process(1)
        except KeyboardInterrupt: 
            return 0
        return 1

    def GoOn(self):
        while self.StepOn(): pass

    ########################################################################################################################
    # "debug" parameter specifies the debug IDs that will go into debug output.
    # You can either specifiy an "include" or "exclude" list. The latter is done via adding "always" pseudo-ID to the list.
    # Full list: ['nodebuilder', 'dispatcher', 'gen_auth', 'SASL_auth', 'bind', 'socket', 'CONNECTproxy', 'TLS', 'roster', 'browser', 'ibb'].
    def __init__(self, server_host="talk.google.com", server_port=5223, debug=[]):
        self.debug = debug
        self.server_host = server_host
        self.server_port = server_port

        #charge all plugins
        self.initCommands()

    def start(self, gmail_account, password):
        jid=xmpp.JID(gmail_account)
        user, server, password = jid.getNode(), jid.getDomain(), password

        self.conn=xmpp.Client(server, debug=self.debug)
        #talk.google.com
        conres=self.conn.connect( server=(self.server_host, self.server_port) )
        if not conres:
            print("Unable to connect to server %s!"%server)
            sys.exit(1)
        if conres != 'tls':
            print("Warning: unable to estabilish secure connection - TLS failed!")
        
        authres=self.conn.auth(user, password)
        if not authres:
            print("Unable to authorize on %s - Plsese check your name/password."%server)
            sys.exit(1)
        if authres != "sasl":
            print("Warning: unable to perform SASL auth os %s. Old authentication method used!" % server)
        
        self.conn.RegisterHandler("message", self.controller)
        self.conn.RegisterHandler('presence',self.presenceHandler)
        
        self.conn.sendInitPresence()
        
        self.set_state(self.show, self.status)
        
        print("Bot started.")
        self.GoOn()

    ########################################################################################################################




    ############################# BOT FUNCTIONS ###########################
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
            print(jid, " ---> ",bot.getResources(jid), bot.getShow(jid), bot.getStatus(jid))
            self.setState(show, status)
            self.replyMessage(user, "State settings changed！")

    

    #this method is for get a tinyUrl from some site
    def command_tinyurl(self,user,message,args):
        
        if(args[1] == ""):
            self.replyMessage(user,"Necesitas darme una dirección Valida") 
        else:
            url =  args[1]

            tiny = tinyUrl()
            tiny.set_url(url)
            url = tiny.main()
            
            self.replyMessage(user,url) 

    def command_md5(self,user,message,args):
        #return the md5 hash form some url
        if(args[1] == ""):
            self.replyMessage(user,"Vamos no te voy a generar un md5 hash de una cadena vacia") 
        else:
            md = args[1]
            hash = mbot_md5()
            hash.set_string(md)
            
            hash = hash.main()
            
            self.replyMessage(user,hash)

    def command_unmd5(self,user,message,args):
        #retunrs the original string for some hash
        if(args[1] == ""):
            self.replyMessage(user,"Me estas pasando una cadena vacia, por ahí algo anda mal") 

        else:
            unmd = args[1]
            word = unmd5()
            word.set_hash(unmd)
            
            word = word.main()
            self.replyMessage(user,word)

    def command_translate(self,user,message,args):
        #translate text
        
        language_pair =  args[1].split("-")
        language_pair = language_pair[0]+"|"+language_pair[1]
        
        text = args[2]
        trans = translate()
        trans.set_paragraph(text)
        trans.set_lang(language_pair)
        text = trans.main()
        self.replyMessage(user,text)

    def command_c_translate(self,user,message,args):
        args2 = (args[0],'en-es',args[1])
        self.command_translate(user,message,args2)

    #rado: this methid are under construction
    #this method is used for get the last feed for rss or atom entry
    #def command_007_getfeed(self,user,message,args):
    #'''(^getfeed)\s+(.*)'''
    #if(args[1] == ""):
    #        self.replyMessage(user,"El primer  feed de  la cadena vacia es....   la cadena vacia!") 
    #else:
    #     feed = args[1]
         
    #This method is used to response users.

    def command_help(self,user,message,args):
        #help 
        '''(^help)\s+(.*)'''
        
        ayuda =  help()
        ayuda = ayuda.main(args[1])
        
        self.replyMessage(user,ayuda)

    def command_awbox(self,user,message,args):
        #awbox

        if(args[1] == ""):
            self.replyMessage(user,"Necesitas darme una dirección Valida") 
        else:
            url =  args[1]

            tiny = awbox()
            tiny.set_url(url)
            url = tiny.main()
            
            self.replyMessage(user,url)         

    def command_default(self, user, message, args):
        #self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))
        cosa = user.getStripped()
        msg = "Hola, aun soy un pequeño, no entendí lo que quieres que haga intenta con el comando help list"
        self.replyMessage(user,msg)

############################################################################################################################
if __name__ == "__main__":
    bot = GtalkRobot()
    bot.set_state('available', "PyGtalkRobot")
    
    bot.start('mail','password')
