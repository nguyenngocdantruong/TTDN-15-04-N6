from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class LuanChuyenTaiSanLine(models.Model):
    _name = 'luan_chuyen_tai_san_line'
    _description = 'Chi tiết luân chuyển tài sản'

    luan_chuyen_id = fields.Many2one('luan_chuyen_tai_san', string='Luân chuyển tài sản', required=True, ondelete='cascade')
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True, ondelete='cascade')
    so_luong = fields.Integer('Số lượng luân chuyển', default = 1, readonly=True)
    ghi_chu = fields.Char('Ghi chú', default='')

    @api.constrains('so_luong')
    def _constrains_so_luong(self):
        for rec in self:
            if rec.so_luong <= 0:
                raise ValidationError('Số lượng phải lớn hơn 0!')
            if rec.so_luong > rec.phan_bo_tai_san_id.so_luong:
                raise ValidationError(f'Số lượng luân chuyển không được lớn hơn số lượng tài sản được phân bổ ({rec.phan_bo_tai_san_id.so_luong}) !')