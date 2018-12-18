const crearProveedorForm = (refresh) => {
    const bodyHtml = `
        <p class="card-description mb-3">
        Ingresa los datos del proveedor
        </p>
        <form class="">
        <div class="form-group">
            <label for="proveedor_nombre">Nombre</label>
            <input type="text" class="form-control" id="proveedor_nombre" placeholder="Nombre del proveedor">
        </div>
        <div class="form-group">
            <label for="proveedor_telefono">Telefono</label>
            <input type="text" class="form-control" id="proveedor_telefono" placeholder="Telefono">
        </div>
        <div class="form-group">
            <label for="proveedor_direccion">Direccion</label>
            <input type="text" class="form-control" id="proveedor_direccion" placeholder="Direccion">
        </div>
        <div class="form-group">
            <label for="proveedor_email">Email</label>
            <input type="email" class="form-control" id="proveedor_email" placeholder="Email">
        </div>
        </form>
    `
    const footerHtml = `
        <button type="button" class="btn btn-info btn-rounded btn-fw loader-await" id="btn_crear_proveedor">Crear</button>
        <button type="button" class="btn btn-light btn-rounded btn-fw" data-dismiss="modal">Cancelar</button>
    `
    ShowModal('modal', 'Nuevo Proveedor', bodyHtml, footerHtml)

    $('#btn_crear_proveedor').on('click', async () => {
        const proveedor_nombre = $('#proveedor_nombre').val()
        const proveedor_telefono = $('#proveedor_telefono').val()
        const proveedor_direccion = $('#proveedor_direccion').val()
        const proveedor_email = $('#proveedor_email').val()

        if ( proveedor_nombre == '') {
            showDangerToast('El nombre del proveedor es requerido')
            return
        }

        const data = {
            nombre: proveedor_nombre,
            telefono: proveedor_telefono,
            direccion: proveedor_direccion,
            email: proveedor_email
        }

        showAlert('warning-message-and-cancel', {
            title: 'Crear Proveedor',
            text: 'Esta seguro que quiere crear al proveedor?'
        })

        $('.swal-button--confirm').on('click', async function() {            
            try {
                MostrarLoader()
                console.log(data)
                const response = await axios.post('proveedores/', data)
                if (response.status === 201) {
                    OcultarLoader()
                    showAlert('success-message', {
                        title: 'Proveedor creado con exito'
                    })
                    $('.btn-success-confirm').on('click', async function () {
                        if (refresh === 'refresh') {
                            await getProveedores()
                            $('#modal').modal('toggle')
                        }else{
                            location.reload()
                        }
                    })
                }
            } catch (err) {
                OcultarLoader()
                showAlert('error-message', {title: 'No se pudo crear el proveedor, intente mas tarde'})
                console.log(err)
            }
        })

    })

}