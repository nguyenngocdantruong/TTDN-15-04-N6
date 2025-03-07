from odoo import models, fields, api


class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Bảng chứa thông tin lịch sử công tác'
    
    time_start = fields.Date("Thời gian bắt đầu", required=True, default=lambda self: fields.Date.today())
    time_end = fields.Date("Thời gian kết thúc", required=True, default=lambda self: fields.Date.today())
    phong_ban_id = fields.Many2one("phong_ban",string="Phòng ban", required=True)
    chuc_vu_id = fields.Many2one("chuc_vu",string="Chức vụ", required=True)
    nhan_vien_id =fields.Many2one("nhan_vien",string="Nhân viên", required=True)  