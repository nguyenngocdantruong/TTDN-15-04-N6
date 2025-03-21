# -*- coding: utf-8 -*-
{
    'name': "quan_ly_tai_san",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Quản lý tài sản của Doanh Nghiệp
    """,

    'author': "Nguyễn Ngọc Đan Trường - 1504",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/danh_muc_tai_san.xml',
        'views/kiem_ke_tai_san.xml',
        'views/lich_su_khau_hao.xml',
        'views/luan_chuyen_tai_san.xml',
        'views/don_muon_tai_san.xml',
        'views/muon_tra_tai_san.xml',
        'views/phan_bo_tai_san.xml',
        'views/tai_san.xml',
        'views/thanh_ly_tai_san.xml',
        'views/dashboard_overview.xml',
        'views/dashboard_borrowing.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'assets': {
        'web.assets_backend': [
            'https://cdn.jsdelivr.net/npm/chart.js@3.7.1/dist/chart.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js',
            'quan_ly_tai_san/static/src/css/dashboard.css',
            'quan_ly_tai_san/static/src/js/dashboard_overview.js',
            'quan_ly_tai_san/static/src/js/dashboard_borrowing.js',
        ],
    },
}