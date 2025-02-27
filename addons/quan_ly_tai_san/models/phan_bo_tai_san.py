from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    
    @api.constrains("so_luong")
    def _check_so_luong(self):
        for record in self:
            so_luong_hien_co = record.tai_san_id.so_luong_tong
            if record.so_luong <= 0:
                raise ValidationError("Số lượng phải lớn hơn 0!")
            elif record.so_luong > so_luong_hien_co:
                msg = f"Số lượng nhập không được lớn hơn số lượng hiện có ({so_luong_hien_co})"
                raise ValidationError(msg)

    @api.onchange('tai_san_id')
    def _onchange_tai_san_id(self):
        for record in self:
            record.so_luong = 0

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            tai_san_id = val.get('tai_san_id')
            so_luong = val.get('so_luong')
            if not tai_san_id:
                continue
            tai_san = self.env['tai_san'].browse(tai_san_id)
            tai_san.so_luong_tong -= so_luong
        return super().create(vals)    
    
    