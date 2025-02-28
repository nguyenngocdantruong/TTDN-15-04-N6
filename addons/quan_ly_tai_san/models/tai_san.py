from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = 'cus_rec_name'
    _order = 'ngay_mua_ts desc'
    _sql_constraints = [
        ("ma_tai_san_unique", "unique(ma_tai_san)", "Mã tài sản đã tồn tại !"),
    ]


    ma_tai_san = fields.Char('Mã tài sản', required=True)
    ten_tai_san = fields.Char('Tên tài sản', required=True)
    ngay_mua_ts = fields.Date('Ngày mua tài sản', required=True)
    don_vi_tien_te = fields.Selection([
        ('vnd', 'VNĐ'),
        ('usd', '$'),
    ], string='Đơn vị tiền tệ', default='vnd', required=True)
    gia_tri_ban_dau = fields.Float('Giá trị ban đầu', default = 1, required=True)
    gia_tri_hien_tai = fields.Float('Giá trị hiện tại', default = 1, required=True)
    danh_muc_ts_id = fields.Many2one('danh_muc_tai_san', string='Danh mục tài sản', required=True, ondelete='restrict')

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

    don_vi_tinh = fields.Char('Đơn vị tính', default = 'Chiếc', required=True)
    ghi_chu = fields.Char('Ghi chú')

    cus_rec_name = fields.Char('Tên tài sản', compute='_compute_cus_rec_name', store=True)
    @api.depends('ten_tai_san', 'ma_tai_san')
    def _compute_cus_rec_name(self):
        for record in self:
            record.cus_rec_name = record.ma_tai_san + ' - ' + record.ten_tai_san

    phong_ban_su_dung_ids = fields.One2many('phan_bo_tai_san', 'tai_san_id', string='Phòng ban sử dụng')
    lich_su_khau_hao_ids = fields.One2many('lich_su_khau_hao', 'ma_ts', string='Lịch sử khấu hao')
    kiem_ke_history_ids = fields.One2many('kiem_ke_tai_san_line', compute='_compute_kiem_ke_history_ids', string='Lịch sử kiểm kê')
    luan_chuyen_ids = fields.Many2many('luan_chuyen_tai_san', compute='_compute_luan_chuyen_ids', string='Phiếu luân chuyển')
    thanh_ly_ids = fields.One2many('thanh_ly_tai_san', 'tai_san_id', string='Lịch sử thanh lý')
    trang_thai_thanh_ly = fields.Char(string = 'Trạng thái thanh lý', compute='_compute_trang_thai_thanh_ly', store=True)
    
    @api.depends('thanh_ly_ids')
    def _compute_trang_thai_thanh_ly(self):
        for record in self:
            thanh_ly = self.env['thanh_ly_tai_san'].search([('tai_san_id', '=', record.id)], limit=1)
            if thanh_ly:
                msg = 'Đã thanh lý' if thanh_ly.hanh_dong == 'ban' else 'Đã tiêu hủy' + f'({thanh_ly.ma_thanh_ly})'
                record.trang_thai_thanh_ly = msg
            else:
                record.trang_thai_thanh_ly = 'Chưa thanh lý'
    
    def _compute_kiem_ke_history_ids(self):
        for record in self:
            phan_bo_ids = self.env['phan_bo_tai_san'].search([('tai_san_id', '=', record.id)]).ids
            record.kiem_ke_history_ids = self.env['kiem_ke_tai_san_line'].search([
                ('phan_bo_tai_san_id', 'in', phan_bo_ids)
            ])
    
    def _compute_luan_chuyen_ids(self):
        for record in self:
            phan_bo_ids = self.env['phan_bo_tai_san'].search([('tai_san_id', '=', record.id)]).ids
            luan_chuyen_lines = self.env['luan_chuyen_tai_san_line'].search([
                ('phan_bo_tai_san_id', 'in', phan_bo_ids)
            ])
            record.luan_chuyen_ids = luan_chuyen_lines.mapped('luan_chuyen_id')

    @api.constrains('gia_tri_ban_dau', 'gia_tri_hien_tai')
    def _check_gia_tri(self):
        for record in self:
            if record.gia_tri_ban_dau < 0 or record.gia_tri_hien_tai < 0:
                raise ValidationError("Giá trị (ban đầu, hiện tại) không thể âm !")
            elif record.gia_tri_hien_tai > record.gia_tri_ban_dau:
                raise ValidationError("Giá trị hiện tại không thể lớn hơn giá trị ban đầu !")
    
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
            ma_phieu_khau_hao = 'KH-' + record.ma_tai_san + '-' + datetime.now().strftime('%Y%m%d%H%M%S%f')


            self.env['lich_su_khau_hao'].create({
                'ma_phieu_khau_hao': ma_phieu_khau_hao,
                'ma_ts': record.id,
                'ngay_khau_hao': fields.Datetime.now(),
                'so_tien_khau_hao': so_tien_khau_hao,
                'gia_tri_con_lai': record.gia_tri_hien_tai,
                'loai_phieu': 'automatic',
                'ghi_chu': f'Khấu hao tự động {fields.Date.today().strftime("%Y/%m")}'
            })

            record.thoi_gian_su_dung += 1

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

