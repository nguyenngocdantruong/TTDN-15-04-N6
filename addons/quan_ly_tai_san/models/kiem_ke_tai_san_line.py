from odoo import _, api, fields, models

class KiemKeTaiSanLine(models.Model):
    _name = 'kiem_ke_tai_san_line'
    _description = 'Bảng chứa thông tin phiếu kiểm kê tài sản'

    kiem_ke_tai_san_id = fields.Many2one('kiem_ke_tai_san', string='Phiếu kiểm kê', required=True)
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True, ondelete='cascade')
    so_luong_thuc_te = fields.Integer('SL thực tế', required=True)
    so_luong_ly_thuyet = fields.Integer('SL lý thuyết', compute='_compute_so_luong_ly_thuyet', store=True)
    dvt = fields.Char('Đơn vị tính', compute='_compute_dvt', store=True)
    trang_thai = fields.Selection([
        ('not-finished', 'Chưa kiểm kê'),
        ('finished', 'Đã kiểm kê')
    ], string='Trạng thái', default='not-finished', required=True)

    @api.depends('phan_bo_tai_san_id')
    def _compute_so_luong_ly_thuyet(self):
        for record in self:
            record.so_luong_ly_thuyet = record.phan_bo_tai_san_id.so_luong if record.phan_bo_tai_san_id else 0

    @api.depends('phan_bo_tai_san_id')
    def _compute_dvt(self):
        for record in self:
            record.dvt = record.phan_bo_tai_san_id.tai_san_id.don_vi_tinh if record.phan_bo_tai_san_id else ''
    ghi_chu = fields.Char('Ghi chú', default='')
    