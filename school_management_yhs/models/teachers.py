from odoo import fields,models,api
from datetime import datetime

class Teachers(models.Model):
    
    _name = 'school.teachers'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    _description = 'teachers'

    name = fields.Char(string="Name", required=True)
    dob = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age", required=True, digits=(3, 0),store=True)
    address = fields.Text(string="Address", required=True)
    nrc = fields.Char(string="NRC",required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone", required=True)
    subject_ids = fields.Many2many('school.subjects', string='Subjects')
    class_ids = fields.Many2many('school.classes', string='Classes')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    @api.onchange('dob')
    def onchange_age(self):
        for res in self:
            if res.dob:
                res.age = datetime.now().year - res.dob.year
            else:
                res.age = 0