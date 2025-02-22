from odoo import _, api, fields, models

class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng chứa thông tin tài sản'

    ma_tai_san = fields.Char('Mã tài sản', required=True)
    ten_tai_san = fields.Char('ten_tai_san', required=True)
    ngay_mua_ts = fields.Date('ngay_mua_ts')
    gia_tri_ban_dau = fields.Float('gia_tri_ban_dau')
    gia_tri_hien_tai = fields.Float('gia_tri_hien_tai')
    danh_muc_ts_id = fields.Many2one('danh_muc_tai_san', string='Danh mục tài sản')

    pp_khau_hao = fields.Selection([
        ('straight-line', 'Tuyến tính'),
        ('degressive', 'Giảm dần'),
        ('units-of-production', 'Đơn vị sản xuất'),
        ('none', 'Không')
    ], string='Phương pháp khấu hao', default = 'none')

    ngay_bat_dau_khau_hao = fields.Date('ngay_bat_dau_khau_hao')
    trang_thai = fields.Selection([
        ('new', 'Mới'),
        ('in-use', 'Đang sử dụng'),
        ('broken', 'Hỏng'),
        ('lost', 'Mất'),
        ('disposed', 'Thanh lý')
    ], string='trang_thai', required=True, default='new')
    ghi_chu = fields.Char('Ghi chú')