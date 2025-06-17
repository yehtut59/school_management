from odoo import fields,models,api


class ProductTemplate(models.Model):
    
    _inherit = 'product.template'

    major_id = fields.Many2one('school.majors', string='Major',readonly=True)
    

class ProudctProduct(models.Model):
    
    _inherit = 'product.product'
        
    major_id = fields.Many2one('school.majors', string='Major',readonly=True)
    