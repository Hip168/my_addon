from odoo import models, fields

class SchoolCampus(models.Model):
    _name = 'school.campus'
    _description = 'School Campus'
    name = fields.Char()

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'
    name = fields.Char()

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'School Student'
    name = fields.Char()

class SchoolLecturer(models.Model):
    _name = 'school.lecturer'
    _description = 'School Lecturer'
    name = fields.Char()

class SchoolStaff(models.Model):
    _name = 'school.staff'
    _description = 'School Staff'
    name = fields.Char()
