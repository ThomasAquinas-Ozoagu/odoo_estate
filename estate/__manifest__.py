# -*- coding: utf-8 -*-


{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Sales/Real Estate',
    'description': "Advertise new houses",
    'depends': [
        'base',
        'mail',
           ],
    'installable': True,
    'application': True,

     'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
#        'views/estate_property_seller_views.xml',
         'views/estate_menus.xml',

     ]


}
