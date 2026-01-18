from odoo import models, fields, api

class Classes(models.Model):
    
    _inherit = 'school.classes'
    
    
    def mapped_days(self):
        days = self.class_schedule_ids.mapped('day_of_week')
        return days
    
    
    def search_days_hours(self,day_h,subject_id):
        hour = self.class_schedule_ids.search([('day_of_week','=',day_h),('subject_id','=',subject_id)],limit=1)
        hours = hour.start_time + " - " + hour.end_time
        return hours