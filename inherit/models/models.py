from odoo import models, fields, api
from datetime import date

class AnimalSpecies(models.Model):
    _name = 'animal.species'
    _description = 'Danh mục Loài vật'
    _rec_name = 'name'

    name = fields.Char(string="Tên Loài", required=True)
    description = fields.Text(string="Mô tả đặc tính")
    classification = fields.Selection([
        ('mammal', 'Thú có vú'),
        ('bird', 'Chim'),
        ('reptile', 'Bò sát'),
        ('other', 'Khác')
    ], string="Phân lớp sinh học", default='mammal')

class Cage(models.Model):
    _name = 'cage'
    _description = 'Chuồng nuôi'

    name = fields.Char(string="Tên chuồng", required=True)
    species_id = fields.Many2one('animal.species', string="Dành riêng cho Loài", required=True)
    animal_ids = fields.One2many('animal.base', 'cage_id', string="Danh sách vật nuôi")

class AnimalBase(models.Model):
    _name = 'animal.base'
    _description = 'Hồ sơ động vật'

    name = fields.Char(string="Tên gọi", required=True)
    species_id = fields.Many2one('animal.species', string="Loài", required=True)
    cage_id = fields.Many2one('cage', string="Chuồng nuôi", domain="[('species_id', '=', species_id)]")
    birthday = fields.Date(string="Ngày sinh")
    age = fields.Integer(string="Tuổi đời", compute='_compute_age', store=True)

    @api.depends('birthday')
    def _compute_age(self):
        for record in self:
            if record.birthday:
                today = fields.Date.today()
                record.age = (today - record.birthday).days // 365
            else:
                record.age = 0

class AnimalBaseExtension(models.Model):
    _inherit = 'animal.base'
    
    health_status = fields.Selection([
        ('good', 'Tốt'),
        ('sick', 'Đang bệnh'),
        ('recovering', 'Đang hồi phục')
    ], string="Tình trạng sức khỏe", default='good')
    last_checkup_date = fields.Date(string="Ngày khám gần nhất")

class AnimalToy(models.Model):
    _name = 'animal.toy'       
    _inherit = 'animal.base'   
    
    price = fields.Float(string="Giá bán")
    material = fields.Char(string="Chất liệu (VD: Vải cotton)")

class RaceHorse(models.Model):
    _name = 'race.horse'
    _description = 'Ngựa đua chuyên nghiệp'
    _inherits = {'animal.base': 'animal_id'} 
    
    animal_id = fields.Many2one('animal.base', required=True, ondelete='cascade')
    top_speed = fields.Float(string="Tốc độ tối đa (km/h)")
    trophies_count = fields.Integer(string="Số cúp đạt được")

    @api.model
    def default_get(self, fields_list):
        defaults = super(RaceHorse, self).default_get(fields_list)
        horse_species = self.env['animal.species'].search([('name', '=', 'Ngựa')], limit=1)
        if horse_species:
            defaults['species_id'] = horse_species.id
        return defaults