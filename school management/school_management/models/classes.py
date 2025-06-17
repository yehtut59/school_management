from odoo import fields,models,api

class Classes(models.Model):
    _name = 'school.classes'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    _description = 'Classes'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    # main_subject = fields.Many2one('school.subjects', string='Main Subject', required=True,domain="[('sub_type', '=', 'major')]")
    student_ids = fields.One2many('school.students','class_id',string='Students',domain="[('state', '!=', 'draft')]")
    teacher_ids = fields.Many2many('school.teachers', string='Teachers')
    subject_ids = fields.Many2many('school.subjects', string='Subjects',domain="[('sub_type', '=', 'minor')]")
    years = fields.Selection(
        [('first', 'First Year'), ('second', 'Second Year'), ('third', 'Third Year'),('fourth', 'Fourth Year')],
        string='Year',
        required=True,
        default='first'
    )
    # main_attachment_ids = fields.Many2many('ir.attachment', string="Main Attachments", store=True)
