from odoo import fields,models,api


class AccountPaymentRegister(models.TransientModel):
    
    _inherit = 'account.payment.register'
    
    
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get('active_model') == 'account.move.line':
            move_ids = self.env.context.get('active_ids', [])
            moves = self.env['account.move.line'].browse(move_ids)
            res['student_id'] = moves.move_id.student_id.id
        return res
    
    student_id = fields.Many2one('school.students', string='Student', readonly=True)
    
    def action_create_payments(self):
        res = super(AccountPaymentRegister,self).action_create_payments()
        self.student_id.state = 'done'
        self.student_id.is_paid = True
        self.student_id.generate_stu_code()
        return res