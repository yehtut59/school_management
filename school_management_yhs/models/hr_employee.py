from odoo import fields,models,api
from datetime import datetime

class HrEmployee(models.Model):
    
    _inherit = 'hr.employee'

    related_teacher_id = fields.Many2one('school.teachers', string='Related Teacher')