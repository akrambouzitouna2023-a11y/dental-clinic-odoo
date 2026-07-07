{
    'name': 'Dental Clinic',
    'version': '1.7.0',
    'category': 'Healthcare',
    'summary': 'Dental Clinic Management',
    'description': 'Patient registration, purchases and profit reporting for dental clinic',
    'author': 'Dental Clinic',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/tooth_data.xml',
        'views/patient_views.xml',
        'views/purchase_views.xml',
        'views/profit_report_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
