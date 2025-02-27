from odoo import _, api, fields, models

class MuonTraTaiSanLine(models.Model):
    _name = 'muon_tra_tai_san_line'
    _description = 'Chi tiết mượn trả tài sản'

    muon_tra_id = fields.Many2one('muon_tra_tai_san', string='Phiếu mượn trả', required=True)
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True)
    so_luong = fields.Integer('Số lượng', required=True)

