document.addEventListener('DOMContentLoaded', function () {
    const selectorVoluntarios = document.getElementById('selector-voluntarios');
    const todosLosSlots = document.querySelectorAll('.organigrama div, .vehiculo td');
    let voluntarioSeleccionado = null;
    const organigramaContainer = document.querySelector('.organigrama-container');
    const organigrama = document.querySelector('.organigrama');
    let scale = 1;
    let isDragging = false;
    let startX, startY, scrollLeft, scrollTop;
    const zoomInButton = document.getElementById('zoom-in');
    const zoomOutButton = document.getElementById('zoom-out');

    zoomInButton.addEventListener('click', function () {
        scale += 0.1;
        applyZoom();
    });

    zoomOutButton.addEventListener('click', function () {
        scale -= 0.1;
        if (scale < 0.5) scale = 0.5; // Prevenir zoom out excesivo
        applyZoom();
    });

    function applyZoom() {
        organigrama.style.transform = `scale(${scale})`;
        organigramaContainer.classList.toggle('zoomable', scale > 1);
    }

    // Funcionalidad de arrastre
    organigramaContainer.addEventListener('mousedown', startDragging);
    organigramaContainer.addEventListener('mousemove', drag);
    organigramaContainer.addEventListener('mouseup', stopDragging);
    organigramaContainer.addEventListener('mouseleave', stopDragging);

    function startDragging(e) {
        if (scale > 1) {
            isDragging = true;
            startX = e.pageX - organigramaContainer.offsetLeft;
            startY = e.pageY - organigramaContainer.offsetTop;
            scrollLeft = organigramaContainer.scrollLeft;
            scrollTop = organigramaContainer.scrollTop;
        }
    }

    function drag(e) {
        if (!isDragging) return;
        e.preventDefault();
        const x = e.pageX - organigramaContainer.offsetLeft;
        const y = e.pageY - organigramaContainer.offsetTop;
        const walkX = (x - startX) * 2;
        const walkY = (y - startY) * 2;
        organigramaContainer.scrollLeft = scrollLeft - walkX;
        organigramaContainer.scrollTop = scrollTop - walkY;
    }

    function stopDragging() {
        isDragging = false;
    }


    selectorVoluntarios.addEventListener('change', function () {
        voluntarioSeleccionado = this.value;
        todosLosSlots.forEach(slot => {
            if (!slot.classList.contains('asignado')) {
                slot.classList.toggle('seleccionable', !!voluntarioSeleccionado);
            }
        });
    });

    todosLosSlots.forEach(slot => {
        slot.dataset.textoOriginal = slot.textContent.trim();
        if (slot.textContent.includes('GRUPO DE INTERVENCION')) {
            return;
        }
        slot.addEventListener('click', function () {
            if (voluntarioSeleccionado && !this.classList.contains('asignado')) {
                const voluntarioNombre = selectorVoluntarios.options[selectorVoluntarios.selectedIndex].text;
                this.dataset.voluntarioId = voluntarioSeleccionado;
                this.dataset.voluntarioNombre = voluntarioNombre;

                const voluntarioSpan = document.createElement('span');
                voluntarioSpan.textContent = voluntarioNombre;
                voluntarioSpan.classList.add('voluntario-asignado');

                this.innerHTML = '';
                this.appendChild(document.createTextNode(this.dataset.textoOriginal));
                this.appendChild(document.createElement('br'));
                this.appendChild(voluntarioSpan);

                this.classList.add('asignado');
                this.classList.remove('seleccionable');
                selectorVoluntarios.remove(selectorVoluntarios.selectedIndex);
                voluntarioSeleccionado = null;
                selectorVoluntarios.value = '';

            } else if (this.classList.contains('asignado')) {
                const voluntarioId = this.dataset.voluntarioId;
                const voluntarioNombre = this.dataset.voluntarioNombre;

                const nuevaOpcion = new Option(voluntarioNombre, voluntarioId);
                selectorVoluntarios.add(nuevaOpcion);

                const opciones = Array.from(selectorVoluntarios.options).slice(1);
                opciones.sort((a, b) => a.text.localeCompare(b.text));
                selectorVoluntarios.innerHTML = '<option value="">Seleccione un voluntario</option>';
                opciones.forEach(opcion => selectorVoluntarios.add(opcion));

                this.textContent = this.dataset.textoOriginal;
                this.classList.remove('asignado');
                delete this.dataset.voluntarioId;
                delete this.dataset.voluntarioNombre;
            }
        });
    });
    const printButton = document.getElementById('print');
    printButton.addEventListener('click', function () {
        window.print();
    });
});

