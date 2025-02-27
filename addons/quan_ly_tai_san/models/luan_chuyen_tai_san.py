from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class LuanChuyenTaiSan(models.Model):
    _name = 'luan_chuyen_tai_san'
    _description = 'Bảng chứa thông tin Luân chuyển tài sản'

    ma_phieu_luan_chuyen = fields.Char('Mã phiếu',default='LCTS-', required=True)
    bo_phan_nguon = fields.Many2one('phong_ban', string='Bộ phận hiện tại', required=True)
    bo_phan_dich = fields.Many2one('phong_ban', string='Bộ phận nhận', required=True)
    thoi_gian_luan_chuyen = fields.Datetime('Thời gian luân chuyển', required=True, default=fields.Datetime.now)
    ghi_chu = fields.Char('Lý do luân chuyển', default='', required=True)

    luan_chuyen_line_ids = fields.One2many('luan_chuyen_tai_san_line', 'luan_chuyen_id', string='Danh sách tài sản')

    @api.onchange('bo_phan_nguon')
    def _onchange_bo_phan_nguon(self):
        if self.bo_phan_nguon:
            self.luan_chuyen_line_ids = [(5, 0, 0)]  
    
    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for record in records:
            if record.luan_chuyen_line_ids:
                for line in record.luan_chuyen_line_ids:
                    phan_bo_tai_san = line.phan_bo_tai_san_id
                    phan_bo_tai_san.so_luong -= line.so_luong
                    self.env['phan_bo_tai_san'].create({
                        'phong_ban_id': record.bo_phan_dich.id,
                        'tai_san_id': line.phan_bo_tai_san_id.tai_san_id.id,
                        'ngay_phat': fields.Date.today(),
                        'so_luong': line.so_luong,
                        'trang_thai': 'in-use',
                        'vi_tri_tai_san_id': record.bo_phan_dich.id,
                        'ghi_chu': f"Lưu ý: Phiếu lưu chuyển {record.ma_phieu_luan_chuyen}"
                    })
        return records