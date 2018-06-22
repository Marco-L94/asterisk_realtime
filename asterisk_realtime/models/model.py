# -*- coding: utf-8 -*-
from odoo import models, fields

class SIP_Users(models.Model):
    _name = 'sip.users'
    _rec_name= 'extension'
    extension = fields.Char('Extension', default='SIP/', help="The 'Extension' field defines the number that will be connected to the SIP user and should start with 'SIP/'.", required=True)
    context = fields.Char('Context', help="The 'Context' field defines the context used in the /etc/asterisk/extensions.conf file on the Asterisk server.", required=True)
    defaultuser = fields.Char('Defaultuser',help="The 'Defaultuser' field is the same as the username used on a SIP device.", required=True) 
    secret = fields.Char('Secret', help="The 'Secret' field is the same as the password used on a SIP device.", required=True)
  #  callerid = fields.Char('Caller ID', required=False)
    #priority = fields.Char('Priority', required=False)
    description = fields.Char('Description', help="The 'Description' field is optional and is used to add a description to the SIP user.", required=False)
    
class SIP_Trunks(models.Model):
    _name = 'sip.trunks'
    _rec_name= 'trunkname'
    trunkname = fields.Char('Trunk name', required=False)
    proxy = fields.Char('Outbound proxy', required=True)
    host = fields.Char('Host', required=True)
    username = fields.Char('Defaultuser', required=True)
    secret = fields.Char('Secret', required=True)
    description = fields.Char('Description', required=False)
    
    
class Dialplan_inbound(models.Model):
    _name = 'dialplan.inbound'
    _description = 'Dialplan inbound'
    _rec_name = 'did'
    description = fields.Char('Description', help="The 'Description' field is optional and is used to add a description to the inbound route.", required=False)
    context = fields.Char('Context', help="The 'Context' field should match the context defined in SIP users.", required=True)
    did = fields.Char('DID number',help="The 'DID number' field defines the number which needs to be dialed to reach the SIP device.", required=True)
    priority = fields.Char('Priority', default='1', help="The 'Priority field has a default value of '1' and should not be changed, as changing this value can cause problems.", required=True)
    destination = fields.Many2one('sip.users', string='Destination to extension', help="The 'Destination to extension' field defines which extension should ring when the DID number is dialed. This destination may differ from the DID to act as an internal call forward.",)
   # destination1 = fields.Many2one(comodel_name='sip.trunks', string='Destination to trunk')
#    destination2 = fields.Many2one(comodel_name='call.groups', string='Destination to group')
 #   destination3 = fields.Many2one(comodel_name='voice.mail', string='Destination to voicemail')
  #  destination4 = fields.Many2one(comodel_name='call.forward', string='Destination to call forward')

class Dialplan_outbound(models.Model):
    _name = 'dialplan.outbound'
    _description = 'Dialplan outbound'
    _rec_name = 'did'
    description = fields.Char('Description', required=False)
    context = fields.Char('Context', required=True)
    did = fields.Char('DID Number', required=True)
    dialpatterns = fields.Many2many(comodel_name='dial.patterns', string='Dial patterns', required=True) 
    destination =  fields.Many2one(comodel_name='sip.trunks', string='Select a SIP trunk', required=True)
    
class Dial_patterns(models.Model):
    _name = 'dial.patterns'
    _description = 'Dial patterns'
    _rec_name = 'dialpatterns'
    dialpatterns= fields.Char('Dial pattern', required=True)
    
class Call_groups(models.Model):
    _name = 'call.groups'
    _rec_name = 'callgroupextension'
    _description = 'Call groups'
    callgroupextension = fields.Char('Call group extension',help="The 'call group extension' field defines the number which needs be dialed for the call group.", required=True)
    context = fields.Char('Context', help="The 'Context' field should match the context defined in SIP users.", required=True)
    grouptype = fields.Selection(size=50, string='Call group type', help="""This function serves no purpose yet! 
The 'call group type' field defines the order the extensions of the call group will ring. 

'Ringall' will call every available extension at once. 
'Hunt' will take turns ringing each available extension one at a time. 
'Memoryhunt' will ring the first extension in the list. After that, it will ring the 1st and 2nd together, and so on. 
'First available' will only ring the first available extension. 
'First not on phone' will only ring the first extension that is not off-hook, ignoring call waiting. 
'Random' will call a random extension in the call group list.        """, required=False, default='ringall', selection=[('ringall', 'Ringall'), ('hunt', 'Hunt'), ('memoryhunt', 'Memoryhunt'), 
('first available', 'First available'), ('first not on phone', 'First not on phone'), ('random', 'Random')])
                            
    ringtime = fields.Char('Ring time (max 300 sec)', help="The 'Ring time' field defines how long the call group should ring until it switches to the next destination.", required=False)
    extensions = fields.Many2many(comodel_name='sip.users', string='Extensions for call group',help="The 'extensions for call group' defines which extensions will ring when the call group extension number is dialed.", required=True)
    #destination = fields.Many2one(comodel_name='sip.users', string='Set no answer to extension')
    #destination1 = fields.Many2one(comodel_name='sip.trunks', string='Set no answer to trunk')
    #destination2 = fields.Many2one(comodel_name='call.groups', string='Set no answer to call group')
    #destination3 = fields.Many2one(comodel_name='voice.mail', string='Set no answer to voicemail')
    #destination4 = fields.Many2one(comodel_name='call.forward', string='Set no answer to call forward')
    enabled = fields.Boolean('Enabled', default=True, help="""This function serves no purpose yet! 
    The 'enabled' field is used to turn the call group on or off.""", required=True)
    
    
    def get_sips(self):
        sips = []
        for rec in self:
            print rec.extensions
            for sip in rec.extensions:
                print sip.extension
                sips += [sip.extension]
        return '%26'.join(sips)
   

class Voice_mail(models.Model):
    _name = 'voice.mail'
    _rec_name = 'voicemailextension'
    _description = 'Voicemail'
    context = fields.Char('Context', help="The 'Context' field should match the context defined in SIP users.", required=True)
    pin = fields.Char('Pin', help="The 'Pin' field defines the password that is used when retrieving voicemail messages on a SIP phone.", required=True)
    email = fields.Char('Email address', help="The 'Email address' field is an optional field where an email address can be entered. If a valid email address is entered an email will be sent when someone leaves a voicemail. ", required=False)
    attachment = fields.Boolean('Email attachment', help="The 'Email attachment' field is an optional field which can be checked to sent an attachment of the voicemail to the email address (defined at the 'Email address' field).", required=False)
    maximummessages = fields.Char('Maximum messages', help="""The 'Maximum messages' field defines how many voicemail messages can be received. 
If the mailbox is full the caller will be unable to leave a message and will hear a recording that the mailbox is full. 
The voicemail messages can be deleted by dialing the number for voicemail messages, and choosing the delete option at the message which has to be deleted. """, required=True)
    voicemailextension = fields.Char('Voicemail extension', help="The 'Voicemail extension' field defines the number that will be read to the caller when the caller reaches voicemail.", required=True)
    fullname = fields.Char('Full name', help="The 'full name' field is an optional field, if entered this field will address the receiver of the email by the defined 'Full name'.", required=False) 
    messages = fields.Char('Number for voicemail messages', help="The 'Number for voicemail messages' field, defines which number the user has to dial to listen to the voicemail messages.", required=True)
    enabled = fields.Boolean('Enabled', default=True, help="""This function serves no purpose yet! 
    The 'enabled' field is used to turn the voicemail on or off.""", required=True)

class Call_forward(models.Model):
    _name = 'call.forward'
    _rec_name = 'forwardto'
    _description = 'Call forward'
    created = fields.Boolean('Call forward created?', default=True)
    forwardto= fields.Char('Forward to', required=True)
    description = fields.Char('Description', required=False)
    
    
class Users_forward(models.Model):
    _inherit = "res.users"
    sip_user = fields.Many2one(comodel_name='sip.users', string='Extension')
    forward = fields.Many2one(comodel_name='call.forward', string='Forward to')

