/**
 * Base JavaScript for ePallet Application
 * Funcionalidades gerais e utilitários
 */

// Aguardar carregamento do DOM
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Inicializar funcionalidades
    initForms();
    initTables();
    initAlerts();
    initTooltips();
    
    console.log('ePallet App initialized');
}

// Funcionalidades de formulários
function initForms() {
    // Auto-focus no primeiro campo de formulário
    const firstInput = document.querySelector('form input:not([type="hidden"]):not([readonly])');
    if (firstInput) {
        firstInput.focus();
    }
    
    // Validação de formulários
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
    
    // Confirmação antes de enviar formulários críticos
    const criticalForms = document.querySelectorAll('form[data-confirm]');
    criticalForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const message = form.getAttribute('data-confirm') || 'Tem certeza que deseja continuar?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// Validação básica de formulários
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            showFieldError(field, 'Este campo é obrigatório');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Validação de email
    const emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(function(field) {
        if (field.value && !isValidEmail(field.value)) {
            showFieldError(field, 'Email inválido');
            isValid = false;
        }
    });
    
    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    errorDiv.textContent = message;
    
    field.style.borderColor = '#dc3545';
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    field.style.borderColor = '';
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Funcionalidades de tabelas
function initTables() {
    // Ordenação de tabelas
    const sortableTables = document.querySelectorAll('table[data-sortable]');
    sortableTables.forEach(function(table) {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(function(header) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, header);
            });
        });
    });
    
    // Filtro de tabelas
    const filterInputs = document.querySelectorAll('input[data-table-filter]');
    filterInputs.forEach(function(input) {
        const tableId = input.getAttribute('data-table-filter');
        const table = document.getElementById(tableId);
        if (table) {
            input.addEventListener('input', function() {
                filterTable(table, input.value);
            });
        }
    });
}

function sortTable(table, header) {
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const isAscending = header.classList.contains('sort-asc');
    
    // Remover classes de ordenação de outros headers
    table.querySelectorAll('th').forEach(function(th) {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Ordenar linhas
    rows.sort(function(a, b) {
        const aText = a.children[columnIndex].textContent.trim();
        const bText = b.children[columnIndex].textContent.trim();
        
        // Tentar converter para número
        const aNum = parseFloat(aText);
        const bNum = parseFloat(bText);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? bNum - aNum : aNum - bNum;
        } else {
            return isAscending ? bText.localeCompare(aText) : aText.localeCompare(bText);
        }
    });
    
    // Adicionar classe de ordenação
    header.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
    
    // Reordenar DOM
    const tbody = table.querySelector('tbody');
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

function filterTable(table, filterText) {
    const rows = table.querySelectorAll('tbody tr');
    const filter = filterText.toLowerCase();
    
    rows.forEach(function(row) {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
    });
}

// Funcionalidades de alertas
function initAlerts() {
    // Auto-fechar alertas após 5 segundos
    const alerts = document.querySelectorAll('.alert[data-auto-dismiss]');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            fadeOut(alert);
        }, 5000);
    });
    
    // Botões de fechar alertas
    const closeButtons = document.querySelectorAll('.alert .close, .alert [data-dismiss="alert"]');
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const alert = button.closest('.alert');
            fadeOut(alert);
        });
    });
}

function fadeOut(element) {
    element.style.transition = 'opacity 0.3s';
    element.style.opacity = '0';
    setTimeout(function() {
        element.remove();
    }, 300);
}

// Tooltips simples
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(function(element) {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const element = e.target;
    const text = element.getAttribute('data-tooltip');
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: #333;
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 12px;
        z-index: 1000;
        pointer-events: none;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    element._tooltip = tooltip;
}

function hideTooltip(e) {
    const element = e.target;
    if (element._tooltip) {
        element._tooltip.remove();
        delete element._tooltip;
    }
}

// Utilitários
function showLoading(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    
    if (element) {
        element.innerHTML = '<div class="spinner"></div>';
    }
}

function hideLoading(element, content) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    
    if (element) {
        element.innerHTML = content || '';
    }
}

function showMessage(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1050;
        min-width: 300px;
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(function() {
        fadeOut(alert);
    }, 3000);
}

// Exportar funções para uso global
window.ePallet = {
    showMessage: showMessage,
    showLoading: showLoading,
    hideLoading: hideLoading,
    validateForm: validateForm,
    sortTable: sortTable,
    filterTable: filterTable
};

