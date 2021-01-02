from odoo import models, fields, api, _

class OpFacultyGrade(models.Model):
    _name = "op.grade.faculty"
    _description = "Faculty Grade"
    session = fields.Many2one('op.session', 'Session')
    course = fields.Many2one('op.course', 'Course')
    batch = fields.Many2one('op.batch', 'Batch')
    subject = fields.Many2one('op.subject', 'Subject')
    faculty = fields.Many2one('op.faculty', 'Faculty')
    students_grade = fields.One2many('op.grade', 'grade_class', domain="[('faculty', '=', faculty),('course', '=', course), ('batch', '=', batch), ('subject', '=', subject)]")