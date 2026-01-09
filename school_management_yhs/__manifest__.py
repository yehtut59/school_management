# -*- coding: utf-8 -*-
{
    'name': "School Management(YHS)",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','portal','digest','sale_management','account','stock','web','hr','hr_attendance','hr_contract'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/students.xml',
        'views/teachers.xml',
        'views/classes.xml',
        'views/subjects.xml',
        'views/majors.xml',
        'views/sale_order.xml',
        'views/exam.xml',
        'views/stu_exam_detail.xml',
        'views/stu_attendance.xml',
        'wizard/stu_exam_detail_wizard.xml',
        'reports/class_report.xml',
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

