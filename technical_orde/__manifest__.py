# -*- coding: utf-8 -*-
{
    'name': "Technical_Orde",
    'sequence': '-100',

    'summary': """
        Technical_Orde""",

    'description': """
              Technical_Orde    """,

    'author': "shehab",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','mail','sale'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/technical_sequence.xml',
        'wizard/cencel_purchase.xml',
        'views/sale_order_view.xml',
        'views/technical_order.xml',
        'views/views.xml',
        'views/res_parnter_view.xml',
        'report/tecnical_order_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3'
}
