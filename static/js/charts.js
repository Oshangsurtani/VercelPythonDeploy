// Sustainability Analytics Platform - Charts JavaScript

// Chart configurations and utilities
const ChartConfig = {
    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    usePointStyle: true,
                    padding: 20,
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: 'white',
                bodyColor: 'white',
                borderColor: 'rgba(255, 255, 255, 0.2)',
                borderWidth: 1,
                cornerRadius: 8,
                displayColors: false
            }
        }
    },
    colors: {
        primary: '#007bff',
        success: '#28a745',
        info: '#17a2b8',
        warning: '#ffc107',
        danger: '#dc3545',
        sustainability: '#28a745',
        carbon: '#17a2b8',
        eco: '#ffc107'
    }
};

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('📊 Charts module loaded');
});

// Create carbon footprint breakdown chart
function createCarbonChart(breakdown) {
    const canvas = document.getElementById('carbonChart');
    if (!canvas) return;
    
    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }
    
    canvas.style.display = 'block';
    canvas.height = 300;
    
    const ctx = canvas.getContext('2d');
    
    const data = {
        labels: ['Transport', 'Housing', 'Food', 'Consumption', 'Other'],
        datasets: [{
            data: [
                breakdown.transport || 0,
                breakdown.housing || 0,
                breakdown.food || 0,
                breakdown.consumption || 0,
                breakdown.other || 0
            ],
            backgroundColor: [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF'
            ],
            borderColor: [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF'
            ],
            borderWidth: 2
        }]
    };
    
    const options = {
        ...ChartConfig.defaultOptions,
        plugins: {
            ...ChartConfig.defaultOptions.plugins,
            title: {
                display: true,
                text: 'Carbon Footprint Breakdown (tons CO2/year)',
                font: {
                    size: 16,
                    weight: 'bold'
                },
                padding: 20
            },
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true
                }
            },
            tooltip: {
                ...ChartConfig.defaultOptions.plugins.tooltip,
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.parsed || 0;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(1);
                        return `${label}: ${value.toFixed(2)} tons (${percentage}%)`;
                    }
                }
            }
        }
    };
    
    canvas.chart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: options
    });
}

// Create ESG score radar chart
function createESGChart(scores) {
    const canvas = document.getElementById('esgChart');
    if (!canvas) return;
    
    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }
    
    canvas.style.display = 'block';
    canvas.height = 400;
    
    const ctx = canvas.getContext('2d');
    
    const data = {
        labels: ['Environmental', 'Social', 'Governance'],
        datasets: [{
            label: 'ESG Scores',
            data: [
                scores.e_score || 0,
                scores.s_score || 0,
                scores.g_score || 0
            ],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            pointBackgroundColor: 'rgba(75, 192, 192, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 3,
            pointRadius: 6,
            pointHoverRadius: 8
        }]
    };
    
    const options = {
        ...ChartConfig.defaultOptions,
        scales: {
            r: {
                beginAtZero: true,
                max: 10,
                ticks: {
                    stepSize: 2,
                    color: 'rgba(255, 255, 255, 0.7)'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.2)'
                },
                angleLines: {
                    color: 'rgba(255, 255, 255, 0.2)'
                },
                pointLabels: {
                    color: 'rgba(255, 255, 255, 0.9)',
                    font: {
                        size: 12,
                        weight: 'bold'
                    }
                }
            }
        },
        plugins: {
            ...ChartConfig.defaultOptions.plugins,
            title: {
                display: true,
                text: 'ESG Score Analysis (0-10 scale)',
                font: {
                    size: 16,
                    weight: 'bold'
                },
                padding: 20
            },
            legend: {
                display: false
            },
            tooltip: {
                ...ChartConfig.defaultOptions.plugins.tooltip,
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.parsed.r || 0;
                        return `${label}: ${value.toFixed(1)}/10`;
                    }
                }
            }
        }
    };
    
    canvas.chart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: options
    });
}

// Create model performance chart
function createPerformanceChart(containerId, data) {
    const canvas = document.getElementById(containerId);
    if (!canvas) return;
    
    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }
    
    const ctx = canvas.getContext('2d');
    
    const chartData = {
        labels: data.labels || ['Packaging', 'Carbon Footprint', 'Product Rec.', 'ESG Analysis'],
        datasets: [{
            label: 'Accuracy (%)',
            data: data.values || [89, 92, 87, 91],
            backgroundColor: [
                ChartConfig.colors.primary,
                ChartConfig.colors.success,
                ChartConfig.colors.info,
                ChartConfig.colors.warning
            ],
            borderColor: [
                ChartConfig.colors.primary,
                ChartConfig.colors.success,
                ChartConfig.colors.info,
                ChartConfig.colors.warning
            ],
            borderWidth: 2,
            borderRadius: 8,
            borderSkipped: false
        }]
    };
    
    const options = {
        ...ChartConfig.defaultOptions,
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)',
                    callback: function(value) {
                        return value + '%';
                    }
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            },
            x: {
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)'
                },
                grid: {
                    display: false
                }
            }
        },
        plugins: {
            ...ChartConfig.defaultOptions.plugins,
            legend: {
                display: false
            },
            tooltip: {
                ...ChartConfig.defaultOptions.plugins.tooltip,
                callbacks: {
                    label: function(context) {
                        return `${context.label}: ${context.parsed.y}%`;
                    }
                }
            }
        }
    };
    
    canvas.chart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: options
    });
}

// Create usage statistics pie chart
function createUsageChart(containerId, data) {
    const canvas = document.getElementById(containerId);
    if (!canvas) return;
    
    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }
    
    const ctx = canvas.getContext('2d');
    
    const chartData = {
        labels: data.labels || ['Packaging', 'Carbon Footprint', 'Product Rec.', 'ESG Analysis'],
        datasets: [{
            data: data.values || [35, 28, 22, 15],
            backgroundColor: [
                ChartConfig.colors.primary,
                ChartConfig.colors.success,
                ChartConfig.colors.info,
                ChartConfig.colors.warning
            ],
            borderWidth: 2,
            borderColor: 'rgba(255, 255, 255, 0.1)'
        }]
    };
    
    const options = {
        ...ChartConfig.defaultOptions,
        plugins: {
            ...ChartConfig.defaultOptions.plugins,
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true
                }
            },
            tooltip: {
                ...ChartConfig.defaultOptions.plugins.tooltip,
                callbacks: {
                    label: function(context) {
                        const label = context.label || '';
                        const value = context.parsed || 0;
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((value / total) * 100).toFixed(1);
                        return `${label}: ${percentage}%`;
                    }
                }
            }
        }
    };
    
    canvas.chart = new Chart(ctx, {
        type: 'doughnut',
        data: chartData,
        options: options
    });
}

// Create trends line chart
function createTrendsChart(containerId, data) {
    const canvas = document.getElementById(containerId);
    if (!canvas) return;
    
    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }
    
    const ctx = canvas.getContext('2d');
    
    const chartData = {
        labels: data.labels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [
            {
                label: 'Average Carbon Footprint',
                data: data.actual || [8.5, 8.2, 7.9, 7.6, 7.4, 7.1],
                borderColor: ChartConfig.colors.success,
                backgroundColor: ChartConfig.colors.success + '20',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: ChartConfig.colors.success,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            },
            {
                label: 'Global Average',
                data: data.baseline || [4.8, 4.8, 4.8, 4.8, 4.8, 4.8],
                borderColor: ChartConfig.colors.danger,
                backgroundColor: ChartConfig.colors.danger + '20',
                borderDash: [5, 5],
                pointBackgroundColor: ChartConfig.colors.danger,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            }
        ]
    };
    
    const options = {
        ...ChartConfig.defaultOptions,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Tons CO2/year',
                    color: 'rgba(255, 255, 255, 0.7)'
                },
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            },
            x: {
                ticks: {
                    color: 'rgba(255, 255, 255, 0.7)'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            }
        },
        plugins: {
            ...ChartConfig.defaultOptions.plugins,
            legend: {
                position: 'top',
                labels: {
                    padding: 20,
                    usePointStyle: true
                }
            }
        }
    };
    
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: options
    });
}

// Utility function to destroy all charts
function destroyAllCharts() {
    document.querySelectorAll('canvas').forEach(canvas => {
        if (canvas.chart) {
            canvas.chart.destroy();
            canvas.chart = null;
        }
    });
}

// Utility function to resize all charts
function resizeAllCharts() {
    document.querySelectorAll('canvas').forEach(canvas => {
        if (canvas.chart) {
            canvas.chart.resize();
        }
    });
}

// Handle window resize
window.addEventListener('resize', function() {
    setTimeout(resizeAllCharts, 100);
});

// Export functions for global use
window.sustainabilityCharts = {
    createCarbonChart,
    createESGChart,
    createPerformanceChart,
    createUsageChart,
    createTrendsChart,
    destroyAllCharts,
    resizeAllCharts,
    ChartConfig
};

console.log('📊 Sustainability Analytics Platform - Charts JS loaded');
