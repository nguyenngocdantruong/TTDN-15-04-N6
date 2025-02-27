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
    phong_ban_muon_id = fields.Many2one('phong_ban', string='Phòng ban mượn', ondelete='set null')
    phong_ban_cho_muon_id = fields.Many2one('phong_ban', string='Phòng ban cho mượn', required=True, ondelete='restrict')
    ngay_muon = fields.Date('Ngày mượn', required=True, default=fields.Date.today)
    ngay_tra = fields.Date('Ngày trả', required=True)
    nhan_vien_muon_id = fields.Many2one('nhan_vien', string='Nhân viên mượn', required=True, ondelete='restrict')
    
    ghi_chu = fields.Char('Ghi chú', default='')
    
    muon_tra_line_ids = fields.One2many('muon_tra_tai_san_line', 'muon_tra_id', string='Danh sách tài sản')

    trang_thai = fields.Selection([
        ('dang-muon', 'Đang mượn'),
        ('da-tra', 'Đã trả')
    ], string='Trạng thái', required=True, default='dang-muon')

    tinh_trang = fields.Char(compute='_compute_tinh_trang', string='Trạng thái', store=True)

    @api.constrains('ngay_muon')
    def _constrains_ngay_muon_ngay_tra(self):
        for record in self:
            if record.ngay_muon < fields.Date.today():
                raise ValidationError("Ngày mượn không được nhỏ hơn ngày hiện tại !")
            if record.ngay_muon > record.ngay_tra:
                raise ValidationError("Ngày mượn phải trước ngày trả !")
    
    @api.constrains('ngay_tra')
    def _constrains_ngay_tra(self):
        for record in self:
            if record.ngay_tra < fields.Date.today():
                raise ValidationError("Ngày trả không được nhỏ hơn ngày hiện tại !")
    
    @api.depends('trang_thai', 'ngay_muon', 'ngay_tra')
    def _compute_tinh_trang(self):
        for record in self:
            if record.trang_thai == 'da-tra':
                record.tinh_trang = 'Đã trả'
                return
            if record.ngay_muon <= fields.Date.today() <= record.ngay_tra:
                record.tinh_trang = 'Đang mượn'
            elif fields.Date.today() > record.ngay_tra:
                record.tinh_trang = 'Quá hạn'
    
    @api.onchange('phong_ban_muon_id')
    def _onchange_phong_ban_muon_id(self):
        for record in self:
            record.muon_tra_line_ids = [(5, 0, 0)]

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.tinh_trang == 'Đang mượn':
                for line in record.muon_tra_line_ids:
                    phan_bo_tai_san = line.phan_bo_tai_san_id
                    phan_bo_tai_san.so_luong -= line.so_luong
        return records

    def write(self, vals):
        for record in self:
            if 'muon_tra_line_ids' in vals or 'tinh_trang' in vals:
                if record.tinh_trang == 'Đang mượn':
                    for line in record.muon_tra_line_ids:
                        phan_bo_tai_san = line.phan_bo_tai_san_id
                        phan_bo_tai_san.so_luong += line.so_luong
        result = super().write(vals)
        for record in self:
            if record.tinh_trang == 'Đang mượn':
                for line in record.muon_tra_line_ids:
                    phan_bo_tai_san = line.phan_bo_tai_san_id
                    phan_bo_tai_san.so_luong -= line.so_luong
        return result

    def unlink(self):
        for record in self:
            if record.tinh_trang == 'Đang mượn':
                for line in record.muon_tra_line_ids:
                    phan_bo_tai_san = line.phan_bo_tai_san_id
                    phan_bo_tai_san.so_luong += line.so_luong
        return super().unlink()
    