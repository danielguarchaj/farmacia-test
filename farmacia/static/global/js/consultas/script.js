const CrearPacienteForm = (refresh) => {
    const bodyHtml = `
        <p class="card-description mb-3">
        Ingresa los datos del proveedor
        </p>
        <form class="">
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <label for="paciente_nombres">Nombres</label>
                    <input type="text" class="form-control" id="paciente_nombres" placeholder="Nombres">
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <label for="paciente_apellidos">Apellidos</label>
                    <input type="text" class="form-control" id="paciente_apellidos" placeholder="Apellidos">
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <label for="paciente_nacimiento">Fecha de nacimiento</label>
                    <div id="" class="input-group date datepicker datepicker-popup">
                        <input type="text" class="form-control" id="paciente_nacimiento" 
                                onkeypress="return ValidarTeclaEnInput(event, 'datepicker')">
                        <span class="input-group-addon input-group-append border-left">
                            <span class="mdi mdi-calendar input-group-text"></span>
                        </span>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <label for="paciente_telefono">Telefono</label>
                    <input type="text" class="form-control" id="paciente_telefono" placeholder="Telefono">
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
                <div class="form-group">
                    <label for="paciente_origen">Lugar de origen</label>
                    <input type="text" class="form-control" id="paciente_origen" placeholder="Lugar de origen">
                </div>
            </div>
        </div>
        </form>
    `
    const footerHtml = `
        <button type="button" class="btn btn-info btn-rounded btn-fw loader-await" id="btn_crear_paciente">Crear</button>
        <button type="button" class="btn btn-light btn-rounded btn-fw" data-dismiss="modal">Cancelar</button>
    `
    ShowModal('modal', 'Nuevo Paciente', bodyHtml, footerHtml)
    
    InitDatePickers()

    $('#btn_crear_paciente').on('click', async () => {
        const paciente_nombres = $('#paciente_nombres').val()
        const paciente_apellidos = $('#paciente_apellidos').val()
        let paciente_nacimiento = $('#paciente_nacimiento').val()
        const paciente_telefono = $('#paciente_telefono').val()
        const paciente_origen = $('#paciente_origen').val()

        let errores = false
        if (paciente_nombres == '') {
            showDangerToast('El nombre del paciente es requerido')
            errores = true
        }
        if (paciente_apellidos == '') {
            showDangerToast('El apellido del paciente es requerido')
            errores = true
        }

        if (errores)return

        if (paciente_nacimiento == '') paciente_nacimiento = null
        else paciente_nacimiento = moment(paciente_nacimiento, 'DD/MM/Y').format('Y-MM-DD')

        const data = {
            nombres: paciente_nombres,
            apellidos: paciente_apellidos,
            fecha_nacimiento: paciente_nacimiento,
            lugar_origen: paciente_origen,
            telefono: paciente_telefono            
        }
        console.log(data)
        showAlert('warning-message-and-cancel', {
            title: 'Crear Paciente',
            text: 'Esta seguro que quiere crear al paciente?'
        })

        $('.swal-button--confirm').on('click', async function () {
            try {
                MostrarLoader()
                const response = await axios.post('pacientes/', data)
                if (response.status === 201) {
                    OcultarLoader()
                    showAlert('success-message', {
                        title: 'Paciente creado con exito'
                    })
                    $('.btn-success-confirm').on('click', async function () {
                        if (refresh === 'refresh') {
                            await populatePacientesSelect()
                            $('#modal').modal('toggle')
                        } else {
                            location.reload()
                        }
                    })
                }
            } catch (err) {
                OcultarLoader()
                showAlert('error-message', {
                    title: 'No se pudo crear al paciente, intente mas tarde'
                })
            }
        })

    })

}

const PacienteDetalle = async pacienteId => {
    const bodyHtml = `
        <p class="card-description mb-3">
        Ingresa los datos del proveedor
        </p>
        <form class="">
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <label for="paciente_nombres">Nombres</label>
                    <input type="text" class="form-control" id="paciente_nombres" placeholder="Nombres">
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <label for="paciente_apellidos">Apellidos</label>
                    <input type="text" class="form-control" id="paciente_apellidos" placeholder="Apellidos">
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
                    <label for="paciente_nacimiento">Fecha de nacimiento</label>
                    <div id="datepicker-popup" class="input-group date datepicker">
                        <input type="text" class="form-control" id="paciente_nacimiento" 
                                onkeypress="return ValidarTeclaEnInput(event, 'datepicker')">
                        <span class="input-group-addon input-group-append border-left">
                            <span class="mdi mdi-calendar input-group-text"></span>
                        </span>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-group">
                    <label for="paciente_telefono">Telefono</label>
                    <input type="text" class="form-control" id="paciente_telefono" placeholder="Telefono">
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
                <div class="form-group">
                    <label for="paciente_origen">Lugar de origen</label>
                    <input type="text" class="form-control" id="paciente_origen" placeholder="Lugar de origen">
                </div>
            </div>
        </div>
        </form>
    `
    const footerHtml = `
        <button type="button" class="btn btn-info btn-rounded btn-fw loader-await adminonly" id="btn_editar_paciente">Guardar Cambios</button>
        <button type="button" class="btn btn-light btn-rounded btn-fw" data-dismiss="modal">Cancelar</button>
    `
    ShowModal('modal', 'Detalle del Paciente', bodyHtml, footerHtml)
    await ValidarPermisos()
    try {
        MostrarLoader()
        const {data} = await axios.get(`pacientes/${pacienteId}/`)
        $('#paciente_nombres').val(data.nombres)
        $('#paciente_apellidos').val(data.apellidos)
        $('#paciente_telefono').val(data.telefono)
        $('#paciente_origen').val(data.lugar_origen)
        if (data.fecha_nacimiento == null) $('#paciente_nacimiento').val('')
        else $('#paciente_nacimiento').val(
            moment(data.fecha_nacimiento, 'Y-MM-DD').format('DD/MM/Y')
        )
        OcultarLoader()
    }catch (err) {
        OcultarLoader()
        showAlert('error-message', {
            title: 'No se pudieron cargar los datos del paciente, intente mas tarde'
        })
    }

    InitDatePickers()

    $('#btn_editar_paciente').on('click', async () => {
        const paciente_nombres = $('#paciente_nombres').val()
        const paciente_apellidos = $('#paciente_apellidos').val()
        let paciente_nacimiento = $('#paciente_nacimiento').val()
        const paciente_telefono = $('#paciente_telefono').val()
        const paciente_origen = $('#paciente_origen').val()

        if (paciente_nombres == '') {
            showDangerToast('El nombre del paciente es requerido')
            return
        }

        if (paciente_nacimiento == '') paciente_nacimiento = null
        else paciente_nacimiento = moment(paciente_nacimiento, 'DD/MM/Y').format('Y-MM-DD')

        const data = {
            nombres: paciente_nombres,
            apellidos: paciente_apellidos,
            fecha_nacimiento: paciente_nacimiento,
            lugar_origen: paciente_origen,
            telefono: paciente_telefono
        }

        showAlert('warning-message-and-cancel', {
            title: 'Editar Paciente',
            text: 'Esta seguro que quiere editar al paciente?'
        })

        $('.swal-button--confirm').on('click', async function () {
            try {
                MostrarLoader()
                const response = await axios.patch(`pacientes/${pacienteId}/`, data)
                if (response.status === 200) {
                    OcultarLoader()
                    showAlert('success-message', {
                        title: 'Paciente editado con exito'
                    })
                    $('.btn-success-confirm').on('click', async function () {
                        $('#modal').modal('toggle')
                        location.reload()
                    })
                }
            } catch (err) {
                OcultarLoader()
                showAlert('error-message', {
                    title: 'No se pudo editar al paciente, intente mas tarde'
                })
            }
        })

    })

}