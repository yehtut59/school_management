from odoo import fields,models,api
from datetime import datetime

class Students(models.Model):
    _name = 'school.students'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    _description = 'students'

    stu_id = fields.Char(string='Student ID', required=True, copy=False, readonly=True, index=True,default='/')
    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age", required=False,digits=(3,0))
    dob = fields.Date(string="Date of Birth", required=True)
    nrc = fields.Char(string="NRC")
    address = fields.Text(string="Address", required=True)
    email = fields.Char(string="Email", required=True)
    father_name = fields.Char(string="Father Name", required=True)
    mother_name = fields.Char(string="Mother Name", required=True)
    phone = fields.Char(string="Phone", required=True)
    major_id = fields.Many2one('school.majors', string='Major', required=True)  # Many2one relationship with majors
    class_id = fields.Many2one('school.classes', string='Class', required=True)  # Many2one relationship with classes
    subject_ids = fields.Many2many('school.subjects', string='Subjects')  # Many2many relationship with subjects
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Paid'),('edit', 'Edit')], default='draft', string='Status',tracking=True)
    is_paid = fields.Boolean(string='Is Paid', default=False)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    
    @api.onchange('major_id')
    def _onchange_major_id(self):
        for rec in self:
            rec.class_id = None
    
    
    def editable_student(self):
        for rec in self:
            rec.state = 'edit'
            
    def confirm_edit(self):
        for rec in self:
            if rec.is_paid:
                rec.state = 'done'
            else:
                rec.state = 'confirm'
            
    
    @api.onchange('dob')
    def onchange_age(self):
        for res in self:
            if res.dob:
                res.age = datetime.now().year - res.dob.year
            else:
                res.age = 0
    
    def action_view_related_order(self):
        result = self.env["ir.actions.actions"]._for_xml_id('sale.action_quotations_with_onboarding')
        # override the context to get rid of the default filtering on operation type
        result['domain'] = [('student_id', '=', self.id),('sale_type', '=', 'student')]
        result['context'] = {'create': False}
        return result
    
    def generate_stu_code(self):
        for stu in self:
            if stu.state == 'done':
                stu.stu_id = self.major_id.code + self.env['ir.sequence'].next_by_code('school.students')
            else:
                stu.stu_id = '/'
                
                
    def create_sale_order(self):
        for stu in self:
            partner_id = self.env['res.partner'].create({
                'name': stu.name,
                'email': stu.email,
                'phone': stu.phone,
            })
            
            sale_order = self.env['sale.order'].create({
                'student_id': stu.id,
                'sale_type': 'student',
                'partner_id': partner_id.id,
                'order_line': [(0, 0, {
                    'product_id': stu.major_id.product_id.id,
                    'name': stu.major_id.name,
                    'price_unit': stu.major_id.price_unit,
                    'product_uom_qty': 1,
                })],
            })
            
            stu.sale_order_id = sale_order.id   
            stu.state = 'confirm'