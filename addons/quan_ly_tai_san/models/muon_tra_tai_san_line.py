from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class MuonTraTaiSanLine(models.Model):
    _name = 'muon_tra_tai_san_line'
    _description = 'Chi tiết mượn trả tài sản'

    muon_tra_id = fields.Many2one('muon_tra_tai_san', string='Phiếu mượn trả', required=True, ondelete='cascade')
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True, ondelete='cascade')
    so_luong = fields.Integer('Số lượng', required=True)
    ghi_chu = fields.Char('Ghi chú', default='')

    @api.constrains('so_luong')
    def _constrains_so_luong(self):
        for record in self:
            if record.so_luong <= 0:
                raise ValidationError("Số lượng phải lớn hơn 0")
            if record.so_luong > record.phan_bo_tai_san_id.so_luong:
                raise ValidationError("Số lượng mượn không thể lớn hơn số lượng hiện có")
