from odoo import _, api, fields, models

class thanh_ly_tai_san(models.Model):
    _name = 'thanh_ly_tai_san'
    _description = 'Bảng chứa thông tin Thanh lý tài sản'

    hanh_dong = fields.Selection([
        ('ban', 'Bán'),
        ('huy', 'Tiêu hủy')
    ], string='Hành động', required=True)
    ngay_thanh_ly = fields.Date('Ngày thanh lý', required=True, default=fields.Date.today)
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True)
    so_luong = fields.Integer('Số lượng', required=True)
    ghi_chu = fields.Char('Ghi chú', default='')