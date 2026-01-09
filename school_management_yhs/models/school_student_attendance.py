from odoo import fields,models,api

from datetime import datetime


class SchoolStudentAttendance(models.Model):
    
    _name = 'school.student.attendance'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    _description = 'student attendance'

    student_id = fields.Many2one('school.students', string='Student', required=True)
    attendance_date = fields.Date(string='Attendance Date', required=True, default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company) 
    class_id = fields.Many2one('school.classes', string='Class', required=True)
    status = fields.Selection([('late','Late'),('present', 'Present'), ('absent', 'Absent')], string='Status', required=True, default='present')
    notes = fields.Text(string='Notes')
    subject_id = fields.Many2one('school.subjects', string='Subject', required=True)
    teacher_id = fields.Many2one('school.teachers', string='Recorded By', required=True)
    stu_id = fields.Char(string='Student ID', related='student_id.stu_id', store=True)