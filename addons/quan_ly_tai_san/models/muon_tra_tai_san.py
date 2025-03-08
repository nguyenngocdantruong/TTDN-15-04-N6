from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class MuonTraTaiSan(models.Model):
    _name = 'muon_tra_tai_san'
    _description = 'Bảng chứa thông tin Mượn trả tài sản'
    _rec_name = "ma_phieu_muon_tra"
    _order = "thoi_gian_muon desc"
    _sql_constraints = [
        ("ma_phieu_muon_tra_unique", "unique(ma_phieu_muon_tra)", "Mã phiếu mượn trả đã tồn tại !"),
    ]

    ma_don_muon_id = fields.Many2one('don_muon_tai_san', string='Duyệt từ mã đơn mượn', ondelete='cascade')

    ma_phieu_muon_tra = fields.Char('Mã phiếu', default='MTTS-', required=True)
    ten_phieu_muon_tra = fields.Char('Tên phiếu', required=True)
    phong_ban_cho_muon_id = fields.Many2one('phong_ban', string='Phòng ban cho mượn', required=True, ondelete='restrict')
    thoi_gian_muon = fields.Datetime('Thời gian mượn', required=True, default=lambda self: fields.Datetime.now())
    thoi_gian_tra = fields.Datetime('Thời gian trả', required=True, default=lambda self: fields.Datetime.now())
    nhan_vien_muon_id = fields.Many2one('nhan_vien', string='Nhân viên mượn', required=True, ondelete='restrict')
    
    ghi_chu = fields.Char('Ghi chú', default='')

    trang_thai = fields.Selection([
        ('dang-muon', 'Đang mượn'),
        ('da-tra', 'Đã trả')
    ], string='Trạng thái', required=True, default='dang-muon')

    tinh_trang = fields.Char(compute='_compute_tinh_trang')
    
    muon_tra_line_ids = fields.One2many('muon_tra_tai_san_line', 'muon_tra_id', string='Danh sách tài sản')
    ds_tai_san_chua_muon = fields.Many2many('phan_bo_tai_san', compute='_compute_ds_tai_san_chua_muon', string="Tài sản chưa mượn")

    @api.onchange('ma_don_muon_id')
    def _onchange_ma_don_muon_id(self):
        if self.ma_don_muon_id:
            don_muon = self.ma_don_muon_id
            self.phong_ban_cho_muon_id = don_muon.phong_ban_cho_muon_id
            self.thoi_gian_muon = don_muon.thoi_gian_muon
            self.thoi_gian_tra = don_muon.thoi_gian_tra
            self.nhan_vien_muon_id = don_muon.nhan_vien_muon_id
            self.ten_phieu_muon_tra = "Duyệt đơn mượn: " + str(don_muon.ten_don_muon)
            self.ma_phieu_muon_tra = "MTTS-" + str(don_muon.ten_don_muon) + str(fields.Datetime.now())

            # Lấy danh sách tài sản từ đơn mượn
            muon_tra_lines = []
            for line in don_muon.don_muon_tai_san_ids:
                muon_tra_lines.append((0, 0, {
                    'phan_bo_tai_san_id': line.phan_bo_tai_san_id.id,
                    'ghi_chu': line.ghi_chu
                }))

            self.muon_tra_line_ids = muon_tra_lines

    @api.model
    def create(self, vals):
        record = super(MuonTraTaiSan, self).create(vals)
        if record.ma_don_muon_id:
            record.ma_don_muon_id.trang_thai = 'da-duyet'
        return record
    
    @api.model
    def write(self, vals):
        res = super(MuonTraTaiSan, self).write(vals)
        for record in self:
            if record.ma_don_muon_id:
                record.ma_don_muon_id.trang_thai = 'da-duyet'
        return res


    @api.depends('phong_ban_cho_muon_id', 'muon_tra_line_ids')
    def _compute_ds_tai_san_chua_muon(self):
        for record in self:
            da_muon_ids = record.muon_tra_line_ids.mapped('phan_bo_tai_san_id').ids
            ds_tai_san = self.env['phan_bo_tai_san'].search([
                ('phong_ban_id', '=', record.phong_ban_cho_muon_id.id),
                ('id', 'not in', da_muon_ids)
            ])
            record.ds_tai_san_chua_muon = ds_tai_san

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
            elif record.thoi_gian_muon and record.thoi_gian_tra:
                now = fields.Datetime.now()
                if record.thoi_gian_muon <= now and now <= record.thoi_gian_tra:
                    record.tinh_trang = 'Đang mượn'
                elif now > record.thoi_gian_tra:
                    record.tinh_trang = 'Quá hạn'
                else:
                    record.tinh_trang = 'Chưa tới hạn'
            else:
                record.tinh_trang = 'Không xác định'  # Tránh lỗi nếu có dữ liệu thiếu
