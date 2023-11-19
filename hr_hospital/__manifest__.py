{
    'name': "Hospital",
    'summary': "Hospital Management System",

    'author': "Uliana Kurianska",
    'website': "http://www.mycompany.com",

    'category': "Customization",
    'license': "LGPL-3",
    'version': "15.0.1.0.0",

    'depends': ["base"],

    'data': [
        "data/data_disease.xml",
        "security/ir.model.access.csv",
        "report/model_report_doctor_template.xml",
        "report/models_report.xml",
        "views/menu.xml",
        "views/patient_view.xml",
        "views/doctor_view.xml",
        "views/disease_view.xml",
        "views/visit_view.xml",
        "views/diagnosis_view.xml",
        "views/patient_test_view.xml",
        "views/doctor_schedule_calendar.xml",
        "wizard/reassign_doctor_wizard.xml",
        "wizard/disease_report_wizard.xml",
        "wizard/reschedule_visit_wizard.xml",
        "wizard/doctor_schedule_wizard_week.xml",
        "wizard/mass_reassign_doctor_wizard.xml",
    ],

    'demo': [
        'demo/demo_doctor.xml',
        'demo/demo_patient.xml',
    ],

    'installable': True,
    'auto_install': False,
}
