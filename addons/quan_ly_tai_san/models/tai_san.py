from odoo import _, api, fields, models

class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng chứa thông tin tài sản'

    ma_tai_san = fields.Char('Mã tài sản', required=True)
    ten_tai_san = fields.Char('Tên tài sản', required=True)
    ngay_mua_ts = fields.Date('Ngày mua tài sản')
    gia_tri_ban_dau = fields.Float('Giá trị ban đầu')
    gia_tri_hien_tai = fields.Float('Giá trị hiện tại')
    danh_muc_ts_id = fields.Many2one('danh_muc_tai_san', string='Danh mục tài sản', ondelete='restrict')

    pp_khau_hao = fields.Selection([
        ('straight-line', 'Tuyến tính'),
        ('degressive', 'Giảm dần'),
        ('units-of-production', 'Đơn vị sản xuất'),
        ('none', 'Không')
    ], string='Phương pháp khấu hao', default = 'none', required=True)

    ngay_bat_dau_khau_hao = fields.Date('Ngày bắt đầu khấu hao')
    trang_thai = fields.Selection([
        ('new', 'Mới'),
        ('in-use', 'Đang sử dụng'),
        ('broken', 'Hỏng'),
        ('lost', 'Mất'),
        ('disposed', 'Thanh lý')
    ], string='Trạng thái', required=True, default='new')
    ghi_chu = fields.Char('Ghi chú')