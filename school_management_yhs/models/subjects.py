from odoo import fields,models,api


class Subjects(models.Model):
    _name = 'school.subjects'
    _description = 'subjects'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")
    sub_type = fields.Selection([('major', 'Major'), ('minor', 'Minor')], string='Subject Type', required=True,default='major')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)