from odoo import fields,api,models


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    
    sale_type = fields.Selection([('student', 'Student'), ('normal', 'Normal')], string='Sale Type', default='normal', required=True)
    student_id = fields.Many2one('school.students', string='Student', readonly=True)
    
    