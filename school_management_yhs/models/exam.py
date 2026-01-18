from odoo import fields, models, api
from odoo.exceptions import UserError

class SchoolExam(models.Model):
    
    _name = "school.exam"
    _description = "School Exam"
    
    name = fields.Char(name="Exam Name", required=True, help="Mid/Final Exam etc.")
    code = fields.Char(name="Exam Code", readonly=True,compute="_compute_code", store=True)
    start_date = fields.Date(name="Start Date", required=True)
    end_date = fields.Date(name="End Date", required=True)
    major_id = fields.Many2one('school.majors', string='Major', required=True)
    years = fields.Selection(
        [('first', 'First Year'), ('second', 'Second Year'), ('third', 'Third Year'),('fourth', 'Fourth Year'),('fifth', 'Fifth Year'),('sixth', 'Sixth Year')],
        string='Year',
       
    )
    edu_level = fields.Selection(related='major_id.edu_level', string='Education Level', store=True)
    grades = fields.Selection(
        [('1', 'Grade 1'), ('2', 'Grade 2'), ('3', 'Grade 3'), ('4', 'Grade 4'), ('5', 'Grade 5'),
         ('6', 'Grade 6'), ('7', 'Grade 7'), ('8', 'Grade 8'), ('9', 'Grade 9'), ('10', 'Grade 10'),
         ('11', 'Grade 11'), ('12', 'Grade 12')],
        string='Grades',
    )
    # domain_subject_ids = fields.Many2many('school.subjects', string='Subjects',compute='_compute_domain_subjects',store=True)
    subject_ids = fields.Many2many('school.subjects', string='Subjects', required=True,store=True,compute="_compute_subjects")
    student_exam_ids = fields.One2many('school.student.exam', 'exam_id', string='Students',ondelete='cascade',store=True)
    exam_timetable_ids = fields.One2many('school.exam.timetable', 'exam_id', string='Exam Timetable',ondelete='cascade')
    class_ids = fields.Many2many('school.classes', string='Classes', required=True,domain="[('is_active','=',True)]")
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('in_progress','In Progress'),('done','Done'),('result','Result')],string="Status",default='draft')
    total_marks = fields.Float(string="Total Marks", compute="_compute_total_marks", store=True)
    
    # @api.depends('major_id')
    # def _compute_domain_subjects(self):
    #     for rec in self:
    #         if rec.major_id:
    #             rec.domain_subject_ids = self.env['school.subjects'].search([('major_id','=',rec.major_id.id)]).ids
    #         else:
    #             rec.domain_subject_ids = [(5, 0, 0)]
    
    def generate_exam_students(self):
        for rec in self:
            children_vals = []
            rec.student_exam_ids = [(5, 0, 0)]
            for cls in rec.class_ids:
                for stu in cls.student_ids:
                    children_vals.append((0, 0, {
                        'student_id': stu.id,
                    }))
            rec.student_exam_ids = children_vals
    
    
    @api.depends('major_id','years')
    def _compute_subjects(self):
        for rec in self:
            if rec.major_id and rec.years:
                rec.subject_ids = self.env['school.majors.curriculum'].search([('major_id','=',rec.major_id.id),('years','=',rec.years)]).mapped('subject_ids').ids
            else:
                rec.subject_ids = [(5, 0, 0)]

    @api.depends('exam_timetable_ids.total_marks')
    def _compute_total_marks(self):
        for rec in self:
            rec.total_marks = sum(rec.exam_timetable_ids.mapped('total_marks'))
            
            
    @api.depends('name','major_id')
    def _compute_code(self):
        for rec in self:
            if rec.name and rec.major_id:
                seq = self.env['ir.sequence'].next_by_code('school.exam') or '/'
                rec.code = f"{rec.major_id.code}-{rec.name[:3].upper()}:{seq}"
            else:
                rec.code = ''
    
    
    # @api.onchange('class_ids')
    # def _prepare_student_exam_lines(self):
    #     for rec in self:
    #         if rec.class_ids and rec.state == 'draft':
    #             children_vals = []
    #             rec.student_exam_ids = [(5, 0, 0)]
    #             for cls in rec.class_ids:
    #                 for stu in cls.student_ids:
    #                     children_vals.append((0, 0, {
    #                         'student_id': stu.id,
    #                     }))
    #                     # student_exams = self.env['school.student.exam'].create({
    #                     #     'exam_id': rec.id,
                            
                
    #                     # })
    #             rec.student_exam_ids = children_vals
                
    def action_confirm(self):
        self.ensure_one()
        subject_ids = self.subject_ids.ids
        check_sub_timetable = self.env['school.exam.timetable'].search_count([('exam_id','=',self.id),('subject_id','in',subject_ids)])
        if check_sub_timetable < len(subject_ids):
            raise UserError("Please set exam timetable for all subjects before confirming the exam.")
        else:
            self.state = 'confirm'
            
    def action_start_exam(self):
        self.ensure_one()
        self.state = 'in_progress'
        
    def action_end_exam(self):
        self.ensure_one()
        self.state = 'done'
        
    def action_publish_result(self):
        self.ensure_one()
        for stu in self.student_exam_ids:
            result_count = self.env['student.exam.detail'].search_count([('student_exam_id','=',stu.id)])
            if result_count < len(self.subject_ids) or result_count > len(self.subject_ids):
                raise UserError(f"Please enter all exam details for student {stu.student_id.name} before publishing results.")
            else:
                stu.total_marks = sum([detail.marks_obtained for detail in stu.stu_exam_detail_ids])
                stu.rating = (sum([detail.marks_obtained for detail in stu.stu_exam_detail_ids]) / self.total_marks) * 10 if self.total_marks > 0 else 0.0
        
        self.state = 'result'
        
    
class SchoolStudentExam(models.Model):
    
    _name = "school.student.exam"
    _description = "School Student Exam"
    
    name = fields.Char(string='Roll No.',readonly=True)
    exam_id = fields.Many2one('school.exam', string='Exam',ondelete='cascade',)
    stu_exam_detail_ids = fields.One2many('student.exam.detail', 'student_exam_id', string='Exam Details')
    student_id = fields.Many2one('school.students', string='Student', required=True)
    stu_id = fields.Char(related='student_id.stu_id', string='Student ID', store=True)
    total_marks = fields.Float(string='Total Marks', required=True,default=0.0)
    rating = fields.Float(string='Rating', required=True,default=0.0)
    status = fields.Selection(related='exam_id.state',string="Exam Status")

    @api.model
    def create(self, values):
        result = super(SchoolStudentExam,self).create(values)
        count = self.env['school.student.exam'].search_count([('exam_id', '=', result.exam_id.id)])
        result['name'] =result.exam_id.code +  str(count)
        
        return result
    

    def view_detail_stu_exam(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student Exam Details',
            'view_mode': 'form',
            'res_model': 'school.student.exam',
            'res_id': self.id,
            'view_id': self.env.ref('school_management_yhs.stu_exam_detail_wizard').id,
            'domain': [('student_id','=',self.student_id.id),('exam_id','=',self.exam_id.id )],
            'target': 'new',
        }
                
class SchoolExamTimeTable(models.Model):
    
    _name = "school.exam.timetable"
    _description = "School Exam Timetable"
    
    exam_id = fields.Many2one('school.exam', string='Exam',ondelete='cascade',)
    domain_subject_ids = fields.Many2many(related='exam_id.subject_ids', string='Subjects')
    subject_id = fields.Many2one('school.subjects', string='Subject', required=True)
    exam_date = fields.Date(string='Exam Date', required=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    total_marks = fields.Float(string='Total Marks', required=True)
    class_id = fields.Many2one('school.classes', string='Class', required=True,ondelete='cascade')
    class_code = fields.Char(related='class_id.code', string='Class Code', store=True)
    
    
    @api.model
    def create(self, values):
        result = super(SchoolExamTimeTable,self).create(values)
        exist_count = self.env['school.exam.timetable'].search_count([('exam_id', '=', result.exam_id.id),('subject_id','=',result.subject_id.id),('id','!=',result.id)])
        if exist_count > 0:
            raise UserError(f"The timetable for subject {result.subject_id.name} already exists for this exam.")
        return result