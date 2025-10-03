// ppr.js - Funcionalidad para la gestión de PPRs

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades de la página de PPR
    initPprPage();
    
    // Event listeners para botones
    const saveBtn = document.getElementById('savePprBtn');
    if (saveBtn) {
        saveBtn.addEventListener('click', savePpr);
    }
    
    // Inicializar la tabla
    initializeTable();
});

function initPprPage() {
    console.log('Página de gestión de PPR inicializada');
    
    // Proteger la página si el usuario no está autenticado
    if (!authManager.isAuthenticated()) {
        window.location.href = 'index.html';
    }
    
    // Actualizar la interfaz según el rol del usuario
    updateInterfaceForRole();
}

function updateInterfaceForRole() {
    const userData = authManager.getUserData();
    if (userData) {
        // Por ejemplo, ocultar botones si el usuario no tiene permisos
        // Esto dependerá de la implementación específica de roles
        console.log('Usuario:', userData.username, 'Rol:', userData.role);
    }
}

function savePpr() {
    // Obtener datos del formulario
    const codigo = document.getElementById('codigo').value;
    const nombre = document.getElementById('nombre').value;
    const descripcion = document.getElementById('descripcion').value;
    const unidadMedida = document.getElementById('unidadMedida').value;
    const estado = document.getElementById('estado').value;
    const fechaInicio = document.getElementById('fechaInicio').value;
    const fechaFin = document.getElementById('fechaFin').value;
    
    // Obtener responsables seleccionados
    const responsablesSelect = document.getElementById('responsables');
    const responsables = Array.from(responsablesSelect.selectedOptions).map(option => option.value);
    
    // Validar campos requeridos
    if (!codigo || !nombre) {
        showAlert('Por favor complete los campos requeridos', 'error');
        return;
    }
    
    // Enviar datos al backend
    const pprData = {
        codigo: codigo,
        nombre: nombre,
        descripcion: descripcion,
        unidad_medida: unidadMedida,
        responsable_planificacion_id: 1, // Esto debería obtenerse del usuario actual
        estado: estado,
        fecha_inicio: fechaInicio ? new Date(fechaInicio).toISOString() : null,
        fecha_fin: fechaFin ? new Date(fechaFin).toISOString() : null,
        ano_ejecucion: new Date().getFullYear(),
        responsable_ppr_ids: responsables.map(id => parseInt(id))
    };
    
    // Simular la llamada al API (en implementación real, usar fetch)
    simulateCreatePpr(pprData)
        .then(response => {
            if (response.success) {
                showAlert('PPR creado exitosamente', 'success');
                // Limpiar formulario
                document.getElementById('pprForm').reset();
                // Cerrar modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addPprModal'));
                if (modal) {
                    modal.hide();
                }
                // Actualizar tabla
                setTimeout(updatePprTable, 500);
            } else {
                showAlert(response.message || 'Error al crear el PPR', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error de conexión con el servidor', 'error');
        });
}

// Simulación de la creación de un PPR
function simulateCreatePpr(pprData) {
    // En implementación real:
    // return authManager.authenticatedFetch('/ppr/', {
    //     method: 'POST',
    //     body: JSON.stringify(pprData)
    // }).then(response => response.json());
    
    return new Promise((resolve) => {
        setTimeout(() => {
            // Simular éxito
            resolve({ success: true, message: 'PPR creado exitosamente', data: { ...pprData, id: Math.floor(Math.random() * 1000) } });
        }, 1000);
    });
}

function updatePprTable() {
    // Simular actualización de la tabla
    console.log('Actualizando tabla de PPRs...');
    // En implementación real, se llamaría al API para obtener los PPRs actualizados
    // y se actualizaría la tabla
}

function initializeTable() {
    // Inicializar características de la tabla (búsqueda, paginación, etc.)
    // En una implementación real, se podría usar DataTables o similar
    console.log('Tabla de PPRs inicializada');
    
    // Agregar funcionalidad a los botones de acción
    addTableButtonListeners();
}

function addTableButtonListeners() {
    // Agregar eventos para los botones de acción en la tabla
    const actionButtons = document.querySelectorAll('.btn-outline-primary, .btn-outline-info, .btn-outline-warning, .btn-outline-danger');
    
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.querySelector('i').className;
            const row = this.closest('tr');
            const codigo = row.cells[0].textContent;
            
            if (action.includes('eye')) {
                viewPprDetails(codigo);
            } else if (action.includes('edit')) {
                editPpr(codigo);
            } else if (action.includes('chart-line')) {
                viewPprProgress(codigo);
            } else if (action.includes('trash')) {
                deletePpr(codigo);
            }
        });
    });
}

function viewPprDetails(codigo) {
    console.log(`Ver detalles del PPR: ${codigo}`);
    // Implementar lógica para ver detalles
    showAlert(`Viendo detalles del PPR: ${codigo}`, 'info');
}

function editPpr(codigo) {
    console.log(`Editar PPR: ${codigo}`);
    // Implementar lógica para edición
    showAlert(`Editando PPR: ${codigo}`, 'info');
}

function viewPprProgress(codigo) {
    console.log(`Ver avances del PPR: ${codigo}`);
    // Implementar lógica para ver avances
    window.location.href = `ppr-progress.html?codigo=${codigo}`;
}

function deletePpr(codigo) {
    if (confirm(`¿Está seguro que desea eliminar el PPR ${codigo}?`)) {
        // Simular eliminación
        console.log(`Eliminar PPR: ${codigo}`);
        showAlert(`PPR ${codigo} eliminado`, 'success');
    }
}

// Función para cargar la lista de PPRs desde el backend
function loadPprList(filters = {}) {
    // En implementación real, llamar al API:
    // const params = new URLSearchParams(filters);
    // return authManager.authenticatedFetch(`/ppr/?${params}`)
    //     .then(response => response.json());
    
    // Simulación
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                success: true,
                data: [
                    { id: 1, codigo: "PPR-001", nombre: "Programa de Salud Materno Infantil", unidad_medida: "% de cobertura", responsable: "Juan Pérez", estado: "activo", avance: 75 },
                    { id: 2, codigo: "PPR-002", nombre: "Educación Básica Rural", unidad_medida: "Número de estudiantes", responsable: "María López", estado: "activo", avance: 45 },
                    { id: 3, codigo: "PPR-003", nombre: "Infraestructura Vial", unidad_medida: "Kilómetros construidos", responsable: "Carlos Gómez", estado: "suspendido", avance: 20 }
                ]
            });
        }, 500);
    });
}