// Comportamiento global para la aplicación
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-ocultar alertas después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

/**
 * 3IT App - Funcionalidades JavaScript para el Formateador de CVs
 */

// Inicialización cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Inicializa todas las funcionalidades de la aplicación
 */
function initializeApp() {
    // Inicializar componentes Bootstrap
    initBootstrapComponents();
    
    // Configurar formulario de CV
    setupCVForm();
    
    // Configurar efectos visuales
    setupVisualEffects();
    
    // Configurar notificaciones
    setupNotifications();
}

/**
 * Inicializa componentes de Bootstrap
 */
function initBootstrapComponents() {
    // Inicializar tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-ocultar alertas después de 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

/**
 * Configura el formulario de CV
 */
function setupCVForm() {
    const cvForm = document.getElementById('cv-form');
    if (!cvForm) return;

    // Actualizar nombre de archivo cuando se selecciona
    const cvFileInput = document.getElementById('cv_file');
    const templateFileInput = document.getElementById('template_file');
    
    if (cvFileInput) {
        cvFileInput.addEventListener('change', function() {
            updateFileInfo(this, 'cv-file-info');
        });
    }
    
    if (templateFileInput) {
        templateFileInput.addEventListener('change', function() {
            updateFileInfo(this, 'template-file-info');
        });
    }
    
    // Validar formulario antes de enviar
    cvForm.addEventListener('submit', function(event) {
        if (!validateCVForm()) {
            event.preventDefault();
            return false;
        }
        
        // Mostrar indicador de carga
        showLoader();
        
        // Deshabilitar botón de envío
        const submitButton = cvForm.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Procesando...';
        }
        
        return true;
    });
}

/**
 * Actualiza la información de archivo mostrada
 */
function updateFileInfo(input, infoElementId) {
    const infoElement = document.getElementById(infoElementId);
    if (!infoElement) return;
    
    if (input.files && input.files[0]) {
        const fileName = input.files[0].name;
        infoElement.innerHTML = `
            <div class="d-flex align-items-center mt-2">
                <span class="text-success me-2">✓</span>
                Archivo seleccionado: <span class="file-selected ms-1">${fileName}</span>
            </div>
        `;
        infoElement.style.display = 'block';
    } else {
        infoElement.style.display = 'none';
    }
}

/**
 * Valida el formulario de CV
 */
function validateCVForm() {
    const cvFileInput = document.getElementById('cv_file');
    const templateFileInput = document.getElementById('template_file');
    let isValid = true;
    
    // Validar archivo CV
    if (cvFileInput && (!cvFileInput.files || cvFileInput.files.length === 0)) {
        showError('Por favor, seleccione un archivo CV');
        isValid = false;
    } else if (cvFileInput && cvFileInput.files[0]) {
        const fileName = cvFileInput.files[0].name.toLowerCase();
        if (!fileName.endsWith('.pdf') && !fileName.endsWith('.docx') && !fileName.endsWith('.doc')) {
            showError('Por favor, seleccione un archivo PDF o DOCX válido para el CV');
            isValid = false;
        }
    }
    
    // Validar archivo de plantilla
    if (templateFileInput && (!templateFileInput.files || templateFileInput.files.length === 0)) {
        showError('Por favor, seleccione una plantilla');
        isValid = false;
    } else if (templateFileInput && templateFileInput.files[0]) {
        const fileName = templateFileInput.files[0].name.toLowerCase();
        if (!fileName.endsWith('.docx')) {
            showError('Por favor, seleccione un archivo DOCX válido para la plantilla');
            isValid = false;
        }
    }
    
    return isValid;
}

/**
 * Muestra un mensaje de error
 */
function showError(message) {
    // Buscar o crear el contenedor de mensajes
    let messagesContainer = document.querySelector('.messages');
    if (!messagesContainer) {
        messagesContainer = document.createElement('div');
        messagesContainer.className = 'messages mb-4';
        
        // Insertar después del encabezado
        const header = document.querySelector('.text-center.mb-4');
        if (header && header.parentNode) {
            header.parentNode.insertBefore(messagesContainer, header.nextSibling);
        }
    }
    
    // Crear la alerta
    const alertElement = document.createElement('div');
    alertElement.className = 'alert alert-danger alert-dismissible fade show';
    alertElement.role = 'alert';
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Agregar al contenedor de mensajes
    messagesContainer.appendChild(alertElement);
    
    // Inicializar alerta de Bootstrap
    new bootstrap.Alert(alertElement);
}

/**
 * Configura efectos visuales
 */
function setupVisualEffects() {
    // Añadir efectos hover a las tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 38, 0.15)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 20px rgba(0, 0, 38, 0.1)';
        });
    });
    
    // Añadir efecto hover a botones
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(function(button) {
        if (!button.classList.contains('btn-close')) {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.transition = 'all 0.3s ease';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        }
    });
    
    // Añadir efecto parallax al contenedor principal
    const mainContainer = document.querySelector('.main-container');
    if (mainContainer) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.scrollY;
            const decorationElements = mainContainer.querySelectorAll('.decoration, .header-bg');
            
            decorationElements.forEach(function(element) {
                const speed = element.classList.contains('header-bg') ? 0.1 : -0.05;
                element.style.transform = `translateY(${scrollTop * speed}px)`;
            });
        });
    }
}

/**
 * Configura sistema de notificaciones
 */
function setupNotifications() {
    // Crear elemento para notificaciones
    const notificationContainer = document.createElement('div');
    notificationContainer.className = 'notification-container';
    notificationContainer.style.position = 'fixed';
    notificationContainer.style.bottom = '20px';
    notificationContainer.style.right = '20px';
    notificationContainer.style.zIndex = '9999';
    document.body.appendChild(notificationContainer);
    
    // Exponer método global para mostrar notificaciones
    window.showNotification = function(message, type = 'info') {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} fade-in`;
        notification.style.backgroundColor = type === 'success' ? 'rgba(44, 213, 196, 0.95)' : 
                                          type === 'error' ? 'rgba(220, 53, 69, 0.95)' : 
                                          'rgba(0, 90, 238, 0.95)';
        notification.style.color = 'white';
        notification.style.padding = '15px 20px';
        notification.style.borderRadius = '8px';
        notification.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        notification.style.marginTop = '10px';
        notification.style.maxWidth = '300px';
        notification.style.wordWrap = 'break-word';
        
        // Contenido de la notificación
        const iconMap = {
            success: '✓',
            error: '✕',
            info: 'ℹ'
        };
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center;">
                <div style="margin-right: 10px; font-size: 20px;">${iconMap[type] || iconMap.info}</div>
                <div>${message}</div>
            </div>
        `;
        
        // Agregar al contenedor
        notificationContainer.appendChild(notification);
        
        // Eliminar después de 5 segundos
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            notification.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 5000);
    };
}

/**
 * Muestra u oculta el indicador de carga
 */
function showLoader(show = true) {
    let loader = document.getElementById('loader-3it');
    
    if (!loader && show) {
        loader = document.createElement('div');
        loader.id = 'loader-3it';
        loader.className = 'loader-3it';
        document.body.appendChild(loader);
    } else if (loader && !show) {
        loader.remove();
    }
}

/**
 * Utilidad para formatear fechas
 */
function formatDate(dateString) {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

/**
 * Utilidad para formatear hora
 */
function formatTime(dateString) {
    const options = { hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleTimeString('es-ES', options);
}