#!flask/bin/python
import json
from flask import Flask
from flask import request
import xmlrpclib
srv = 'http://localhost:8069'
common = xmlrpclib.ServerProxy('%s/xmlrpc/2/common' % srv)
db = 'Test_Realtime'
user, pwd= 'admin', 'admin'
uid = common.authenticate(db, user, pwd, {})
api = xmlrpclib.ServerProxy('%s/xmlrpc/2/object' % srv)

app = Flask(__name__)
@app.route('/sippeers/single', methods=['GET', 'POST'])

def index():
    print request

    print request.args

    print request.form

    print 'name:%s' % request.form.getlist('name')

    print 'Values:%s' % request.values
    
    search = api.execute_kw(db, uid, pwd, 'sip.users', 'search_read', ([('defaultuser', 'in', request.form.getlist('name')) ], ['context', 'defaultuser', 'secret']))
   
    print search
   
    if len(search)==1:
        ret = "type=friend&context=%s&host=dynamic&defaultuser=%s&secret=%s" % (search[0].get('context'),search[0].get('defaultuser'), search[0].get('secret'))
        return ret
    else:
        return '' 

@app.route('/voicemail/single', methods=['GET', 'POST'])
@app.route('/voicemail/multi', methods=['GET', 'POST'])

def index1():
    search = api.execute_kw(db, uid, pwd, 'voice.mail', 'search_read', ([('context', 'in', request.form.getlist('context')) ], ['context', 'voicemailextension', 'pin', 'fullname', 'email', 'attachment', 'maximummessages']))
    print 'search %s' % search
    print 'voicemail%s' % request.form
    if True==True:
        ret = "context=%s&mailbox=%s&password=%s&fullname=%s&email=%s&attach=%s&maxmsg=%s" % (search[0].get('context'),search[0].get('voicemailextension'),search[0].get('pin'),search[0].get('fullname'), search[0].get('email'),search[0].get('attachment'),search[0].get('maximummessages'))
        return ret
    else:
        return ''

        
@app.route('/extensions/single', methods=['GET', 'POST'])
@app.route('/extensions/multi', methods=['GET', 'POST'])

def index2():   
    print request

    print request.args

    print request.form

    print 'name:%s' % request.form.getlist('name')

    print 'Values:%s' % request.values
    
    
    
    search = api.execute_kw(db, uid, pwd, 'dialplan.inbound', 'search_read', ([('did', 'in', request.form.getlist('exten')) ], ['context', 'did', 'destination']))
    search1 = api.execute_kw(db, uid, pwd, 'dialplan.inbound', 'search_read', ([('priority', 'in', request.form.getlist('priority')) ], ['priority']))
    search2 = api.execute_kw(db, uid, pwd, 'call.groups', 'search_read', ([('callgroupextension', 'in', request.form.getlist('exten')) ], ['callgroupextension', 'context', 'ringtime']))
    search3 = api.execute_kw(db, uid, pwd, 'voice.mail', 'search_read', ([('context', 'in', request.form.getlist('context')) ], ['context', 'voicemailextension', 'messages']))
    
    print 'search:%s' % search
    print 'search2:%s' % search2
    print 'search3%s' % search3
    
    print (request.form.getlist('priority')) 
    if len(search)==1 and request.form.getlist('priority')[0]=='1':
        print 'inbound route' 
        ret="""context=%s&exten=%s&priority=%s&app=Dial&appdata=%s""" % (search[0].get('context'),search[0].get('did'),search1[0].get('priority'),search[0].get('destination')[1])
        return ret 
    elif request.form.getlist('priority')[0]=='2':
        print 'voicemail'
        ret= "context=%s&exten=%s&priority=2&app=VoiceMail&appdata=%s@%s,u" % (search3[0].get('context'),search[0].get('did'),search3[0].get('voicemailextension'),search3[0].get('context'))
        print '123'
        print ret
        return ret 

    elif len(search2)==1:
        print 'call group'
        sips= api.execute_kw(db, uid, pwd, 'call.groups', 'get_sips',([search2[0].get('id')]))
        print 'sips:%s' % sips
        ret="""context=%s&exten=%s&priority=%s&app=Dial&appdata=%s,%s""" % (search2[0].get('context'),search2[0].get('callgroupextension'),search1[0].get('priority'),sips,search2[0].get('ringtime'))
        return ret
        
    elif len(search3)==1:
        print 'voicemailmain'
        ret="context=%s&exten=%s&priority=2&app=VoiceMailMain&appdata=%s@%s,u" % (search3[0].get('context'),search3[0].get('messages'),search3[0].get('voicemailextension'),search3[0].get('context'))
        return ret
    else:
        return ''        

        
if __name__ == '__main__':

    app.run(debug=True, host='192.168.1.1', port=5000)
