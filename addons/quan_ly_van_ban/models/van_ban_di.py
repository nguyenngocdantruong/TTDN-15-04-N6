from odoo import models, fields, api


class VanBanDi(models.Model):
    _name = 'van_ban_di'
    _description = 'Bảng chứa thông tin văn bản đi'
    _rec_name = "ten_van_ban"

    ten_van_ban = fields.Char("Tên văn bản", required=True)
    ngay_ban_hanh = fields.Date("Ngày ban hành")
    ngay_ky_vb = fields.Date("Ngày ký văn bản")
    ngay_het_han = fields.Date("Ngay het han vb")
    ma_vb = fields.Char("Ma van ban")

    nhan_vien = fields.Char("Nhân viên")
