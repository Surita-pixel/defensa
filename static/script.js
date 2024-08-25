document.addEventListener('DOMContentLoaded', function () {
    const selectores = document.querySelectorAll('.select-group select');
    const todosLosSlots = document.querySelectorAll('.organigrama div, .vehiculo td');
    let voluntarioSeleccionado = null;
    let categoriaSeleccionada = null;
    const organigramaContainer = document.querySelector('.organigrama-container');
    const organigrama = document.querySelector('.organigrama');
    let scale = 1;
    let isDragging = false;
    let startX, startY, scrollLeft, scrollTop;
    const zoomInButton = document.getElementById('zoom-in');
    const zoomOutButton = document.getElementById('zoom-out');
    const vehiculos = document.querySelectorAll('.vehiculo');

    // Guardar el texto original de las celdas de vehículos
    vehiculos.forEach(vehiculo => {
        const celdas = vehiculo.querySelectorAll('td');
        celdas.forEach(celda => {
            celda.dataset.textoOriginal = celda.textContent.trim();
        });
    });

    zoomInButton.addEventListener('click', function () {
        scale += 0.1;
        applyZoom();
    });

    zoomOutButton.addEventListener('click', function () {
        scale -= 0.1;
        if (scale < 0.5) scale = 0.5;
        applyZoom();
    });

    function applyZoom() {
        organigrama.style.transform = `scale(${scale})`;
        organigramaContainer.classList.toggle('zoomable', scale > 1);
    }

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

    selectores.forEach(selector => {
        selector.addEventListener('change', function () {
            voluntarioSeleccionado = this.value;
            categoriaSeleccionada = this.dataset.categoria;
            todosLosSlots.forEach(slot => {
                if (!slot.classList.contains('asignado')) {
                    const esSeleccionable = esSlotSeleccionable(slot, categoriaSeleccionada);
                    slot.classList.toggle('seleccionable', esSeleccionable && !!voluntarioSeleccionado);
                }
            });
        });
    });

    function esSlotSeleccionable(slot, categoria) {
        const textoSlot = slot.dataset.textoOriginal.toUpperCase();
        switch (categoria) {
            case 'operaciones':
                return textoSlot.includes('RESCATISTA') || textoSlot.includes('LIDER GRUPO') || textoSlot.includes('OPERACIONES');
            case 'seguridad':
                return textoSlot.includes('SEGURIDAD') || textoSlot.includes('AUXILIAR SEGURIDAD');
            case 'planeacion':
                return textoSlot.includes('PLANEACION');
            case 'logistica':
                return textoSlot.includes('LOGISTICA') || textoSlot.includes('ASISTENTE LOGISTICA');
            case 'unidad-medica':
                return textoSlot.includes('UNIDAD MEDICA') || textoSlot.includes('AUXILIAR ENFERMERIA');
            case 'comunicacion':
                return textoSlot.includes('COMUNICACION');
            default:
                return false;
        }
    }

    todosLosSlots.forEach(slot => {
        slot.dataset.textoOriginal = slot.textContent.trim();
        if (slot.textContent.includes('GRUPO DE INTERVENCION')) {
            return;
        }
        slot.addEventListener('click', function () {
            if (voluntarioSeleccionado && !this.classList.contains('asignado') && esSlotSeleccionable(this, categoriaSeleccionada)) {
                const selectorActual = document.querySelector(`select[data-categoria="${categoriaSeleccionada}"]`);
                const voluntarioNombre = selectorActual.options[selectorActual.selectedIndex].text;
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
                selectorActual.remove(selectorActual.selectedIndex);
                voluntarioSeleccionado = null;
                categoriaSeleccionada = null;
                selectorActual.value = '';

                // Actualizar las tablas de vehículos
                const celdaVehiculo = document.querySelector(`td[data-vehiculo="${this.id}"]`);
                if (celdaVehiculo) {
                    celdaVehiculo.dataset.voluntarioId = this.dataset.voluntarioId;
                    celdaVehiculo.dataset.voluntarioNombre = this.dataset.voluntarioNombre;
                    celdaVehiculo.dataset.textoOriginal = celdaVehiculo.dataset.textoOriginal || celdaVehiculo.textContent.trim();
                    celdaVehiculo.innerHTML = `${voluntarioNombre}`;
                }

            } else if (this.classList.contains('asignado')) {
                const voluntarioId = this.dataset.voluntarioId;
                const voluntarioNombre = this.dataset.voluntarioNombre;

                // Encontrar el selector correcto basado en el texto del slot
                let selectorCorrespondiente;
                for (const selector of selectores) {
                    if (esSlotSeleccionable(this, selector.dataset.categoria)) {
                        selectorCorrespondiente = selector;
                        break;
                    }
                }

                if (selectorCorrespondiente) {
                    const nuevaOpcion = new Option(voluntarioNombre, voluntarioId);
                    selectorCorrespondiente.add(nuevaOpcion);

                    const opciones = Array.from(selectorCorrespondiente.options).slice(1);
                    opciones.sort((a, b) => a.text.localeCompare(b.text));
                    selectorCorrespondiente.innerHTML = '<option value="">Seleccione un voluntario</option>';
                    opciones.forEach(opcion => selectorCorrespondiente.add(opcion));
                }

                this.textContent = this.dataset.textoOriginal;
                this.classList.remove('asignado');
                delete this.dataset.voluntarioId;
                delete this.dataset.voluntarioNombre;

                // Remover de las tablas de vehículos
                const celdaVehiculo = document.querySelector(`td[data-vehiculo="${this.id}"]`);
                if (celdaVehiculo) {
                    celdaVehiculo.textContent = celdaVehiculo.dataset.textoOriginal || '';
                    delete celdaVehiculo.dataset.voluntarioId;
                    delete celdaVehiculo.dataset.voluntarioNombre;
                }
            }
        });
    });
    const printButton = document.getElementById('print');
    printButton.addEventListener('click', function () {
        // Guarda el contenido original
        const bodyHTML = document.body.innerHTML;

        // Crea un nuevo contenido solo con el organigrama
        let printContent = '<div class="organigrama-container" style="page-break-after: always;">'
            + document.querySelector('.organigrama-container').innerHTML
            + '</div>';

        // Agrega un salto de página antes de cada tabla y crea el contenido de impresión
        document.querySelectorAll('.vehiculo').forEach(vehiculo => {
            printContent += '<div class="vehiculo" style="page-break-before: always;">'
                + vehiculo.outerHTML
                + '</div>';
        });

        // Reemplaza el contenido del body
        document.body.innerHTML = printContent;

        // Imprime
        window.print();

        // Restaura el contenido original
        document.body.innerHTML = bodyHTML;
    });

});