// Sustainability Analytics Platform - Main JavaScript

// Global variables
let modelStatus = {
    packaging: 'not_trained',
    carbon_footprint: 'not_trained',
    product_recommendation: 'not_trained',
    esg_score: 'not_trained'
};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkModelsStatus();
});

// Initialize application
function initializeApp() {
    console.log('🌱 Sustainability Analytics Platform initialized');
    
    // Add loading states to buttons
    addLoadingStates();
    
    // Setup form validation
    setupFormValidation();
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Setup event listeners
function setupEventListeners() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form submit handlers with loading states
    setupFormSubmitHandlers();
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
            if (alert && alert.parentNode) {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }
        });
    }, 5000);
}

// Add loading states to buttons
function addLoadingStates() {
    document.querySelectorAll('button[type="submit"]').forEach(button => {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                showButtonLoading(this);
            }
        });
    });
}

// Show loading state on button
function showButtonLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    button.disabled = true;
    
    // Store original text for restoration
    button.dataset.originalText = originalText;
    
    // Auto-restore after 10 seconds (fallback)
    setTimeout(() => {
        hideButtonLoading(button);
    }, 10000);
}

// Hide loading state on button
function hideButtonLoading(button) {
    if (button.dataset.originalText) {
        button.innerHTML = button.dataset.originalText;
        button.disabled = false;
        delete button.dataset.originalText;
    }
}

// Setup form validation
function setupFormValidation() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Show first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    showValidationError(firstInvalid, 'Please fill in this field correctly.');
                }
            }
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        form.querySelectorAll('input, select, textarea').forEach(field => {
            field.addEventListener('blur', function() {
                validateField(this);
            });
            
            field.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

// Validate individual field
function validateField(field) {
    if (field.checkValidity()) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        hideValidationError(field);
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        showValidationError(field, field.validationMessage);
    }
}

// Show validation error
function showValidationError(field, message) {
    let errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        field.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Hide validation error
function hideValidationError(field) {
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}

// Setup form submit handlers
function setupFormSubmitHandlers() {
    // Handle all form submissions with AJAX
    document.querySelectorAll('form[id]').forEach(form => {
        if (form.id && !form.hasAttribute('enctype')) {
            form.addEventListener('submit', function(e) {
                handleFormSubmit(e, this);
            });
        }
    });
}

// Handle form submission
async function handleFormSubmit(event, form) {
    event.preventDefault();
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Convert checkboxes to boolean
    form.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        data[checkbox.name] = checkbox.checked;
    });
    
    // Convert numbers
    form.querySelectorAll('input[type="number"]').forEach(input => {
        if (data[input.name]) {
            data[input.name] = parseFloat(data[input.name]);
        }
    });
    
    const submitButton = form.querySelector('button[type="submit"]');
    const resultDiv = document.getElementById(form.id.replace('Form', 'Result'));
    
    try {
        // Determine API endpoint based on form ID
        let endpoint = '';
        switch (form.id) {
            case 'packagingForm':
                endpoint = '/api/predict/packaging';
                break;
            case 'carbonForm':
                endpoint = '/api/predict/carbon-footprint';
                break;
            case 'productForm':
                endpoint = '/api/predict/product-recommendation';
                break;
            case 'esgForm':
                endpoint = '/api/predict/esg-score';
                break;
            default:
                throw new Error('Unknown form type');
        }
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displaySuccess(resultDiv, result, form.id);
        } else {
            throw new Error(result.error || 'Prediction failed');
        }
        
    } catch (error) {
        displayError(resultDiv, error.message);
    } finally {
        hideButtonLoading(submitButton);
    }
}

// Display success result
function displaySuccess(resultDiv, result, formId) {
    if (!resultDiv) return;
    
    let html = '';
    
    switch (formId) {
        case 'packagingForm':
            html = `
                <div class="alert alert-success">
                    <h6><i class="fas fa-box me-2"></i>Recommended Packaging:</h6>
                    <p class="mb-1"><strong>${result.prediction}</strong></p>
                    <small class="text-muted">Confidence: ${(result.confidence * 100).toFixed(1)}%</small>
                </div>
            `;
            break;
            
        case 'carbonForm':
            html = `
                <div class="alert alert-success">
                    <h6><i class="fas fa-leaf me-2"></i>Carbon Footprint:</h6>
                    <p class="mb-1"><strong>${result.prediction.toFixed(2)} tons CO2/year</strong></p>
                    <small class="text-muted">Global average: 4.8 tons CO2/year</small>
                </div>
            `;
            // Create breakdown chart if data available
            if (result.breakdown) {
                setTimeout(() => createCarbonChart(result.breakdown), 100);
            }
            break;
            
        case 'productForm':
            html = '<div class="alert alert-success"><h6><i class="fas fa-shopping-cart me-2"></i>Recommended Products:</h6>';
            if (result.recommendations && result.recommendations.length > 0) {
                result.recommendations.forEach(product => {
                    html += `
                        <div class="border rounded p-2 mb-2 bg-light">
                            <div class="d-flex justify-content-between align-items-start">
                                <div>
                                    <strong>Product #${product.product_id}</strong>
                                    <span class="badge bg-secondary ms-2">${product.category}</span>
                                    ${product.eco_friendly ? '<span class="badge bg-success ms-1">Eco-Friendly</span>' : ''}
                                </div>
                                <div class="text-end">
                                    <div class="fw-bold">$${product.price.toFixed(2)}</div>
                                    <small class="text-muted">Score: ${product.recommendation_score.toFixed(1)}</small>
                                </div>
                            </div>
                            <div class="mt-1">
                                <small class="text-muted">
                                    Sustainability: ${product.sustainability_score.toFixed(1)}/10 | 
                                    Rating: ${product.rating.toFixed(1)}/5
                                </small>
                            </div>
                        </div>
                    `;
                });
            } else {
                html += '<p class="mb-0">No products found matching your criteria.</p>';
            }
            html += '</div>';
            break;
            
        case 'esgForm':
            const scores = result.esg_scores;
            html = `
                <div class="alert alert-success">
                    <h6><i class="fas fa-chart-bar me-2"></i>ESG Analysis Results:</h6>
                    <div class="row text-center mt-3">
                        <div class="col-3">
                            <div class="h4 text-success">${scores.e_score.toFixed(1)}</div>
                            <small class="text-muted">Environmental</small>
                        </div>
                        <div class="col-3">
                            <div class="h4 text-info">${scores.s_score.toFixed(1)}</div>
                            <small class="text-muted">Social</small>
                        </div>
                        <div class="col-3">
                            <div class="h4 text-warning">${scores.g_score.toFixed(1)}</div>
                            <small class="text-muted">Governance</small>
                        </div>
                        <div class="col-3">
                            <div class="h4 text-primary">${scores.overall_esg.toFixed(1)}</div>
                            <small class="text-muted">Overall ESG</small>
                        </div>
                    </div>
                </div>
            `;
            // Create ESG chart
            setTimeout(() => createESGChart(scores), 100);
            break;
    }
    
    resultDiv.innerHTML = html;
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display error message
function displayError(resultDiv, message) {
    if (!resultDiv) return;
    
    resultDiv.innerHTML = `
        <div class="alert alert-danger">
            <h6><i class="fas fa-exclamation-triangle me-2"></i>Error</h6>
            <p class="mb-0">${message}</p>
        </div>
    `;
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Check models status
async function checkModelsStatus() {
    try {
        const response = await fetch('/api/models/status');
        const status = await response.json();
        
        modelStatus = status;
        updateModelStatusUI(status);
        
    } catch (error) {
        console.error('Error checking model status:', error);
    }
}

// Update model status UI
function updateModelStatusUI(status) {
    // Update status indicators if they exist
    Object.keys(status).forEach(model => {
        const statusElement = document.getElementById(`${model}Status`);
        if (statusElement) {
            statusElement.textContent = status[model].replace('_', ' ').toUpperCase();
            
            // Add status indicator
            const indicator = document.createElement('span');
            indicator.className = `status-indicator ms-2 status-${status[model]}`;
            statusElement.appendChild(indicator);
        }
    });
}

// Utility Functions

// Show notification
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Copy text to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success');
    } catch (error) {
        console.error('Failed to copy to clipboard:', error);
        showNotification('Failed to copy to clipboard', 'danger');
    }
}

// Export functions for global use
window.sustainabilityAnalytics = {
    showNotification,
    formatNumber,
    formatCurrency,
    copyToClipboard,
    checkModelsStatus,
    modelStatus
};

console.log('🌱 Sustainability Analytics Platform - Main JS loaded');
