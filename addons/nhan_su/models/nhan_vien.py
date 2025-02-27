from odoo import models, fields, api

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = "ten_nhan_vien"

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ten_nhan_vien = fields.Char("Tên nhân viên", required=True)
    ngay_sinh = fields.Date("Ngày sinh", required=True)
    que_quan = fields.Char("Quê quán", required=True)
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại", required=True)

    lich_su_cong_tac_ids = fields.One2many("lich_su_cong_tac", "nhan_vien_id", string="Lịch sử công tác")
    tuoi = fields.Char(compute='_compute_tuoi', string='Tuổi', store=True)
    
    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                record.tuoi = (fields.Date.today() - record.ngay_sinh).days // 365
