from odoo import models, fields, api


class FootballTeam(models.Model):
    _name = "football.team"
    _description = "Football Team"

    name = fields.Char(string="Tên Đội", required=True)
    coach_name = fields.Char(string="Tên HLV")
    player_ids = fields.One2many(
        "football.player", "team_id", string="Danh sách Cầu thủ"
    )

    # Dependent field
    total_salary = fields.Float(
        string="Tổng Lương", compute="_compute_total_salary", store=True
    )

    @api.depends("player_ids.salary")
    def _compute_total_salary(self):
        for team in self:
            team.total_salary = sum(player.salary for player in team.player_ids)


class FootballPlayer(models.Model):
    _name = "football.player"
    _description = "Football Player"

    name = fields.Char(string="Tên Cầu thủ", required=True)
    team_id = fields.Many2one("football.team", string="Đội bóng")
    salary = fields.Float(string="Lương")
    position = fields.Selection(
        [
            ("zk", "Thủ môn"),
            ("df", "Hậu vệ"),
            ("mf", "Tiền vệ"),
            ("fw", "Tiền đạo"),
        ],
        string="Vị trí",
    )

    # Multi-level dependency
    coach_name = fields.Char(string="HLV", compute="_compute_coach_name", store=True)

    # Onchange experiment
    suggested_bonus = fields.Float(string="Thưởng đề xuất")

    @api.depends("team_id.coach_name")
    def _compute_coach_name(self):
        for player in self:
            player.coach_name = player.team_id.coach_name

    @api.onchange("salary", "position")
    def _onchange_suggested_bonus(self):
        if self.position == "fw":
            self.suggested_bonus = self.salary * 0.1
        elif self.position == "zk":
            self.suggested_bonus = self.salary * 0.05
        else:
            self.suggested_bonus = 0.0


class FootballMatch(models.Model):
    _name = "football.match"
    _description = "Football Match"

    name = fields.Char(string="Tên Trận đấu", required=True)
    date = fields.Date(string="Ngày thi đấu")
    team_home_id = fields.Many2one("football.team", string="Đội Nhà")
    team_away_id = fields.Many2one("football.team", string="Đội Khách")

    # Many2many with fields (via intermediate)
    lineup_ids = fields.One2many(
        "football.match.lineup", "match_id", string="Đội hình ra sân"
    )

    # Deep dependency (Level 2)
    # Depends on team_home_id (Level 1) -> total_salary (Level 2, which depends on players)
    home_team_value = fields.Float(
        string="Giá trị Đội nhà", compute="_compute_home_team_value", store=True
    )

    @api.depends("team_home_id.total_salary")
    def _compute_home_team_value(self):
        for match in self:
            match.home_team_value = match.team_home_id.total_salary


class FootballMatchLineup(models.Model):
    _name = "football.match.lineup"
    _description = "Match Lineup (Intermediate Table)"

    match_id = fields.Many2one(
        "football.match", string="Trận đấu", required=True, ondelete="cascade"
    )
    player_id = fields.Many2one("football.player", string="Cầu thủ", required=True)

    # Extra fields for Many2many relationship
    goals = fields.Integer(string="Bàn thắng")
    assists = fields.Integer(string="Kiến tạo")
    minutes_played = fields.Integer(string="Phút thi đấu")
