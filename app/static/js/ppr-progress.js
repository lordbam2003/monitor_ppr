// ppr-progress.js - Funcionalidad para la página de avance de PPR

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráficos
    initProgressCharts();
    
    // Inicializar otras funcionalidades
    initProgressPage();
});

function initProgressPage() {
    console.log('Página de avance de PPR inicializada');
    
    // Proteger la página si el usuario no está autenticado
    if (!authManager.isAuthenticated()) {
        window.location.href = 'index.html';
    }
    
    // Obtener el código del PPR de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const pprCodigo = urlParams.get('codigo');
    
    if (pprCodigo) {
        console.log('Código de PPR:', pprCodigo);
        loadPprProgressData(pprCodigo);
    }
    
    // Añadir event listeners
    addProgressEventListeners();
}

function loadPprProgressData(pprCodigo) {
    // En implementación real, llamar al API para obtener datos específicos del PPR
    console.log(`Cargando datos de avance para PPR: ${pprCodigo}`);
    
    // Simular carga de datos
    setTimeout(() => {
        updatePprInfo(pprCodigo);
    }, 500);
}

function updatePprInfo(pprCodigo) {
    // Simular actualización de información del PPR
    document.querySelector('.card-title').textContent = `Programa de Salud Materno Infantil (${pprCodigo})`;
    document.querySelector('.card-text').textContent = `Este programa tiene como objetivo mejorar la salud materna e infantil en zonas rurales. Código: ${pprCodigo}`;
}

function initProgressCharts() {
    // Gráfico de avance mensual
    const monthlyCtx = document.getElementById('monthlyProgressChart').getContext('2d');
    
    const monthlyData = {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago'],
        datasets: [{
            label: 'Avance %',
            data: [85, 90, 83, 88, 90, 92, 93, 94],
            borderColor: '#0d6efd',
            backgroundColor: 'rgba(13, 110, 253, 0.1)',
            fill: true,
            tension: 0.3
        }]
    };
    
    new Chart(monthlyCtx, {
        type: 'line',
        data: monthlyData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Avance Mensual del PPR'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
    
    // Gráfico de comparativo programado vs ejecutado
    const comparisonCtx = document.getElementById('comparisonChart').getContext('2d');
    
    const comparisonData = {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago'],
        datasets: [
            {
                label: 'Programado',
                data: [10, 20, 30, 40, 50, 60, 70, 80],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                type: 'line'
            },
            {
                label: 'Ejecutado',
                data: [8.5, 18, 25, 35, 45, 55, 65, 75],
                borderColor: '#ffc107',
                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                type: 'line'
            }
        ]
    };
    
    new Chart(comparisonCtx, {
        type: 'bar',
        data: comparisonData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Comparativo Programado vs Ejecutado'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function addProgressEventListeners() {
    // Event listener para botones de edición
    const editButtons = document.querySelectorAll('.btn-outline-info');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const month = row.cells[0].textContent;
            const target = row.cells[1].textContent;
            const actual = row.cells[2].textContent;
            
            console.log(`Editar avance para ${month}: Programado ${target}, Ejecutado ${actual}`);
            
            // Implementar modal o formulario para edición
            editMonthlyProgress(month, target, actual);
        });
    });
}

function editMonthlyProgress(month, target, actual) {
    // Mostrar modal o formulario para editar avance mensual
    const newActual = prompt(`Editar valor ejecutado para ${month} (actual: ${actual}):`, actual);
    
    if (newActual !== null) {
        // En implementación real, actualizaría el backend
        console.log(`Nuevo valor para ${month}: ${newActual}`);
        
        // Actualizar la fila en la tabla
        const row = event.target.closest('tr');
        row.cells[2].textContent = newActual;
        
        // Recalcular el porcentaje
        const targetVal = parseFloat(row.cells[1].textContent);
        const actualVal = parseFloat(newActual);
        const percentage = targetVal > 0 ? Math.round((actualVal / targetVal) * 100) : 0;
        row.cells[3].textContent = `${percentage}%`;
        
        // Actualizar estado
        const statusBadge = row.querySelector('.badge');
        if (percentage >= 95) {
            statusBadge.className = 'badge bg-success';
            statusBadge.textContent = 'OK';
        } else if (percentage >= 80) {
            statusBadge.className = 'badge bg-warning';
            statusBadge.textContent = 'Parcial';
        } else {
            statusBadge.className = 'badge bg-danger';
            statusBadge.textContent = 'Bajo';
        }
        
        // Mostrar mensaje de éxito
        showAlert(`Avance para ${month} actualizado`, 'success');
    }
}

// Función para cargar datos de avance desde el backend
async function fetchPprProgress(codigoPpr) {
    // En implementación real:
    // return authManager.authenticatedFetch(`/ppr/${codigoPpr}/avances`)
    //     .then(response => response.json());
    
    // Simulación
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                success: true,
                ppr: {
                    codigo: codigoPpr,
                    nombre: "Programa de Salud Materno Infantil",
                    descripcion: "Este programa tiene como objetivo mejorar la salud materna e infantil en zonas rurales.",
                    unidad_medida: "% de cobertura",
                    estado: "activo",
                    ano_ejecucion: 2024
                },
                progress: [
                    { mes: "Enero", programado: 10, ejecutado: 8.5, comentario: "Ligero retraso por permisos" },
                    { mes: "Febrero", programado: 20, ejecutado: 18, comentario: "Avance dentro de lo esperado" },
                    { mes: "Marzo", programado: 30, ejecutado: 25, comentario: "Problemas de suministro" },
                    { mes: "Abril", programado: 40, ejecutado: 35, comentario: "Recuperación del retraso anterior" },
                    { mes: "Mayo", programado: 50, ejecutado: 45, comentario: "Buen avance en este periodo" },
                    { mes: "Junio", programado: 60, ejecutado: 55, comentario: "Avance consistente" },
                    { mes: "Julio", programado: 70, ejecutado: 65, comentario: "Avance por encima del planificado" },
                    { mes: "Agosto", programado: 80, ejecutado: 75, comentario: "Muy buen desempeño" }
                ],
                total_avance: 75 // Porcentaje total de avance
            });
        }, 800);
    });
}