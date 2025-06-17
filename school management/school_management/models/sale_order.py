from odoo import fields,models,api

class SaleOrder(models.Model):
    
    _inherit = 'sale.order'
    
    sale_type = fields.Selection([('student','Student'),('normal','Normal')], string='Sale Type', default='normal', required=True)
    student_id = fields.Many2one('school.students', string='Student')
    
    
    
    def _prepare_invoice(self):
        res = super(SaleOrder,self)._prepare_invoice()
        res.update({'sale_type': self.sale_type,
                    'student_id': self.student_id.id })
        return res