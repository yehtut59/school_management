from odoo import fields, models, api


class SchoolExam(models.Model):
    
    _name = "school.exam"
    _description = "School Exam"
    
    name = fields.Char(name="Exam Name", required=True)
    code = fields.Char(name="Exam Code", readonly=True)
    start_date = fields.Date(name="Start Date", required=True)
    end_date = fields.Date(name="End Date", required=True)
    major_id = fields.Many2one('school.majors', string='Major', required=True)
    subject_ids = fields.Many2many('school.subjects', string='Subjects', required=True)
    student_exam_ids = fields.One2many('school.student.exam', 'exam_id', string='Students')
    exam_timetable_ids = fields.One2many('school.exam.timetable', 'exam_id', string='Exam Timetable')
    class_ids = fields.Many2many('school.classes', string='Classes', required=True)
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('in_progress','In Progress'),('done','Done')],string="Status",default='draft')
    @api.onchange('class_ids')
    def _onchange_class_ids(self):
        for rec in self:
            if rec.class_ids and rec.state == 'draft':
                children_vals = []
                rec.student_exam_ids = [(5, 0, 0)]
                for cls in rec.class_ids:
                    for stu in cls.student_ids:
                        children_vals.append((0, 0, {
                            'student_id': stu.id,
                        }))
                        # student_exams = self.env['school.student.exam'].create({
                        #     'exam_id': rec.id,
                            
                
                        # })
                rec.student_exam_ids = children_vals
    
class SchoolStudentExam(models.Model):
    
    _name = "school.student.exam"
    _description = "School Student Exam"
    
    exam_id = fields.Many2one('school.exam', string='Exam', required=True)
    stu_exam_detail_ids = fields.One2many('student.exam.detail', 'student_exam_id', string='Exam Details')
    student_id = fields.Many2one('school.students', string='Student', required=True)
    stu_id = fields.Char(related='student_id.stu_id', string='Student ID', store=True)
    total_marks = fields.Float(string='Total Marks', required=True,default=0.0)
    rating = fields.Float(string='Rating', required=True,default=0.0)
    # grade = fields.Char(string='Grade', compute='_compute_grade', store=True)
    
    
    # @api.depends('total_marks', 'total_marks')
    # def _compute_grade(self):
    #     for rec in self:
    #         if rec.total_marks > 0:
    #             percentage = (rec.total_marks / rec.total_marks) * 100
    #             if percentage >= 90:
    #                 rec.grade = 'A'
    #             elif percentage >= 80:
    #                 rec.grade = 'B'
    #             elif percentage >= 70:
    #                 rec.grade = 'C'
    #             elif percentage >= 60:
    #                 rec.grade = 'D'
    #             else:
    #                 rec.grade = 'F'
    #         else:
    #             rec.grade = 'N/A'

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
    
    exam_id = fields.Many2one('school.exam', string='Exam', required=True)
    subject_id = fields.Many2one('school.subjects', string='Subject', required=True)
    exam_date = fields.Date(string='Exam Date', required=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    total_marks = fields.Float(string='Total Marks', required=True)
    class_id = fields.Many2one('school.classes', string='Class', required=True)
    class_code = fields.Char(related='class_id.code', string='Class Code', store=True)
    