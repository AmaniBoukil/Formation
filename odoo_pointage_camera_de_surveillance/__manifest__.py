{
    'name': 'Visitors',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'author': 'Amani',
    'summary': 'Manage visitors and their information',
    'description': """Visitors management system""",

    'depends': ['base'],  # installation de modules / independences

    'data': ['security/ir.model.access.csv',
             'views/visitor_view.xml',
              'views/camera_view.xml',
              'views/menu.xml',
             ],

    'demo': [],

    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': -100,
    'license': 'LGPL-3',

    'assets': {},
}
