from odoo import _, api, fields, models

class KiemKeTaiSan(models.Model):
    _name = 'kiem_ke_tai_san'
    _description = 'Bảng chứa thông tin Kiểm kê tài sản'
    _rec_name = 'ma_phieu_kiem_ke'
    _order = 'thoi_gian_tao desc'

    ma_phieu_kiem_ke = fields.Char('Mã phiếu', required=True)
    ten_phieu_kiem_ke = fields.Char('Tên phiếu', required=True)
    phong_ban_id = fields.Many2one('phong_ban', string='Bộ phận muốn kiểm kê', required=True)
    nhan_vien_kiem_ke_id = fields.Many2one('nhan_vien', string='Nhân viên kiểm kê', required=True)
    ds_kiem_ke_ids = fields.One2many(comodel_name='kiem_ke_tai_san_line', 
                                     inverse_name='kiem_ke_tai_san_id', 
                                     string ='Danh sách kiểm kê')
    thoi_gian_tao = fields.Datetime('Thời gian tạo phiếu', default=fields.Datetime.now)
    ghi_chu = fields.Char('Ghi chú', default='')

    @api.onchange('phong_ban_id')
    def _onchange_phong_ban_id(self):
        if self.phong_ban_id:
            self.ds_kiem_ke_ids = [(5, 0, 0)]  # Xóa hết danh sách kiểm kê
    