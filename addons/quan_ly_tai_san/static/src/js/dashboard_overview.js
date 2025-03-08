odoo.define('quan_ly_tai_san.dashboard_overview', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var viewRegistry = require('web.view_registry');
    var core = require('web.core');

    var DashboardOverviewController = FormController.extend({
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
                method: 'get_overview_data',
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
            
            // Update counter cards
            this.$('.total_assets').text(data.total_assets);
            this.$('.in_use_assets').text(data.in_use_assets);
            this.$('.not_used_assets').text(data.not_used_assets);
            this.$('.disposed_assets').text(data.disposed_assets);
            
            // Update financial summary
            this.$('.total_original_value').text(this._formatCurrency(data.total_original_value));
            this.$('.total_current_value').text(this._formatCurrency(data.total_current_value));
            
            // Update borrowing stats
            this.$('.borrowed_assets').text(data.borrowed_assets);
            this.$('.returned_assets').text(data.returned_assets);
            
            // Create or update charts
            this._renderDepartmentsPieChart(data.departments_data);
            this._renderAssetTypeBarChart(data.asset_types_data);
        },
        _formatCurrency: function (amount) {
            return amount.toLocaleString('vi-VN') + ' VNĐ';
        },
        _renderDepartmentsPieChart: function (departmentsData) {
            // Clear previous chart if exists
            if (this.departmentChart) {
                this.departmentChart.destroy();
            }
            
            const ctx = this.$('#departmentsPieChart')[0].getContext('2d');
            const labels = departmentsData.map(d => d.name);
            const data = departmentsData.map(d => d.count);
            
            this.departmentChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e',
                            '#e74a3b', '#5a5c69', '#858796', '#6f42c1',
                            '#20c9a6', '#3498db'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                        }
                    }
                }
            });
        },
        _renderAssetTypeBarChart: function (assetTypeData) {
            // Clear previous chart if exists
            if (this.assetTypeChart) {
                this.assetTypeChart.destroy();
            }
            
            const ctx = this.$('#assetTypeBarChart')[0].getContext('2d');
            const labels = assetTypeData.map(d => d.name);
            const data = assetTypeData.map(d => d.count);
            
            this.assetTypeChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Số lượng tài sản',
                        data: data,
                        backgroundColor: '#4e73df',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });
        }
    });

    var DashboardOverviewView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: DashboardOverviewController
        })
    });

    viewRegistry.add('dashboard_overview_view', DashboardOverviewView);
    
    return {
        DashboardOverviewController: DashboardOverviewController,
        DashboardOverviewView: DashboardOverviewView,
    };
});