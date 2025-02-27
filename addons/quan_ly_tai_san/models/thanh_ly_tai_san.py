from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ThanhLyTaiSan(models.Model):
    _name = 'thanh_ly_tai_san'
    _description = 'Bảng chứa thông tin Thanh lý tài sản'
    _sql_constraints = [
        ("ma_thanh_ly_unique", "unique(ma_thanh_ly)", "Mã thanh lý đã tồn tại"),
    ]

    ma_thanh_ly = fields.Char('Mã thanh lý', required=True, default='TL-')
    hanh_dong = fields.Selection([
        ('ban', 'Bán'),
        ('huy', 'Tiêu hủy')
    ], string='Hành động', required=True)
    tai_san_id = fields.Many2one('tai_san', 'Tài sản', required=True, ondelete='cascade')
    nguoi_thanh_ly_id = fields.Many2one('nhan_vien', 'Người thực hiện', required=True)
    thoi_gian_thanh_ly = fields.Datetime('Thời gian thanh lý', required=True, default=fields.Datetime.now)
    ly_do_thanh_ly = fields.Char('Lý do thanh lý', default='')
    so_luong = fields.Integer('Số lượng', required=True)
    gia_ban = fields.Float('Giá bán', required=True)
    tong_gia_tri = fields.Float('Tổng giá trị', compute='_compute_tong_gia_tri', store=True)
    gia_goc = fields.Float('Giá gốc', compute='_compute_gia_goc', store=True)
                                         
    @api.constrains('so_luong')
    def _constrains_so_luong(self):
        for record in self:
            if record.so_luong <= 0:
                raise ValidationError("Số lượng phải lớn hơn 0")
            if record.so_luong > record.tai_san_id.so_luong_tong:
                raise ValidationError("Số lượng thanh lý không thể lớn hơn số lượng hiện có")

    @api.constrains('gia_ban')
    def _constrains_gia_ban(self):
        for record in self:
            if record.gia_ban < 0:
                raise ValidationError("Giá bán không thể nhỏ hơn 0")
            if record.gia_ban > record.gia_goc:
                raise ValidationError("Giá bán không thể lớn hơn giá trị hiện tại của tài sản")

    @api.depends('gia_ban', 'so_luong')
    def _compute_tong_gia_tri(self):
        for record in self:
            if record.gia_ban < 0:
                raise ValidationError("Giá bán không thể nhỏ hơn 0")
            record.tong_gia_tri = record.gia_ban * record.so_luong
    
    @api.depends('tai_san_id')
    def _compute_gia_goc(self):
        for record in self:
            if record.tai_san_id:
                record.gia_goc = record.tai_san_id.gia_tri_ban_dau

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for record in records:
            if record.tai_san_id:
                tai_san = record.tai_san_id
                tai_san.so_luong_tong -= record.so_luong
        return records