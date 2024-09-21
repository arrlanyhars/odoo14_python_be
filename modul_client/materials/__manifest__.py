{
    'name': 'Material Module',
    'version': '14.0.1.0.0',
    'category': 'material',
    'summary': 'Material Custom Module',
    'description': """
        Material Custom Module with API by Arryanda M
    """,
    'website': '',
    'author': 'Arryanda Maulani',
    'depends': ["web","base","mail","point_of_sale"],
    'data': [
        'security/ir.model.access.csv',
        'views/material_views.xml',
        'views/pos_assets.xml',
        'views/mail_template_data.xml',
        #'views/pos_menu.xml'
    ],
    'qweb': [],
    'application': False,
    'installable': True,
    'license': 'OEEL-1'
}
