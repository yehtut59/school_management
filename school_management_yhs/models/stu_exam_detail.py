from odoo import fields,models,api

class StudentExamDetail(models.Model):
    
    _name = "student.exam.detail"
    _descroiption = "Student Exam Detail"
    
    
    student_exam_id = fields.Many2one('school.student.exam',string="Student Exam",required=True)
    exam_id = fields.Many2one(related="student_exam_id.exam_id",string="Exam")
    student_id = fields.Many2one(related="student_exam_id.student_id",string="Student")
    subject_id = fields.Many2one('school.subjects',string="Subject",required=True)
    marks_obtained = fields.Float(string="Marks Obtained",required=True,default=0.0)
    remarks = fields.Text(string="Remarks")
    grade = fields.Char(string="Grade",compute="_compute_grade",store=True)
    is_passed = fields.Boolean(string="Is Passed",default=False)
    
    @api.depends('marks_obtained')
    def _compute_grade(self):
        for rec in self:
            if rec.marks_obtained >= 90:
                rec.grade = 'A'
            elif rec.marks_obtained >= 80:
                rec.grade = 'B'
            elif rec.marks_obtained >= 70:
                rec.grade = 'C'
            elif rec.marks_obtained >= 60:
                rec.grade = 'D'
            else:
                rec.grade = 'F'
    