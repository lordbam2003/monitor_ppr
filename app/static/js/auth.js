// auth.js - Funciones de autenticación generales

class AuthManager {
    constructor() {
        this.tokenKey = 'authToken';
        this.userKey = 'userData';
    }

    // Almacenar token de autenticación
    setToken(token) {
        localStorage.setItem(this.tokenKey, token);
    }

    // Obtener token de autenticación
    getToken() {
        return localStorage.getItem(this.tokenKey);
    }

    // Eliminar token (cerrar sesión)
    removeToken() {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem(this.userKey);
    }

    // Verificar si el usuario está autenticado
    isAuthenticated() {
        const token = this.getToken();
        if (!token) return false;
        
        // Verificar si el token ha expirado
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const currentTime = Date.now() / 1000;
            return payload.exp > currentTime;
        } catch (e) {
            return false;
        }
    }

    // Almacenar información del usuario
    setUserData(userData) {
        localStorage.setItem(this.userKey, JSON.stringify(userData));
    }

    // Obtener información del usuario
    getUserData() {
        const userData = localStorage.getItem(this.userKey);
        return userData ? JSON.parse(userData) : null;
    }

    // Hacer una solicitud autenticada
    async authenticatedFetch(url, options = {}) {
        const token = this.getToken();
        
        if (!token) {
            throw new Error('No hay token de autenticación');
        }

        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };

        const response = await fetch(url, options);

        if (response.status === 401) {
            // Token expirado o inválido, redirigir a login
            this.removeToken();
            window.location.href = 'index.html';
            return;
        }

        return response;
    }
}

// Instancia global del AuthManager
const authManager = new AuthManager();

// Middleware para proteger rutas
function requireAuth() {
    if (!authManager.isAuthenticated()) {
        window.location.href = 'index.html';
    }
}

// Función para proteger páginas que requieren autenticación
document.addEventListener('DOMContentLoaded', function() {
    // En páginas que requieren autenticación, descomentar la siguiente línea:
    // requireAuth();
});