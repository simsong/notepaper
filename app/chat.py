import bottle
import mysql_vars
from mysql_vars import *
import sys
import json

import ctools.dbfile as dbfile

"""
Chat API:

Status messages:

post(channel,message) - store a message in the chats table with:
  t=now(), ipaddr=source, channel=channel, message=message

poll(channels,t) - returns all messages sent on the specified channels since
t. Channels is a comma-separated list of channels. 

If channels is not present, ignores t and returns the last
message for each channel. 

If t is 0, '' or not present, returns the last message on each
channel.

  [ {channel:channel, t:t, message:message}, ...]
"""

auth=dbfile.DBMySQLAuth(user=mysql_user,password=mysql_password,host=mysql_host,database=mysql_database)

@bottle.route('/chat/')
def chat():
    return bottle.static_file('chat.html', root='static')

@bottle.route('/chat/chat.js')
def chat():
    return bottle.static_file('chat.js', root='static')

@bottle.route('/chat/post', method=['GET','POST'])
def chat_post():
    client_ip = bottle.request.environ.get('REMOTE_ADDR')
    id = dbfile.DBMySQL.csfr(auth,"insert into chats (t,ipaddr,channel,message) values (now(),%s,%s,%s)",
                                 (client_ip, bottle.request.params.channel, bottle.request.params.message), asDicts=True)
    row = dbfile.DBMySQL.csfr(auth,"select t from chats where id=%s",(id,))
    return json.dumps({'t':row[0][0]}, default=str)

@bottle.route('/chat/poll', method=['GET','POST'])
def chat_poll():
    channels = bottle.request.params.channels
    t        = bottle.request.params.t
    if channels is None:
        cmd = "SELECT channel,max(t) FROM chats GROUP BY channel"
        vals = ()
    elif (str(t)=="0") or t is None:
        vals = channels.split(",")
        args = ",".join( ["%s"] * len(vals) )
        cmd = "select a.channel,a.t,b.message from (select channel,max(t) as t from chats group by channel) a left join chats b on a.channel=b.channel and a.t=b.t where a.channel in (" + args + ")"
    else:
        vals = [t] + channels.split(",")
        args = ",".join( ["%s"] * len(vals) )
        cmd = "select * from chats where t>%s and channel in (" + args +")"
        
    res = dbfile.DBMySQL.csfr(auth,cmd,vals, asDicts=True)
    return json.dumps(res,default=str)

