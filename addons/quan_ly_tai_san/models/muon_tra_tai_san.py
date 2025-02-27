from odoo import _, api, fields, models

class MuonTraTaiSan(models.Model):
    _name = 'muon_tra_tai_san'
    _description = 'Bảng chứa thông tin Mượn trả tài sản'

    ma_phieu_muon_tra = fields.Char('Mã phiếu', required=True)
    ten_phieu_muon_tra = fields.Char('Tên phiếu', required=True)
    phong_ban_muon_id = fields.Many2one('phong_ban', string='Phòng ban mượn', required=True)
    phong_ban_cho_muon_id = fields.Many2one('phong_ban', string='Phòng ban cho mượn', required=True)
    ngay_muon = fields.Date('Ngày mượn', required=True, default=fields.Date.today)
    ngay_tra = fields.Date('Ngày trả', required=True)
    nhan_vien_muon_id = fields.Many2one('nhan_vien', string='Nhân viên mượn', required=True)
    
    so_luong = fields.Integer('Số lượng', required=True)
    ghi_chu = fields.Char('Ghi chú', default='')
    
    muon_tra_line_ids = fields.One2many('muon_tra_tai_san_line', 'muon_tra_id', string='Danh sách tài sản')

    trang_thai = fields.Selection([
        ('dang-muon', 'Đang mượn'),
        ('da-tra', 'Đã trả')
    ], string='Trạng thái', required=True, default='dang-muon')
    
    