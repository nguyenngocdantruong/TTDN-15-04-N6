from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class AssetDashboard(models.Model):
    _name = 'asset.dashboard'
    _description = 'Dashboard for Asset Management'
    _auto = False

    @api.model
    def name_get(self):
        return [(record.id, "Dashboard") for record in self]
    
    @api.model
    def get_overview_data(self):
        """Dashboard Tổng Quan"""
        # Tổng số tài sản
        total_assets = self.env['tai_san'].search_count([])
        in_use_assets = self.env['tai_san'].search_count([('phong_ban_su_dung_ids.trang_thai', '=', 'in-use')])
        not_used_assets = self.env['tai_san'].search_count([('phong_ban_su_dung_ids.trang_thai', '=', 'not-in-use')])
        disposed_assets = self.env['tai_san'].search_count([('trang_thai_thanh_ly', 'not like', 'Chưa thanh lý')])
        
        # Tổng giá trị tài sản
        assets = self.env['tai_san'].search([])
        total_original_value = sum(assets.mapped('gia_tri_ban_dau'))
        total_current_value = sum(assets.mapped('gia_tri_hien_tai'))
        
        # Số lượng tài sản theo loại
        asset_types = self.env['danh_muc_tai_san'].search([])
        asset_types_data = []
        for asset_type in asset_types:
            asset_count = self.env['tai_san'].search_count([('danh_muc_ts_id', '=', asset_type.id)])
            if asset_count > 0:
                asset_types_data.append({
                    'name': asset_type.ten_danh_muc_ts,
                    'count': asset_count
                })
        
        # Tổng số tài sản theo phòng ban
        departments = self.env['phong_ban'].search([])
        departments_data = []
        for dept in departments:
            asset_count = self.env['phan_bo_tai_san'].search_count([('phong_ban_id', '=', dept.id)])
            if asset_count > 0:
                departments_data.append({
                    'name': dept.ten_phong_ban or dept.ma_phong_ban,
                    'count': asset_count
                })
        
        # Tổng số tài sản đang mượn & đã trả
        borrowed_assets = self.env['muon_tra_tai_san'].search_count([('trang_thai', '=', 'dang-muon')])
        returned_assets = self.env['muon_tra_tai_san'].search_count([('trang_thai', '=', 'da-tra')])
        
        return {
            'total_assets': total_assets,
            'in_use_assets': in_use_assets,
            'not_used_assets': not_used_assets,
            'disposed_assets': disposed_assets,
            'total_original_value': total_original_value,
            'total_current_value': total_current_value,
            'asset_types_data': asset_types_data,
            'departments_data': departments_data,
            'borrowed_assets': borrowed_assets,
            'returned_assets': returned_assets,
        }
    
    
    @api.model
    def get_borrowing_data(self):
        """Dashboard Đơn Mượn & Trả Tài Sản"""
        # Số đơn mượn đang chờ duyệt
        pending_requests = self.env['don_muon_tai_san'].search_count([
            ('trang_thai', '=', 'dang-cho')
        ])
        
        # Số đơn đã duyệt và chưa trả
        approved_not_returned = self.env['muon_tra_tai_san'].search_count([
            ('trang_thai', '=', 'dang-muon')
        ])
        
        # Số tài sản đang được mượn
        borrowed_assets_count = self.env['muon_tra_tai_san_line'].search_count([
            ('muon_tra_id.trang_thai', '=', 'dang-muon')
        ])
        
        # Top tài sản được mượn nhiều nhất
        phan_bo_tai_san_ids = self.env['muon_tra_tai_san_line'].search([]).mapped('phan_bo_tai_san_id.id')
        phan_bo_counts = {}
        for phan_bo_id in phan_bo_tai_san_ids:
            if phan_bo_id in phan_bo_counts:
                phan_bo_counts[phan_bo_id] += 1
            else:
                phan_bo_counts[phan_bo_id] = 1
        
        # Sort by borrow count and get top 5
        top_borrowed_assets = []
        if phan_bo_counts:
            sorted_phan_bo = sorted(phan_bo_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for phan_bo_id, count in sorted_phan_bo:
                phan_bo = self.env['phan_bo_tai_san'].browse(phan_bo_id)
                top_borrowed_assets.append({
                    'asset_name': phan_bo.tai_san_id.ten_tai_san,
                    'department': phan_bo.phong_ban_id.ten_phong_ban or phan_bo.phong_ban_id.ma_phong_ban,
                    'count': count
                })
        
        # Danh sách tài sản quá hạn chưa trả
        now = fields.Datetime.now()
        overdue_borrows = self.env['muon_tra_tai_san'].search([
            ('trang_thai', '=', 'dang-muon'),
            ('thoi_gian_tra', '<', now)
        ], limit=10)
        
        overdue_data = []
        for borrow in overdue_borrows:
            overdue_data.append({
                'id': borrow.id,
                'code': borrow.ma_phieu_muon_tra,
                'name': borrow.ten_phieu_muon_tra,
                'department': borrow.phong_ban_cho_muon_id.ten_phong_ban or borrow.phong_ban_cho_muon_id.ma_phong_ban,
                'employee': borrow.nhan_vien_muon_id.ho_ten if borrow.nhan_vien_muon_id else '',
                'borrow_date': borrow.thoi_gian_muon,
                'due_date': borrow.thoi_gian_tra,
                'days_overdue': (fields.Datetime.now() - borrow.thoi_gian_tra).days
            })
        
        return {
            'pending_requests': pending_requests,
            'approved_not_returned': approved_not_returned,
            'borrowed_assets_count': borrowed_assets_count,
            'top_borrowed_assets': top_borrowed_assets,
            'overdue_borrows': overdue_data
        }
