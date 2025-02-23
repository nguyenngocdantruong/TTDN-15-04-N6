from odoo import _, api, fields, models

class NhanSu(models.Model):
    _name = 'nhan_su'
    _description = 'Bảng chứa thông tin Nhân sự'
    _rec_name = "ten_nhan_su"

    ma_nhan_su = fields.Char('Mã nhân sự', required=True)
    ten_nhan_su = fields.Char('Tên nhân sự', required=True)
    ngay_sinh = fields.Date('Ngày sinh', required=True)
    email = fields.Char('Email', required=True)
    dia_chi = fields.Char('Địa chỉ', required=True)
    so_dien_thoai = fields.Char('Số điện thoại', required=True)
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác')
    ], string='Giới tính', required=True, default='nam')

    bo_phan_id = fields.Many2one('bo_phan_nhan_su', string='Bộ phận')
    chuc_vu_id = fields.Many2one('chuc_vu_nhan_su', string='Chức vụ')