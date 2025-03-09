from odoo import _, api, fields, models

class LichSuKyThuat(models.Model):
    _name = 'lich_su_ky_thuat'
    _description = 'Bảng chứa thông tin về lịch sử kỹ thuật của tài sản (đang hỏng cái gì, vỡ góc này, méo góc kia,…) + date'
    
    tai_san_id = fields.Many2one('tai_san', string='Tài sản', ondelete='cascade')
    noi_dung = fields.Char('Nội dung', required=True)
    ngay = fields.Date('Ngày', required=True, default= lambda self: fields.Date.today())
    ghi_chu = fields.Char('Ghi chú', default='')
    