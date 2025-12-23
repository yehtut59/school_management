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
    subject_ids = fields.Many2many('school.subjects', string='Subjects')
    years = fields.Selection(
        [('first', 'First Year'), ('second', 'Second Year'), ('third', 'Third Year'),('fourth', 'Fourth Year')],
        string='Year',
        required=True,
        default='first'
    )
    parent_id = fields.Many2one('school.classes', string='Parent Class')
    is_parent = fields.Boolean(string='Is Parent Class', compute='_compute_is_parent', store=True)
    is_active = fields.Boolean(string='Is Active', default=False)
    start_date = fields.Date(string='Start Date')
    has_child_class  = fields.Boolean(string='Has Child Class', compute='_compute_has_child_class', store=True)
    
    
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
            
            
    def generate_child_classes(self):
        for res in self:
            if (not res.is_parent) and res.years == 'first':
                res.start_date = fields.Date.today()
                total_year = res.major_id.total_years
                years_mapping = {
                    1: 'second',
                    2: 'third',
                    3: 'fourth'
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
                
                    
                
                
