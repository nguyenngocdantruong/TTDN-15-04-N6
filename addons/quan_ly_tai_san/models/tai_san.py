from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = 'cus_rec_name'


    ma_tai_san = fields.Char('Mã tài sản', required=True)
    ten_tai_san = fields.Char('Tên tài sản', required=True)
    ngay_mua_ts = fields.Date('Ngày mua tài sản')
    don_vi_tien_te = fields.Selection([
        ('vnd', 'VNĐ'),
        ('usd', '$'),
    ], string='Đơn vị tiền tệ', default='vnd', required=True)
    gia_tri_ban_dau = fields.Float('Giá trị ban đầu')
    gia_tri_hien_tai = fields.Float('Giá trị hiện tại')
    danh_muc_ts_id = fields.Many2one('danh_muc_tai_san', string='Danh mục tài sản', ondelete='restrict')

    so_luong_tong = fields.Integer('Số lượng hiện có', default=1)

    pp_khau_hao = fields.Selection([
        ('straight-line', 'Tuyến tính'),
        ('degressive', 'Giảm dần'),
        ('none', 'Không')
    ], string='Phương pháp khấu hao', default = 'none', required=True)
    thoi_gian_su_dung = fields.Integer('Thời gian đã sử dụng (năm)', default=0)

    # Khấu hao tuyến tính
    thoi_gian_toi_da = fields.Integer('Thời gian sử dụng còn lại tối đa (năm)', default=5)

    # Khấu hao giảm dần
    ty_le_khau_hao = fields.Float('Tỷ lệ khấu hao (%)', default=20)

    don_vi_tinh = fields.Char('Đơn vị tính')
    ghi_chu = fields.Char('Ghi chú')

    cus_rec_name = fields.Char('Tên tài sản', compute='_compute_cus_rec_name', store=True)
    @api.depends('ten_tai_san', 'ma_tai_san')
    def _compute_cus_rec_name(self):
        for record in self:
            record.cus_rec_name = record.ma_tai_san + ' - ' + record.ten_tai_san

    phong_ban_su_dung_ids = fields.One2many('phan_bo_tai_san', 'tai_san_id', string='Phòng ban sử dụng')
    lich_su_khau_hao_ids = fields.One2many('lich_su_khau_hao', 'ma_ts', string='Lịch sử khấu hao')

    def action_tinh_khau_hao(self):
        for record in self:
            if record.gia_tri_hien_tai <= 0:
                raise ValidationError("Giá trị hiện tại phải lớn hơn 0 !")
            if record.pp_khau_hao == 'none':
                raise ValidationError("Tài sản này không có phương pháp khấu hao!")

            so_tien_khau_hao = 0

            if record.pp_khau_hao == 'straight-line':  
                if record.thoi_gian_toi_da <= 0:
                    raise ValidationError("Thời gian sử dụng tối đa phải lớn hơn 0 (năm) !")
                so_tien_khau_hao = record.gia_tri_ban_dau / record.thoi_gian_toi_da  

            elif record.pp_khau_hao == 'degressive':  
                if record.ty_le_khau_hao <= 0 or record.ty_le_khau_hao >= 100:
                    raise ValidationError("Tỷ lệ khấu hao phải nằm trong khoảng (0,100) !")
                so_tien_khau_hao = record.gia_tri_hien_tai * (record.ty_le_khau_hao / 100) 

            so_tien_khau_hao = min(so_tien_khau_hao, record.gia_tri_hien_tai)  
            ma_phieu_khau_hao = 'KH' + record.ma_tai_san + '-' + datetime.now().strftime('%Y%m%d%H%M%S%f')


            self.env['lich_su_khau_hao'].create({
                'ma_phieu_khau_hao': ma_phieu_khau_hao,
                'ma_ts': record.id,
                'ngay_khau_hao': fields.Date.today(),
                'so_tien_khau_hao': so_tien_khau_hao,
                'gia_tri_con_lai': record.gia_tri_hien_tai,
                'loai_phieu': 'automatic',
                'ghi_chu': f'Khấu hao tự động ngày {fields.Date.today()}'
            })

            self.env['bus.bus']._sendone(
                self.env.user.partner_id, 
                'simple_notification', 
                {
                    'title': 'Thành công',
                    'message': f'Khấu hao tài sản "{record.ten_tai_san}" thành công!',
                    'sticky': False,  
                    'type': 'success'  
                }
            )

