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
    related_employee_id = fields.Many2one('hr.employee', string='Related Employee')
    state = fields.Selection([('draft', 'Draft'),('edit', 'Edit'), ('confirm', 'Confirmed')], string='Status', default='draft')
    
    
    def view_related_employee(self):   
        self.ensure_one()
        result = self.env["ir.actions.actions"]._for_xml_id('hr.open_view_employee_list_my')
        # override the context to get rid of the default filtering on operation type
        result['domain'] = [('related_teacher_id', '=', self.id)]
        result['context'] = {'create': False}
        return result
    
    def action_confirm(self):
        for rec in self:
            if rec.state == 'draft':
                related_emp = self.env['hr.employee'].create({
                    'name': rec.name,
                    'work_email': rec.email,
                    'work_phone': rec.phone,
                    'related_teacher_id': rec.id,
                })
                rec.related_employee_id = related_emp.id
                rec.state = 'confirm'
            elif rec.state == 'edit':
                rec.state = 'confirm'
            
    def action_edit(self):
        for rec in self:
            if rec.state == 'confirm':
                rec.state = 'edit'
                

    
    @api.onchange('dob')
    def onchange_age(self):
        for res in self:
            if res.dob:
                res.age = datetime.now().year - res.dob.year
            else:
                res.age = 0