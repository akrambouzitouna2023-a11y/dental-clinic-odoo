{
    'name': 'Dental Clinic',
    'version': '1.0.0',
    'category': 'Healthcare',
    'summary': 'Dental Clinic Patient Management',
    'description': 'Patient registration and treatment tracking for dental clinic',
    'author': 'Dental Clinic',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
