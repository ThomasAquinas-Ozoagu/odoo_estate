# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Sales/Real Estate',
    'description': "Advertise new houses",
    'depends': [
        'base',
           ],
    'installable': True,
    'application': True,

     'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
     ]


}
