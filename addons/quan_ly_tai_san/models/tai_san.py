from odoo import _, api, fields, models

class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = 'cus_rec_name'


    ma_tai_san = fields.Char('Mã tài sản', required=True)
    ten_tai_san = fields.Char('Tên tài sản', required=True)
    ngay_mua_ts = fields.Date('Ngày mua tài sản')
    gia_tri_ban_dau = fields.Float('Giá trị ban đầu')
    gia_tri_hien_tai = fields.Float('Giá trị hiện tại')
    danh_muc_ts_id = fields.Many2one('danh_muc_tai_san', string='Danh mục tài sản', ondelete='restrict')

    so_luong_tong = fields.Integer('Số lượng hiện có', default=1)

    pp_khau_hao = fields.Selection([
        ('straight-line', 'Tuyến tính'),
        ('degressive', 'Giảm dần'),
        ('units-of-production', 'Đơn vị sản xuất'),
        ('none', 'Không')
    ], string='Phương pháp khấu hao', default = 'none', required=True)

    ngay_bat_dau_khau_hao = fields.Date('Ngày bắt đầu khấu hao')
    don_vi_tinh = fields.Char('Đơn vị tính')
    ghi_chu = fields.Char('Ghi chú')

    cus_rec_name = fields.Char('Tên tài sản', compute='_compute_cus_rec_name', store=True)
    @api.depends('ten_tai_san', 'ma_tai_san')
    def _compute_cus_rec_name(self):
        for record in self:
            record.cus_rec_name = record.ma_tai_san + ' - ' + record.ten_tai_san

    phong_ban_su_dung_ids = fields.One2many('phan_bo_tai_san', 'tai_san_id', string='Phòng ban sử dụng')
    lich_su_khau_hao_ids = fields.One2many('lich_su_khau_hao', 'ma_ts', string='Lịch sử khấu hao')