from odoo import fields,models,api

class Classes(models.Model):
    _name = 'school.classes'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    _description = 'Classes'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    description = fields.Text(string='Description')
    major_id = fields.Many2one('school.majors', string='Major', required=True)
    # main_subject = fields.Many2one('school.subjects', string='Main Subject', required=True,domain="[('sub_type', '=', 'major')]")
    student_ids = fields.One2many('school.students','class_id',string='Students',domain="[('state', '==', 'done')]")
    teacher_ids = fields.Many2many('school.teachers', string='Teachers')
    subject_ids = fields.Many2many('school.subjects', string='Subjects',store=True,compute="_compute_subjects")
    class_schedule_ids = fields.One2many('school.class.schedule', 'class_id', string='Class Schedule',ondelete='cascade')
    years = fields.Selection(
        [('first', 'First Year'), ('second', 'Second Year'), ('third', 'Third Year'),('fourth', 'Fourth Year'),('fifth', 'Fifth Year'),('sixth', 'Sixth Year')],
        string='Year',
    )
    edu_level = fields.Selection(related='major_id.edu_level', string='Education Level', store=True)
    grades = fields.Selection(
        [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3'), ('4', 'Grade 4'), ('5', 'Grade 5'),
         ('6', 'Grade 6'), ('7', 'Grade 7'), ('8', 'Grade 8'), ('9', 'Grade 9'), ('10', 'Grade 10'),
         ('11', 'Grade 11'), ('12', 'Grade 12')],
        string='Grades',default='1'
    )
    schedule_mode = fields.Selection([('custom','Custom Schedule'),('fixed','Fixed Schedule')],string="Schedule Mode",default='fixed',required=True)
    schedule_type_id = fields.Many2one('class.schedule.type',string="Schedule Type")
    parent_id = fields.Many2one('school.classes', string='Parent Class')
    is_parent = fields.Boolean(string='Is Parent Class', compute='_compute_is_parent', store=True)
    is_active = fields.Boolean(string='Is Active', default=False)
    start_date = fields.Date(string='Start Date')
    has_child_class  = fields.Boolean(string='Has Child Class', compute='_compute_has_child_class', store=True)
    
    
    def generate_timetable(self):
        self.ensure_one()
        if self.schedule_type_id:
            self.schedule_type_id.generate_timetable(self)
            
    
    @api.depends('major_id','years')
    def _compute_subjects(self):
        for rec in self:
            if rec.major_id:
                curriculum_records = self.env['school.majors.curriculum'].search([('major_id','=',rec.major_id.id),('years','=',rec.years)])
                subject_list = []
                for curriculum in curriculum_records:
                    subject_list.extend(curriculum.subject_ids.ids)
                rec.subject_ids = subject_list
            else:
                rec.subject_ids = [(5, 0, 0)]
    
    @api.depends('is_parent')
    def _compute_has_child_class(self):
        for rec in self:
            if rec.is_parent:
                rec.has_child_class = bool(self.env['school.classes'].search([('parent_id','=',rec.id)]))
    # main_attachment_ids = fields.Many2many('ir.attachment', string="Main Attachments", store=True)
    
    
    # @api.model
    # def create(self, vals):
    #     if 'code' not in vals or not vals['code']:
    #         seq = self.env['ir.sequence'].next_by_code('school.classes') or '/'
    #         vals['code'] = vals['major_id'].code +"-"+ str(seq)
    #     return super(Classes, self).create(vals)
    
    def transfer_students_tonext_year(self):
        for rec in self:
            if not rec.parent_id:
                child_class = self.env['school.classes'].search(['|',('parent_id', '=', rec.id),('id','=',rec.id)],order='id desc')
                child_class_count = len(child_class)
                next_class = None
                for child in child_class:
                    if child_class_count == len(child_class) and next_class == None:
                        for student in child.student_ids:
                            student.state = 'end'
                            student.class_id = None
                            
                        next_class = child
                    else:
                        for student in child.student_ids:
                            student.class_id = next_class.id
                        next_class = child
                    child_class_count -= 1
                        
            
    
    def active_class(self):
        for rec in self:
            rec.is_active = True
            rec.start_date = fields.Date.today()
            if not rec.code:
                rec.generate_class_code()
            
            rec.class_schedule_ids.unlink()
            rec.generate_class_schedule()
            
    def deactivate_class(self):
        for rec in self:
            rec.is_active = False
            
    def generate_class_code(self):
        for rec in self:
            if not rec.code:
                seq = self.env['ir.sequence'].next_by_code('school.classes') or '/'
                rec.code = rec.major_id.code +"-"+ str(seq)
    
    
    @api.depends('parent_id')
    def _compute_is_parent(self):
        for record in self:
            record.is_parent = bool(not record.parent_id)
            
    def generate_class_schedule(self):
        self.ensure_one()
        if self.schedule_type_id and not self.class_schedule_ids:
            dow_mapping = {
                1: 'monday',
                2: 'tuesday',
                3: 'wednesday',
                4: 'thursday',
                5: 'friday',
            }
            for i in range(1,6):
                schedule = self.env['school.class.schedule'].create({
                    'class_id': self.id,
                    'day_of_week': dow_mapping[i],
                })
                schedule_type = self.schedule_type_id
                sub_per_day = self.schedule_type_id.subject_per_day
                start_time = schedule_type.check_in_time
                for y in range(0, sub_per_day):
                    
                    if start_time >= schedule_type.lunch_start_time and start_time < schedule_type.lunch_end_time:
                        start_time = schedule_type.lunch_end_time    
                        
                    self.env['class.schedule.detail'].create({ 
                        'class_schedule_id': schedule.id, 
                        'start_time': start_time,
                        'end_time' : start_time + schedule_type.subject_hours,
                    })
                    start_time += schedule_type.subject_hours
                # for 
                #     self.env['class.schedule.detail'].create({
                #         'class_schedule_id': schedule.id,
                #         'subject_id': subject.id,
                #         'start_time': ,
                #         'end_time': ,
                #     })  
                
        return True
            
    def generate_child_classes(self):
        for res in self:
            if res.is_parent and res.years == 'first' and res.edu_level != 'high_school':
                res.start_date = fields.Date.today()
                total_year = res.major_id.total_years
                years_mapping = {
                    1: 'second',
                    2: 'third',
                    3: 'fourth',
                    4: 'fifth',
                    5: 'sixth',
                }
                res.generate_class_code()
                for year in range(1, total_year):
                    child_class = self.env['school.classes'].create({
                        'name': f"{res.name} - {years_mapping[year]} Year",
                        # 'code': f"{res.major_id.code}-{year+1}",
                        'company_id': res.company_id.id,
                        'major_id': res.major_id.id,
                        'years': years_mapping[year],
                        'parent_id': res.id
                    })
                    child_class.generate_class_code()
                    
                res.is_active = True
            elif res.is_parent and res.edu_level == 'high_school' and res.grades == '1':
                res.start_date = fields.Date.today()
                total_year = res.major_id.total_years-1
                res.generate_class_code()
                for year in range(1, total_year):
                    child_class = self.env['school.classes'].create({
                        'name': f"{res.name} - Grade {year + 1}",
                        # 'code': f"{res.major_id.code}-{year+1}",
                        'company_id': res.company_id.id,
                        'major_id': res.major_id.id,
                        'grades': str(year + 1),
                        'parent_id': res.id
                    })
                    child_class.generate_class_code()
                res.is_active = True
                


                
                    
                
                
