from odoo import _, api, fields, models

class LuanChuyenTaiSan(models.Model):
    _name = 'luan_chuyen_tai_san'
    _description = 'Bảng chứa thông tin Luân chuyển tài sản'

    bo_phan_nguon = fields.Many2one('phong_ban', string='Bộ phận hiện tại', required=True)
    bo_phan_dich = fields.Many2one('phong_ban', string='Bộ phận nhận', required=True)
    thoi_gian_luan_chuyen = fields.Datetime('Thời gian luân chuyển', required=True, default=fields.Datetime.now)
    ghi_chu = fields.Char('Ghi chú', default='')

    luan_chuyen_line_ids = fields.One2many('luan_chuyen_tai_san_line', 'luan_chuyen_id', string='Danh sách tài sản')
    