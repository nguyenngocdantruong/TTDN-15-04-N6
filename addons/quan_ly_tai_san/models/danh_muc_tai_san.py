from odoo import _, api, fields, models

class DanhMucTaiSan(models.Model):
    _name = 'danh_muc_tai_san'
    _description = 'Bảng chứa thông tin loại tài sản'
    _rec_name = "ten_danh_muc_ts"
    _order = 'ma_danh_muc_ts asc'
    _sql_constraints = [
        ("ma_danh_muc_ts_unique", "unique(ma_danh_muc_ts)", "Mã loại tài sản đã tồn tại !"),
    ]
    
    ma_danh_muc_ts = fields.Char('Mã loại tài sản', required=True)
    ten_danh_muc_ts = fields.Char('Tên loại tài sản', required=True)
    mo_ta_danh_muc_ts = fields.Char('Mô tả loại tài sản')

    so_luong_tong = fields.Integer(string = 'Số lượng hiện có',compute = "_compute_so_luong_tong", store=True)
    @api.depends('tai_san_ids')
    def _compute_so_luong_tong(self):
        for record in self:
            record.so_luong_tong = len(record.tai_san_ids)

    tai_san_ids = fields.One2many('tai_san', 'danh_muc_ts_id', string='Tài sản')