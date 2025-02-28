from odoo import _, api, fields, models

class KiemKeTaiSanLine(models.Model):
    _name = 'kiem_ke_tai_san_line'
    _description = 'Bảng chứa thông tin phiếu kiểm kê tài sản'

    kiem_ke_tai_san_id = fields.Many2one('kiem_ke_tai_san', string='Phiếu kiểm kê', required=True, ondelete='cascade')
    phan_bo_tai_san_id = fields.Many2one('phan_bo_tai_san', string='Tài sản', required=True, ondelete='cascade')
    so_luong_thuc_te = fields.Integer('SL thực tế', required=True)
    so_luong_ly_thuyet = fields.Integer('SL lý thuyết', default = 1, readonly=True)
    dvt = fields.Char('Đơn vị tính', related='phan_bo_tai_san_id.tai_san_id.don_vi_tinh', store=True)
    trang_thai = fields.Selection([
        ('not-finished', 'Chưa kiểm kê'),
        ('finished', 'Đã kiểm kê')
    ], string='Trạng thái', default='not-finished', required=True)
    trang_thai_tai_san = fields.Selection([
        ('good', 'Tốt'),
        ('broken', 'Hỏng'),
        ('lost', 'Mất')
    ], string='Tình trạng tài sản', default='good', required=True)
    ghi_chu = fields.Char('Ghi chú', default='')
    