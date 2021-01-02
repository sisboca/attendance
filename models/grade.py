from odoo import models, fields, api, _
import math 
class OpGrade(models.Model):
    _name = "op.grade"
    _description = "Student Grade Details"

    session = fields.Many2one('op.session', 'Session')
    grade_class = fields.Many2one('op.grade.faculty', 'Class')
    course = fields.Many2one('op.course', 'Course')
    batch = fields.Many2one('op.batch', 'Batch')
    subject = fields.Many2one('op.subject', 'Subject')
    student = fields.Many2one('op.student', 'Student')
    faculty = fields.Many2one('op.faculty', 'Faculty')
    
    attendance_grade = fields.Float('Attendance Grade')
    daily_grade = fields.Float('Daily Grade')
    homework_grade = fields.Float('Homework Grade')
    exam_grade = fields.Float('Exam Grade')
    
    attendance_percent = fields.Float('Attendance percent')
    daily_percent = fields.Float('Daily percent')
    homework_percent = fields.Float('Homework percent')
    exam_percent = fields.Float('Exam percent')

    final_grade = fields.Float('Final Grade')
   
    @api.onchange('attendance_grade', 'daily_grade', 'homework_grade', 'exam_grade')
    def compute_attendance(self):
        if self.attendance_grade > 100:
            res = {'warning': {'title': _('Invalid grade'),'message': _('Grade can\'t be more than 100')}}  
            self.attendance_grade = 100
            self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
            return res
        if self.daily_grade > 100:
            res = {'warning': {'title': _('Invalid grade'),'message': _('Grade can\'t be more than 100')}}  
            self.daily_grade = 100
            self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
            return res
        if self.homework_grade > 100:
            res = {'warning': {'title': _('Invalid grade'),'message': _('Grade can\'t be more than 100')}}  
            self.homework_grade = 100
            self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
            return res
        if self.exam_grade > 100:
            res = {'warning': {'title': _('Invalid grade'),'message': _('Grade can\'t be more than 100')}}  
            self.exam_grade = 100
            self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
            return res
        if self.attendance_grade < 0:
            res = {'warning': {'title': _('Invalid grade'),'message': _('Grade can\'t be less than 0')}}  
            self.attendance_grade = 0
            self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
            return res
        if self.daily_grade < 0:
            res = {'warning': {'title': _('Invalid grade'),'message': _('Grade can\'t be less than 0')}}  
            self.daily_grade = 0
            self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
            return res
        if self.homework_grade < 0:
            res = {'warning': {'title': _('Invalid grade'),'message': _('Grade can\'t be less than 0')}}  
            self.homework_grade = 0
            self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
            return res
        if self.exam_grade < 0:
            res = {'warning': {'title': _('Invalid grade'),'message': _('Grade can\'t be less than 0')}}  
            self.exam_grade = 0
            self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
            return res    
        self.final_grade = (self.attendance_grade*self.attendance_percent + self.daily_grade*self.daily_percent + self.homework_grade*self.homework_percent + self.exam_grade*self.exam_percent)/100
    
    @api.onchange('final_grade')
    def change_final_grade(self):
        if self.final_grade - math.floor(self.final_grade) >= 0.5:
            self.final_grade = math.floor(self.final_grade) + 1
        else:
            self.final_grade = math.floor(self.final_grade)
        
class OpGradeConfiguration(models.Model):
    _name = "op.grade.configuration"
    _description = "Student Grade Configuration"
    course = fields.Many2one('op.course', 'Course')
    batch = fields.Many2one('op.batch', 'Batch')
    subject = fields.Many2one('op.subject', 'Subject')
    faculty = fields.Many2one('op.faculty', 'Faculty')
    session = fields.Many2one('op.session', 'Session')

    grade_percent = fields.Selection([
        ('t1', 'Хичээлийн үнэлгээний хувь'),
        ('t2', 'Гоо зүйн хичээлийн үнэлгээний хувь')
    ], 'Grade type', required=True, default='t1')

    attendance_percent = fields.Float('Attendance percent', compute="compute_grade")
    daily_percent = fields.Float('Daily percent', compute="compute_grade")
    homework_percent = fields.Float('Homework percent', compute="compute_grade")
    exam_percent = fields.Float('Exam percent', compute="compute_grade")
   
    @api.onchange('grade_percent')
    def compute_grade(self):
        if self.grade_percent == 't1':
            self.attendance_percent = 10
            self.daily_percent = 20
            self.homework_percent = 30
            self.exam_percent = 40
        else:
            self.attendance_percent = 10
            self.daily_percent = 30
            self.homework_percent = 30
            self.exam_percent = 30

    def generate_grades(self):
        vels = {
            'course' : self.course.id,
            'batch' : self.batch.id,
            'subject' : self.subject.id,
            'faculty' : self.faculty.id, 
            'session' : self.session.id
        }
        keke = self.env['op.grade.faculty'].create(vels)
        
        students = self.env['op.student'].search([('course_detail_ids.course_id', '=', self.course.id), ('course_detail_ids.batch_id', '=', self.batch.id)])
        for student in students:
            vals = {
                    'session' : self.session.id,
                    'grade_class': keke.id,
                    'student': student.id, 
                    'course': self.course.id,
                    'batch': self.batch.id,
                    'subject': self.subject.id, 
                    'faculty':self.faculty.id,
                    'attendance_percent': self.attendance_percent,
                    'daily_percent': self.daily_percent,
                    'homework_percent': self.homework_percent,
                    'exam_percent': self.exam_percent
                    }
            self.env['op.grade'].create(vals)