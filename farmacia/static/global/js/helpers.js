function LimpiarCampos(clase) {
    if (clase){ 
        $(clase).val('')
    }
    $('.input-limpiable').val('')
    $('.select-limpiable').val(0)
    $(".select-2").select2({
        theme: "bootstrap",
        width: 'auto',
        dropdownAutoWidth: true
    });
}

const MostrarLoader = () => {
    $('.square-box-loader').show()
    $('.loader-await').hide()
}

const OcultarLoader = () => {
    $('.square-box-loader').hide()
    $('.loader-await').show()
}

const ShowModal = (modalId, title, body, footer, size) => {
    $(`#${modalId}-title`).html(title)
    $(`#${modalId}-body`).html(body)
    $(`#${modalId}-footer`).html(footer)
    if (size) $('.modal-dialog').addClass(size)
}

const populatePacientesSelect = async () => {
    try {
        MostrarLoader()
        const {
            data
        } = await axios.get('pacientes/')
        const selectPacientesHtml = data.reduce(
            (acc, paciente) => acc += `
                <option value="${paciente.id}">${paciente.nombres} ${paciente.apellidos}</option>
            `,
            '<option value="0" disabled selected>Seleccione al paciente</option>'
        )
        $('#consulta_paciente').html(selectPacientesHtml)
        $(".select-2").select2({
            theme: "bootstrap",
            width: 'auto',
            dropdownAutoWidth: true
        })
        OcultarLoader()
    } catch (err) {
        OcultarLoader()
        showAlert('error-message', {title: 'No se pudieron cargar los pacientes, intente mas tarde'})
    }
}

const populateUsersSelect = async () => {
    try {
        MostrarLoader()
        const {
            data
        } = await axios.get('users/')
        const selectUsersHtml = data.reduce(
            (acc, user) => acc += `
                <option value="${user.id}">${user.nombres} ${user.apellidos}</option>
            `,
            '<option value="0" disabled selected>Seleccione al usuario</option>'
        )
        $('#users_select').html(selectUsersHtml)
        $(".select-2").select2({
            theme: "bootstrap",
            width: 'auto',
            dropdownAutoWidth: true
        });
        OcultarLoader()
    } catch (err) {
        OcultarLoader()
        showAlert('error-message', {
            title: 'No se pudieron cargar los usuarios, intente mas tarde'
        })
    }
}

const getUrlParameter = () => {
    let id = window.location.pathname
    id = id.split('/')
    id = id[id.length - 2]
    return id
}

const parseDateFormat = (date) => {
    let date_parsed = date.split('/')
    return date_parsed[2] + '-' + date_parsed[1] + '-' + date_parsed[0]
}

const ValidarPermisos = async () => {
    if (localStorage.user) 
        $('.nav-profile-name').html(localStorage.user)
    $('.dot-opacity-loader').show()
    try {
        const {data} = await axios.get('user/current/')
        $('.nav-profile-name').html(`${data.nombres} ${data.apellidos}`)
        $('.dot-opacity-loader').hide()
        localStorage.user = `${data.nombres} ${data.apellidos}`
        if (data.tipo != 0) $('.adminonly').remove()
        else if (data.tipo == 0) $('.vendedoronly').remove()
    } catch (err) {
        console.log(err)
        showAlert('error-message', {title: 'Error de autenticacion, inicie sesion.'})
    }
}

const getExistenciaActual = async (loteId, loteCantidadComprada) => {
    const loteUnidadesVendidas = await axios.get(`lotes/ventas/${loteId}/`)
    const existenciaActual = Number(loteCantidadComprada) - Number(loteUnidadesVendidas.data.total)
    return existenciaActual
}