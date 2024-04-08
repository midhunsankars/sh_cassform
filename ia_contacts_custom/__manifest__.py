# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2023 (<http://ioppolo.com.au>).
###############################################################################

{
    "name": "Base Customization",
    "version": "16.02",
    "depends": [
        "account",
        "sale",
        "base",
        "crm",
        "contacts",
        "mail"
    ],
    "category": "Ioppolo & Associates",
    "author": "Ioppolo & Associates",
    "website": "http://www.ioppolo.com.au/",
    "summary": "This Base Customizations",
    "description": """
        This Module provides below functions
        Purchase Customizations
        Sale and Account Customizations
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/crm_leads.xml',
        'views/res_partner.xml',
        'views/zone_master.xml',
        'views/post_code.xml',
        'views/crm_lead_lost.xml',
        'views/purchase_order.xml',
        'views/product_packages.xml',
        'views/stock_picking.xml',
        'views/invoice.xml',
    ],
    "installable": True,
    'license': 'LGPL-3',
}
