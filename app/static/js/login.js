// login.js - Funcionalidad para la página de inicio de sesión

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Validación simple
            if (!username || !password) {
                showAlert('Por favor complete todos los campos', 'error');
                return;
            }
            
            try {
                // Simular inicio de sesión (esto debería conectarse con el endpoint real)
                const response = await simulateLogin(username, password);
                
                if (response.success) {
                    showAlert('Inicio de sesión exitoso', 'success');
                    // Redirigir al dashboard
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 1500);
                } else {
                    showAlert(response.message || 'Credenciales incorrectas', 'error');
                }
            } catch (error) {
                showAlert('Error de conexión con el servidor', 'error');
                console.error('Login error:', error);
            }
        });
    }
});

// Simulación de la llamada al endpoint de login
async function simulateLogin(username, password) {
    // En una implementación real, aquí se haría una llamada al endpoint:
    // const response = await fetch('/auth/login', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/x-www-form-urlencoded',
    //     },
    //     body: new URLSearchParams({
    //         username: username,
    //         password: password
    //     })
    // });
    // return await response.json();
    
    // Simulación para fines de demostración
    return new Promise((resolve) => {
        setTimeout(() => {
            // Credenciales válidas de ejemplo
            if (username === 'admin' && password === 'admin123') {
                resolve({ success: true, message: 'Inicio de sesión exitoso' });
            } else {
                resolve({ success: false, message: 'Credenciales incorrectas' });
            }
        }, 1000);
    });
}

// Función para mostrar alertas
function showAlert(message, type) {
    // Remover alerta previa si existe
    const existingAlert = document.querySelector('.alert-container');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert-container alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
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