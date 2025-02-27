from odoo import _, api, fields, models

class LuanChuyenTaiSanLine(models.Model):
    _name = 'luan_chuyen_tai_san_line'
    _description = 'Chi tiết luân chuyển tài sản'

    luan_chuyen_id = fields.Many2one('luan_chuyen_tai_san', string='Luân chuyển tài sản', required=True)
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True)
    so_luong = fields.Integer('Số lượng luân chuyển', required=True)
    ghi_chu = fields.Char('Ghi chú', default='')