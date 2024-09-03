{
    'name': 'Fleet Analytic Account',
    'version': '1.0',
    'category': 'Accounting',
    'author': 'Amani',
    'summary': 'Module for managing vehicle fleet with analytic accounting to track expenses and profits for each vehicle',
    'description': "Vehicule Fleet Management Module",

    'depends': ['base', 'fleet', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'data/analytic_plan_data.xml',
        # 'views/account_analytic_line_group_views.xml',
        'views/fleet_vehicle_views.xml',
        'views/res_config_settings_view_fleet.xml',
        'wizard/generation_analytic_entries.xml',
        'views/fleet_vehicle_log_services_views.xml',
    ],
    'demo': [],

    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': -100,
    'license': 'LGPL-3',

    'assets': {},
}