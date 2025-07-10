/**
 * Password View Toggle Functionality
 * Permite mostrar/ocultar senhas em campos de input
 */

document.addEventListener('DOMContentLoaded', function() {
    initPasswordToggle();
});

function initPasswordToggle() {
    // Encontrar todos os campos de senha
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(function(field) {
        // Verificar se já tem toggle (evitar duplicação)
        if (field.parentElement.classList.contains('password-field-container')) {
            return;
        }
        
        // Criar container
        const container = document.createElement('div');
        container.className = 'password-field-container';
        
        // Inserir container antes do campo
        field.parentNode.insertBefore(container, field);
        
        // Mover campo para dentro do container
        container.appendChild(field);
        
        // Adicionar classe ao campo
        field.classList.add('password-field');
        
        // Criar botão de toggle
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'password-toggle-btn';
        toggleBtn.innerHTML = '<span class="password-toggle-icon eye-icon"></span>';
        toggleBtn.setAttribute('aria-label', 'Mostrar senha');
        toggleBtn.setAttribute('title', 'Mostrar senha');
        
        // Adicionar evento de clique
        toggleBtn.addEventListener('click', function() {
            togglePasswordVisibility(field, toggleBtn);
        });
        
        // Adicionar botão ao container
        container.appendChild(toggleBtn);
    });
}

function togglePasswordVisibility(field, button) {
    const icon = button.querySelector('.password-toggle-icon');
    
    if (field.type === 'password') {
        // Mostrar senha
        field.type = 'text';
        icon.className = 'password-toggle-icon eye-slash-icon';
        button.setAttribute('aria-label', 'Ocultar senha');
        button.setAttribute('title', 'Ocultar senha');
    } else {
        // Ocultar senha
        field.type = 'password';
        icon.className = 'password-toggle-icon eye-icon';
        button.setAttribute('aria-label', 'Mostrar senha');
        button.setAttribute('title', 'Mostrar senha');
    }
}

// Função para adicionar toggle a um campo específico
function addPasswordToggle(fieldId) {
    const field = document.getElementById(fieldId);
    if (field && field.type === 'password') {
        // Simular que o campo foi encontrado pela função principal
        initPasswordToggle();
    }
}

// Função para remover toggle de um campo
function removePasswordToggle(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        const container = field.closest('.password-field-container');
        if (container) {
            const parent = container.parentNode;
            parent.insertBefore(field, container);
            parent.removeChild(container);
            field.classList.remove('password-field');
            field.type = 'password';
        }
    }
}

// Função para toggle programático
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        const container = field.closest('.password-field-container');
        if (container) {
            const button = container.querySelector('.password-toggle-btn');
            if (button) {
                togglePasswordVisibility(field, button);
            }
        }
    }
}

// Exportar funções para uso global
window.passwordToggle = {
    init: initPasswordToggle,
    add: addPasswordToggle,
    remove: removePasswordToggle,
    toggle: togglePassword
};

// Auto-inicializar em mudanças dinâmicas do DOM
if (window.MutationObserver) {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        const passwordFields = node.querySelectorAll ? node.querySelectorAll('input[type="password"]') : [];
                        if (passwordFields.length > 0) {
                            setTimeout(initPasswordToggle, 100);
                        }
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

