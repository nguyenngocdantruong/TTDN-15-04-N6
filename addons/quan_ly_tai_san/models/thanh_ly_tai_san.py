from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ThanhLyTaiSan(models.Model):
    _name = 'thanh_ly_tai_san'
    _description = 'Bảng chứa thông tin Thanh lý tài sản'
    _rec_name = 'ma_thanh_ly'
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
    gia_ban = fields.Float('Giá bán', required=True)
    gia_goc = fields.Float('Giá gốc', compute='_compute_gia_goc', store=True)
                                         
    @api.constrains('gia_ban')
    def _constrains_gia_ban(self):
        for record in self:
            if record.gia_ban < 0:
                raise ValidationError("Giá bán không thể nhỏ hơn 0")
    
    @api.depends('tai_san_id')
    def _compute_gia_goc(self):
        for record in self:
            if record.tai_san_id:
                record.gia_goc = record.tai_san_id.gia_tri_ban_dau
                
    @api.constrains('tai_san_id')
    def _check_tai_san_thanh_ly_once(self):
        for record in self:
            existing_thanh_ly = self.env['thanh_ly_tai_san'].search([
                ('tai_san_id', '=', record.tai_san_id.id),
                ('id', '!=', record.id)
            ])
            if existing_thanh_ly:
                raise ValidationError(_(f"Tài sản '{record.tai_san_id.ten_tai_san}' đã được thanh lý trước đó!"))
