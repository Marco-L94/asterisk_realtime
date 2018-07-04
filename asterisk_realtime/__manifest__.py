# -*- encoding: utf-8 -*-
##############################################################################
#
#    open2bizz
#    Copyright (C) 2018 open2bizz (open2bizz.nl).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Asterisk realtime",
    "version": "0.1",
    "author": "Open2bizz",
    'website': 'http://www.open2bizz.nl',
    "category": "Telephony",
    "description":"Adds Asterisk Realtime functionality to Odoo",
	'depends': ['base'],
	'application': True,
	'data': [
	    'views/view_menu.xml',
            'security/groups_dropdown.xml',
	    'security/groups.xml',
            'security/ir.model.access.csv',
        'views/view_users.xml',
        'views/view_trunks.xml',
        'views/view_dialplan_inbound.xml',
        'views/view_dialplan_outbound.xml',
        'views/view_call_forward.xml',
        'views/view_callgroup.xml',
        'views/view_voicemail.xml',
        'views/res_users.xml',
        ]
}
