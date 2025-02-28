from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class MuonTraTaiSan(models.Model):
    _name = 'muon_tra_tai_san'
    _description = 'Bảng chứa thông tin Mượn trả tài sản'
    _rec_name = "ma_phieu_muon_tra"
    _sql_constraints = [
        ("ma_phieu_muon_tra_unique", "unique(ma_phieu_muon_tra)", "Mã phiếu mượn trả đã tồn tại !"),
    ]

    ma_phieu_muon_tra = fields.Char('Mã phiếu', default='MTTS-', required=True)
    ten_phieu_muon_tra = fields.Char('Tên phiếu', required=True)
    phong_ban_cho_muon_id = fields.Many2one('phong_ban', string='Phòng ban cho mượn', required=True, ondelete='restrict')
    thoi_gian_muon = fields.Datetime('Thời gian mượn', required=True, default=lambda self: fields.Datetime.now())
    thoi_gian_tra = fields.Datetime('Thời gian trả', required=True)
    nhan_vien_muon_id = fields.Many2one('nhan_vien', string='Nhân viên mượn', required=True, ondelete='restrict')
    
    ghi_chu = fields.Char('Ghi chú', default='')
    
    muon_tra_line_ids = fields.One2many('muon_tra_tai_san_line', 'muon_tra_id', string='Danh sách tài sản')

    trang_thai = fields.Selection([
        ('dang-muon', 'Đang mượn'),
        ('da-tra', 'Đã trả')
    ], string='Trạng thái', required=True, default='dang-muon')

    tinh_trang = fields.Char(compute='_compute_tinh_trang', string='Trạng thái', store=True)

    @api.constrains('thoi_gian_muon')
    def _constrains_thoi_gian_muon_thoi_gian_tra(self):
        for record in self:
            if record.thoi_gian_muon > record.thoi_gian_tra:
                raise ValidationError("Thời gian mượn phải trước thời gian trả !")
    
    @api.constrains('thoi_gian_tra')
    def _constrains_thoi_gian_tra(self):
        for record in self:
            if record.thoi_gian_tra < fields.Datetime.now():
                raise ValidationError("Thời gian trả không được nhỏ hơn thời gian hiện tại !")
    
    @api.depends('trang_thai', 'thoi_gian_muon', 'thoi_gian_tra')
    def _compute_tinh_trang(self):
        for record in self:
            if record.trang_thai == 'da-tra':
                record.tinh_trang = 'Đã trả'
                return
            if record.thoi_gian_muon <= fields.Date.today() <= record.thoi_gian_tra:
                record.tinh_trang = 'Đang mượn'
            elif fields.Date.today() > record.thoi_gian_tra:
                record.tinh_trang = 'Quá hạn'