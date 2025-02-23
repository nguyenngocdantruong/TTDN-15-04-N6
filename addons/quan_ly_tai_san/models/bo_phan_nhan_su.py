from odoo import _, api, fields, models

class BoPhanNhanSu(models.Model):
    _name = 'bo_phan_nhan_su'
    _description = 'Bảng chứa thông tin Bộ phận nhân sự'
    _rec_name = "ten_bo_phan"

    ma_bo_phan = fields.Char('Mã bộ phận nhân sự', required=True)
    ten_bo_phan = fields.Char(string='Tên bộ phận', required=True)
    