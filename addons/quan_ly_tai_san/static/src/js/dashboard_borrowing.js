/* filepath: d:\ProjectsWorking\AssetManagement\quan_ly_tai_san\static\src\js\dashboard_borrowing.js */
odoo.define('quan_ly_tai_san.dashboard_borrowing', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var viewRegistry = require('web.view_registry');
    var core = require('web.core');

    var DashboardBorrowingController = FormController.extend({
        start: function () {
            this._super.apply(this, arguments);
            this.$el.addClass('o_dashboard_view');
        },
        willStart: function () {
            return Promise.all([
                this._super.apply(this, arguments),
                this._loadDashboardData()
            ]);
        },
        _loadDashboardData: function () {
            const self = this;
            return this._rpc({
                model: 'asset.dashboard',
                method: 'get_borrowing_data',
                args: [],
            }).then(function (data) {
                self.dashboardData = data;
            });
        },
        renderButtons: function () {
            // Hide default buttons
            this.$buttons = $();
            return this.$buttons;
        },
        _update: function () {
            const self = this;
            return this._loadDashboardData().then(function () {
                self._updateDashboard();
            });
        },
        _updateDashboard: function () {
            if (!this.dashboardData) return;
            const data = this.dashboardData;
            
            // Update summary statistics
            this.$('.pending_requests').text(data.pending_requests);
            this.$('.approved_not_returned').text(data.approved_not_returned);
            this.$('.borrowed_assets_count').text(data.borrowed_assets_count);
            
            // Render top borrowed assets chart
            this._renderTopBorrowedAssetsChart(data.top_borrowed_assets);
            
            // Render overdue borrows table
            this._renderOverdueTable(data.overdue_borrows);
        },
        _renderTopBorrowedAssetsChart: function (assets) {
            // Clear previous chart if exists
            if (this.topBorrowedChart) {
                this.topBorrowedChart.destroy();
            }
            
            const ctx = this.$('#topBorrowedAssetsChart')[0].getContext('2d');
            const labels = assets.map(a => a.asset_name);
            const data = assets.map(a => a.count);
            
            this.topBorrowedChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e',
                            '#e74a3b'
                        ],
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        }
                    }
                }
            });
        },
        _renderOverdueTable: function (overdueBorrows) {
            const $tbody = this.$('#overdueAssetsTable tbody');
            $tbody.empty();
            
            overdueBorrows.forEach(borrow => {
                const borrowDate = moment(borrow.borrow_date).format('DD/MM/YYYY');
                const dueDate = moment(borrow.due_date).format('DD/MM/YYYY');
                
                $tbody.append(`
                    <tr>
                        <td>${borrow.code}</td>
                        <td>${borrow.name}</td>
                        <td>${borrow.employee}</td>
                        <td>${borrowDate}</td>
                        <td>${dueDate}</td>
                        <td class="text-danger font-weight-bold">${borrow.days_overdue}</td>
                    </tr>
                `);
            });
            
            if (overdueBorrows.length === 0) {
                $tbody.append('<tr><td colspan="6" class="text-center">Không có tài sản nào quá hạn</td></tr>');
            }
        }
    });

    var DashboardBorrowingView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: DashboardBorrowingController
        })
    });

    viewRegistry.add('dashboard_borrowing_view', DashboardBorrowingView);
    
    return {
        DashboardBorrowingController: DashboardBorrowingController,
        DashboardBorrowingView: DashboardBorrowingView,
    };
});