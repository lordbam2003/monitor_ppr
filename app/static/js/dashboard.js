// dashboard.js - Funcionalidad para el dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráficos
    initCharts();
    
    // Inicializar otras funcionalidades
    initEventListeners();
});

function initCharts() {
    // Gráfico de avance de PPR por mes
    const ctx = document.getElementById('avanceChart').getContext('2d');
    
    // Datos simulados para el gráfico
    const data = {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        datasets: [{
            label: 'Avance Programado',
            data: [10, 20, 30, 40, 50, 60, 70, 75, 80, 85, 90, 95],
            borderColor: '#0d6efd',
            backgroundColor: 'rgba(13, 110, 253, 0.1)',
            fill: true
        }, {
            label: 'Avance Ejecutado',
            data: [5, 15, 25, 35, 45, 55, 65, 72, 78, 82, 88, 92],
            borderColor: '#198754',
            backgroundColor: 'rgba(25, 135, 84, 0.1)',
            fill: true
        }]
    };
    
    // Configuración del gráfico
    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Comparativo Avance Programado vs Ejecutado'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    };
    
    // Crear el gráfico
    new Chart(ctx, config);
}

function initEventListeners() {
    // Event listener para el botón de cierre de sesión
    const logoutBtn = document.querySelector('a[href="index.html"]');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            // Preguntar confirmación antes de cerrar sesión
            if (!confirm('¿Está seguro que desea cerrar sesión?')) {
                e.preventDefault();
            }
        });
    }
    
    // Event listener para los enlaces de navegación
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Remover clase 'active' de todos los enlaces
            navLinks.forEach(l => l.classList.remove('active'));
            // Agregar clase 'active' al enlace actual
            this.classList.add('active');
        });
    });
    
    // Actualizar el contador de notificaciones
    updateNotificationCount();
}

function updateNotificationCount() {
    // Simular actualización del contador de notificaciones
    const notificationBadge = document.querySelector('.badge-counter');
    if (notificationBadge) {
        // En una implementación real, esto se obtendría de una API
        const count = 3; // Simulado
        notificationBadge.textContent = count > 0 ? count + '+' : '';
        notificationBadge.style.display = count > 0 ? 'inline' : 'none';
    }
}

// Función para hacer llamadas a los endpoints del backend
async function callApi(endpoint, method = 'GET', data = null) {
    const url = `/api${endpoint}`;
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    // Agregar token de autenticación si existe
    const token = localStorage.getItem('authToken');
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Función para mostrar alertas
function showAlert(message, type = 'info') {
    // Remover alerta previa si existe
    const existingAlert = document.querySelector('.alert-container');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert-container alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove después de 5 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}