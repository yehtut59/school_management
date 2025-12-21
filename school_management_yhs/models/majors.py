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
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')], default='draft', string='Status')
    total_years = fields.Integer(string='Total Years', required=True, digits=(2, 0),default=4)
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
            