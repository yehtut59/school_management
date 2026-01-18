from odoo import models,fields,api
from odoo.exceptions import ValidationError

class ClassScheduleType(models.Model):
    
    _name = 'class.schedule.type'
    _description = 'Class Schedule Type'
    
    
    name = fields.Char(required=True)

    subject_hours = fields.Float(
        string='Hours per Subject',
        required=True
    )

    hours_per_day = fields.Float(
        string='Hours per Day',
        required=True,help="Not including lunch time."
    )
    
    subject_per_day = fields.Integer(
        string='Subjects per Day',store=True,compute="_compute_subject_per_day"
    )

    # ⏰ Time fields
    check_in_time = fields.Float(
        string='First Subject Start Time',
        help='Example: 8.0 = 08:00, 13.5 = 13:30'
    )

    lunch_start_time = fields.Float(
        string='Lunch Start Time'
    )

    lunch_end_time = fields.Float(
        string='Lunch End Time'
    )

    lunch_duration = fields.Float(
        compute='_compute_lunch_duration',
        store=True
    )

    note = fields.Text()
    
    status = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed')],string="Status",default="draft",required=True
        
    )
    
    
    @api.constrains('hours_per_day','subject_hours','check_in_time','subject_per_day',
                     'lunch_start_time','lunch_duration')
    def check_timetable_validaty(self):
        for rec in self:
            total_hours = rec.subject_per_day * rec.subject_hours
            if rec.hours_per_day != total_hours:
                raise ValidationError(f"Total hours per day ({rec.hours_per_day}) must be greater than or equal to the sum of subject hours ({total_hours})")
    
            start_minute = rec.check_in_time * 60
            lunch_minute = rec.lunch_start_time * 60
            subject_minutes = rec.subject_hours  * 60
            
            available_minutes = lunch_minute - start_minute
            
            if available_minutes <= 0:
                raise ValidationError("Lunch time must be after class start time.")

            max_subjects_before_lunch = available_minutes // subject_minutes

            # Actual subjects needed before lunch
            required_subjects_before_lunch = (
                available_minutes / subject_minutes
            )

            # If partial subject overlaps lunch → invalid
            if required_subjects_before_lunch % 1 != 0:
                raise ValidationError(
                    "Subjects before lunch overlap lunch time. "
                    "Please adjust check-in time, lunch time, or subject duration."
                )

    @api.depends('hours_per_day','subject_hours')
    def _compute_subject_per_day(self):
        for rec in self:
            
            rec.subject_per_day = int(rec.hours_per_day / rec.subject_hours) if rec.hours_per_day and rec.subject_hours else 0
            

    # -------------------------
    # COMPUTE & CONSTRAINTS
    # -------------------------

    @api.depends('lunch_start_time', 'lunch_end_time')
    def _compute_lunch_duration(self):
        for rec in self:
            if rec.lunch_start_time and rec.lunch_end_time:
                rec.lunch_duration = rec.lunch_end_time - rec.lunch_start_time
            else:
                rec.lunch_duration = 0.0

    @api.constrains('lunch_start_time', 'lunch_end_time')
    def _check_lunch_time(self):
        for rec in self:
            if (
                rec.lunch_start_time
                and rec.lunch_end_time
                and rec.lunch_end_time <= rec.lunch_start_time
            ):
                raise ValidationError(
                    'Lunch end time must be later than lunch start time.'
                    
                )
                
    def generate_timetable(self):
        for rec in self:
            
            return True
            
                
                
    def action_confirm(self):
        self.ensure_one()
        self.status = 'confirm'
    