from odoo import _, api, fields, models

class LichSuKhauHao(models.Model):
    _name = 'lich_su_khau_hao'
    _description = 'lich_su_khau_hao'
    
    ma_phieu_khau_hao = fields.Char('Mã phiếu', required=True)
    ma_ts = fields.Many2one('tai_san', string='Mã tài sản', required=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng ban sở hữu', required=True)
    ngay_khau_hao = fields.Date('Ngày khấu hao', required=True)
    so_tien_khau_hao = fields.Float('Số tiền khấu hao', required=True)
    gia_tri_con_lai = fields.Float('Giá trị còn lại', required=True)
    loai_phieu = fields.Selection([
        ('automatic', 'Tự động'),
        ('manual', 'Thủ công')
    ], string='Phương thức', required=True)
    ghi_chu = fields.Char('Ghi chú')