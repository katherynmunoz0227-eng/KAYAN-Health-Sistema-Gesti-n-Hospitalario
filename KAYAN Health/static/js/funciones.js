console.log("Archivo JS cargado correctamente");

// --- Control de submenús del sidebar ---
document.querySelectorAll('.toggle-submenu').forEach(function(link) {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const parent = link.closest('.has-sub');
        parent.classList.toggle('submenu-open');
    });
});
