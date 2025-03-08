from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class DonMuonTaiSan(models.Model):
    _name = 'don_muon_tai_san'
    _description = 'Bảng chứa thông tin Đơn mượn tài sản'
    _rec_name = "ten_don_muon"

    ten_don_muon = fields.Char('Đơn mượn tài sản', required=True)
    phong_ban_cho_muon_id = fields.Many2one('phong_ban', string='Phòng ban cho mượn', required=True, ondelete='restrict')
    thoi_gian_muon = fields.Datetime('Thời gian mượn', required=True, default=lambda self: fields.Datetime.now())
    thoi_gian_tra = fields.Datetime('Thời gian trả', required=True)
    nhan_vien_muon_id = fields.Many2one('nhan_vien', string='Nhân viên mượn tài sản', required=True, ondelete='restrict')
    
    ly_do = fields.Char('Lý do mượn tài sản', required=True)
    
    don_muon_tai_san_ids = fields.One2many('don_muon_tai_san_line', 'don_muon_id', string='Danh sách tài sản yêu cầu')
    ds_tai_san_chua_muon = fields.Many2many('phan_bo_tai_san', compute='_compute_ds_tai_san_chua_muon', string="Tài sản chưa mượn")

    @api.depends('phong_ban_cho_muon_id', 'don_muon_tai_san_ids')
    def _compute_ds_tai_san_chua_muon(self):
        for record in self:
            da_muon_ids = record.don_muon_tai_san_ids.mapped('phan_bo_tai_san_id').ids
            ds_tai_san = self.env['phan_bo_tai_san'].search([
                ('phong_ban_id', '=', record.phong_ban_cho_muon_id.id),
                ('id', 'not in', da_muon_ids)
            ])
            record.ds_tai_san_chua_muon = ds_tai_san

    trang_thai = fields.Selection([
        ('dang-cho', 'Đang chờ'),
        ('da-duyet', 'Đã duyệt'),
        ('da-huy', 'Đã hủy')
    ], string='Trạng thái', required=True, default='dang-cho')

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
    