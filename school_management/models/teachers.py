from odoo import fields,models,api


class Teachers(models.Model):
    
    _name = 'school.teachers'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    _description = 'teachers'

    name = fields.Char(string="Name", required=True)
    dob = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age", required=True, digits=(3, 0))
    address = fields.Text(string="Address", required=True)
    nrc = fields.Char(string="NRC",required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone", required=True)
    subject_ids = fields.Many2many('school.subjects', string='Subjects')
    class_ids = fields.Many2many('school.classes', string='Classes')