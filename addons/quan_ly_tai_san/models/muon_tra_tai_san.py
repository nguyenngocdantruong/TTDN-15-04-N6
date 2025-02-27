from odoo import _, api, fields, models

class MuonTraTaiSan(models.Model):
    _name = 'muon_tra_tai_san'
    _description = 'Bảng chứa thông tin Mượn trả tài sản'
    _rec_name = "ma_phieu_muon_tra"
    _sql_constraints = [
        ("ma_phieu_muon_tra_unique", "unique(ma_phieu_muon_tra)", "Mã phiếu mượn trả đã tồn tại !"),
    ]

    ma_phieu_muon_tra = fields.Char('Mã phiếu', default='MTTS-', required=True)
    ten_phieu_muon_tra = fields.Char('Tên phiếu', required=True)
    phong_ban_muon_id = fields.Many2one('phong_ban', string='Phòng ban mượn')
    phong_ban_cho_muon_id = fields.Many2one('phong_ban', string='Phòng ban cho mượn', required=True)
    ngay_muon = fields.Date('Ngày mượn', required=True, default=fields.Date.today)
    ngay_tra = fields.Date('Ngày trả', required=True)
    nhan_vien_muon_id = fields.Many2one('nhan_vien', string='Nhân viên mượn', required=True)
    
    ghi_chu = fields.Char('Ghi chú', default='')
    
    muon_tra_line_ids = fields.One2many('muon_tra_tai_san_line', 'muon_tra_id', string='Danh sách tài sản')

    trang_thai = fields.Selection([
        ('dang-muon', 'Đang mượn'),
        ('da-tra', 'Đã trả')
    ], string='Trạng thái', required=True, default='dang-muon')

    tinh_trang = fields.Char(compute='_compute_tinh_trang', string='Trạng thái', store=True)
    
    @api.depends('trang_thai', 'ngay_muon', 'ngay_tra')
    def _compute_tinh_trang(self):
        for record in self:
            if record.trang_thai == 'da-tra':
                record.tinh_trang = 'Đang mượn'
                return
            if record.ngay_muon <= fields.Date.today() <= record.ngay_tra:
                record.tinh_trang = 'Đang mượn'
            elif fields.Date.today() > record.ngay_tra:
                record.tinh_trang = 'Quá hạn'
    
    @api.onchange('phong_ban_muon_id')
    def _onchange_phong_ban_muon_id(self):
        for record in self:
            record.muon_tra_line_ids = [(5, 0, 0)]
    