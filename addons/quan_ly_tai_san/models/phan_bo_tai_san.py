from odoo import _, api, fields, models

class PhanBoTaiSan(models.Model):
    _name = 'phan_bo_tai_san'
    _description = 'Bảng chứa thông tin Phân bổ tài sản'
    _rec_name = "custom_name"

    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban', required=True)
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', required=True)
    ngay_phat = fields.Date('Ngày phân bổ', required=True, default=fields.Date.today)
    so_luong = fields.Integer('Số lượng', required=True)
    ghi_chu = fields.Char('Ghi chú', default='')
    trang_thai = fields.Selection([
        ('in-use', 'Đang sử dụng'),
        ('not-in-use', 'Không sử dụng')
    ], string='Trạng thái', required=True, default='in-use')
    vi_tri_tai_san_id = fields.Many2one('phong_ban', string='Vị trí tài sản')

    custom_name = fields.Char(compute="_compute_custom_name", store=True, string="Tên hiển thị")

    @api.depends('phong_ban_id', 'tai_san_id')
    def _compute_custom_name(self):
        for record in self:
            phong_ban_code = record.phong_ban_id.ma_phong_ban or 'Mã phòng ban không xác định'
            tai_san_name = record.tai_san_id.ten_tai_san or 'Tài sản không xác định'
            record.custom_name = f"{phong_ban_code} - {tai_san_name}"
    