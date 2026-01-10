from odoo import fields,models,api

class Majors(models.Model):
    _name = 'school.majors'
    _description = 'Majors'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Majors Name',required=True)
    code = fields.Char(string='Code', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    price_unit = fields.Float(string='Price/Year', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    description = fields.Text(string='Description')
    product_id = fields.Many2one('product.product', string='Product')
    state = fields.Selection([('draft', 'Draft'),('edit','Edit'),('confirm', 'Confirmed')], default='draft', string='Status',tracking=True)
    total_years = fields.Integer(string='Total Years', required=True, digits=(2, 0),default=4)
    curriculum_ids = fields.One2many('school.majors.curriculum', 'major_id', string='Curriculum')
    edu_level = fields.Selection([('high_school', 'High School'),('bachelor', 'Bachelor'), ('master', 'Master'), ('doctorate', 'Doctorate')], string='Education Level', required=True,default='bachelor')
    
    # subject_ids = fields.Many2many('school.subjects', string='Subjects', domain="[('sub_type', '=', 'major')]")

    
    def create_product(self):
        for major in self:
            product = self.env['product.product'].create({
                'name': major.name,
                'type': 'service',
                'list_price': major.price_unit,
                'default_code': major.code,
            })
            major.product_id = product.id
            major.state = 'confirm'
            
            
    def action_edit(self):
        self.ensure_one()
        self.state = 'edit'

    def action_confirm(self):
        self.ensure_one()
        self.state = 'confirm'

class MajorsCurriculum(models.Model):
    _name = 'school.majors.curriculum'
    _description = 'Majors Curriculum'

    major_id = fields.Many2one('school.majors', string='Major', required=True,ondelete='cascade')
    subject_ids = fields.Many2many('school.subjects', string='Subject', required=True)
    years = fields.Selection(
        [('first', 'First Year'), ('second', 'Second Year'), ('third', 'Third Year'),('fourth', 'Fourth Year')],
        string='Year',
        required=True,
        default='first'
    )
    semester = fields.Selection([('1', 'Semester 1'), ('2', 'Semester 2'),('3','Semester 3'),('4','Semester 4')], string='Semester', required=True)