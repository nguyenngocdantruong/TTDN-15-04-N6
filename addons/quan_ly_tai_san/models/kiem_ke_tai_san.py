from odoo import _, api, fields, models

class KiemKeTaiSan(models.Model):
    _name = 'kiem_ke_tai_san'
    _description = 'Bảng chứa thông tin Kiểm kê tài sản'

    ma_phieu_kiem_ke = fields.Char('Mã phiếu', required=True)
    ten_phieu_kiem_ke = fields.Char('Tên phiếu', required=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Bộ phận muốn kiểm kê', required=True)
    nhan_vien_kiem_ke_id = fields.Many2one('nhan_vien', string='Nhân viên kiểm kê', required=True)
    ds_kiem_ke_ids = fields.One2many(comodel_name='kiem_ke_tai_san_line', 
                                     inverse_name='kiem_ke_tai_san_id', 
                                     string ='Danh sách kiểm kê')
    ngay_kiem_ke = fields.Date('Ngày kiểm kê', required=True, default=fields.Date.today)
    ghi_chu = fields.Char('Ghi chú', default='')

    