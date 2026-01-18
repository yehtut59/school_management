from odoo import fields, models, api


class ClassSchedule(models.Model):
    _name = 'school.class.schedule'
    _description = 'Class Schedule'

    name= fields.Char(string='Name',readonly=True)
    class_id = fields.Many2one('school.classes', string='Class', required=True, ondelete='cascade')
    schedule_type_id = fields.Many2one(related="class_id.schedule_type_id",string="Schedule Type")
    day_of_week = fields.Selection(
        [('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
         ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')],
        string='Day of the Week',
        required=True
    )
    subject_ids = fields.Many2many('school.subjects', string='Subjects')
    schedule_detail_ids = fields.One2many('class.schedule.detail', 'class_schedule_id', string='Schedule Details')
    schedule_mode = fields.Selection(related="class_id.schedule_mode",string='Schedule Mode',store=True)
    
    @api.model
    def create(self, values):
        result = super(ClassSchedule,self).create(values)
        result['name'] =result.class_id.name + result.day_of_week.upper()
        return result
    
   
                
                
    def view_schedule_detail(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Schedule Details',
            'view_mode': 'form',
            'res_model': 'school.class.schedule',
            'res_id': self.id,
            'view_id': self.env.ref('school_management_yhs.class_schedule_details_wizard').id,
            'domain': [('class_id','=',self.class_id.id)],
            'target': 'new',
        }
                
class ClassScheduleDetail(models.Model):
    
    
    _name = 'class.schedule.detail'
    _description = 'Class Schedule Detail'
    
    
    class_schedule_id = fields.Many2one('school.class.schedule',string="Class Schedule",required=True, ondelete='cascade')
    class_id = fields.Many2one(related="class_schedule_id.class_id",string="Class",store=True)
    domain_subject_ids = fields.Many2many(related='class_id.subject_ids', string='Subjects')
    subject_id = fields.Many2one('school.subjects', string='Subject')
    domain_teacher_ids = fields.Many2many('school.teachers', string='Teachers', compute='_compute_domain_teacher_ids', store=True)
    teacher_id = fields.Many2one('school.teachers', string='Teacher')
    day_of_week = fields.Selection(related="class_schedule_id.day_of_week",string='Day of the Week',required=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    schedule_mode = fields.Selection(related="class_id.schedule_mode",string='Schedule Mode',store=True)
    
    @api.depends('class_id')
    def _compute_domain_teacher_ids(self):
        for rec in self:
            if rec.class_id:
                rec.domain_teacher_ids = self.env['school.teachers'].search([('class_ids','in',rec.class_id.ids)]).ids
            else:
                rec.domain_teacher_ids = [(5, 0, 0)]