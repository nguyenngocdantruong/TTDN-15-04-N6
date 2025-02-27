from odoo import _, api, fields, models

class DanhMucTaiSan(models.Model):
    _name = 'danh_muc_tai_san'
    _description = 'Bảng chứa thông tin danh mục tài sản'
    _rec_name = "ten_danh_muc_ts"
    
    ma_danh_muc_ts = fields.Char('Mã danh mục tài sản', required=True)
    ten_danh_muc_ts = fields.Char('Tên danh mục tài sản', required=True)
    mo_ta_danh_muc_ts = fields.Char('Mô tả danh mục tài sản')

    tai_san_ids = fields.One2many('tai_san', 'danh_muc_ts_id', string='Tài sản')