from odoo import models, fields, api

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = "full_name"
    
    ma_dinh_danh = fields.Char("Mã định danh", required=True)

    ho_va_dem_nv = fields.Char('Họ và đệm nhân viên', required=True)
    ten_nhan_vien = fields.Char("Tên nhân viên", required=True)

    full_name = fields.Char('Họ và tên đầy đủ', compute="_tinh_ho_va_ten", store=True)

    ngay_sinh = fields.Date("Ngày sinh", required=True)
    tuoi = fields.Char("Tuổi", compute='_compute_tuoi', store=True)
    
    que_quan = fields.Char("Quê quán", required=True)
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại", required=True)

    lich_su_cong_tac_ids = fields.One2many("lich_su_cong_tac", "nhan_vien_id", string="Lịch sử công tác")

    @api.depends("ho_va_dem_nv", "ten_nhan_vien")
    def _tinh_ho_va_ten(self):
        for record in self:
            if record.ho_va_dem_nv and record.ten_nhan_vien:
                record.full_name = record.ho_va_dem_nv + " " + record.ten_nhan_vien

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                record.tuoi = str((fields.Date.today() - record.ngay_sinh).days // 365) + " tuổi"