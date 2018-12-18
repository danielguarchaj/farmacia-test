const DetalleDetalleVenta = async (loteId, detalleId) => {
    const bodyHtml = `
        <p class="card-description mb-3" id="lote_seleccionado"></p>
        <p class="card-description mb-3" id="lote_marca_seleccionado"></p>
        <p class="card-description mb-3" id="lote_disponibilidad_seleccionado"></p>
        <p class="card-description mb-3" id="lote_vencimiento_seleccionado"></p>
        <p class="card-description mb-3" id="lote_precio_venta_original"></p>
        <hr>
        <form class="">
            <div class="row">
                <div class="form-group col-sm-6">
                    <label for="venta_cantidad"><b>Cantidad Vendida</b></label>
                    <input type="text" class="form-control" id="venta_cantidad" placeholder="Cantidad a vender"
                            onkeypress="return ValidarTeclaEnInput(event, 'int')">
                </div>
                <div class="form-group col-sm-6">
                    <label for="venta_precio_real"><b>Precio de Venta</b></label>
                    <input type="text" class="form-control" id="venta_precio_real" placeholder="Precio Venta"
                            onkeypress="return ValidarTeclaEnInput(event, 'decimal')">
                </div>
            </div>
        </form>
    `
    const footerHtml = `
        <button type="button" class="btn btn-info btn-rounded btn-fw loader-await adminonly" id="btn_editar_detalle_venta">Guardar Cambios</button>
        <button type="button" class="btn btn-light btn-rounded btn-fw" data-dismiss="modal">Cancelar</button>
    `
    ShowModal('modal', 'Detalle de lote vendido', bodyHtml, footerHtml)
    await ValidarPermisos()
    let existenciaActual = 0
    let detalleVentaResponse = {}
    try {
        MostrarLoader()
        const {
            data
        } = await axios.get(`lotes-detailed/${loteId}/`)
        existenciaActual = await getExistenciaActual(data.id, data.cantidad_comprada)
        detalleVentaResponse = await axios.get(`detalles-venta/${detalleId}/`)
        existenciaActual = await getExistenciaActual(data.id, data.cantidad_comprada)
        $('#lote_seleccionado').html(`<b>Producto: </b>
            ${data.producto.nombre} -
            ${data.producto.presentacion.nombre} -
            ${data.producto.presentacion.descripcion}
        `)
        $('#lote_marca_seleccionado').html(`<b>Producto: </b> ${data.producto.marca.nombre}`)
        $('#lote_disponibilidad_seleccionado').html('<b>Disponibilidad: </b> ' + existenciaActual)
        if (data.fecha_vencimiento) $('#lote_vencimiento_seleccionado').html('<b>Fecha de vencimiento: </b>' +
            moment(data.fecha_vencimiento, 'Y-MM-DD').format('DD/MM/Y'))
        $('#lote_precio_venta_original').html(`<b>Precio Original: </b> Q${data.producto.precio_venta}`)
        $('#venta_precio_real').val(data.producto.precio_venta)
        $('#venta_cantidad').val(detalleVentaResponse.data.cantidad)
        OcultarLoader()

    } catch (err) {
        console.log(err)
        OcultarLoader()
        showAlert('error-message', {
            title: 'No se pudo cargar la informacion del lote vendido seleccionado'
        })
    }

     $('#btn_editar_detalle_venta').on('click', async () => {
        showAlert('warning-message-and-cancel', {
            title: 'Guardar Cambios',
            text: 'Esta seguro que desea guardar los cambios en este elemento de la venta?'
        })
        $('.swal-button--confirm').on('click', async () => {

            const precio_venta = $('#venta_precio_real').val()
            const cantidad = $('#venta_cantidad').val()
            let errors = false
            if (precio_venta === '') {
                showDangerToast('Ingrese el precio de venta')
                errors = true
            }
            if (Number(cantidad) < 1 || cantidad === '') {
                showDangerToast('Ingrese una cantidad valida')
                errors = true
            }
            if ( Number(cantidad) > Number(existenciaActual) && Number(detalleVentaResponse.data.cantidad) < Number(existenciaActual) ) {
                showDangerToast('No existen suficientes productos para suplir la venta.')
                errors = true
            }
   
            if (errors) return
   
            try {
               const nuevoSubtotal = (Number(cantidad) * Number(precio_venta)).toFixed(2)
               const response = await axios.patch(`detalles-venta/update/${detalleId}/`, {
                    cantidad: cantidad,
                    precio_venta_real: Number(precio_venta).toFixed(2),
                    subtotal: nuevoSubtotal
               })
               const nuevoTotal = (Number(venta.total) - Number(detalleVentaResponse.data.subtotal)) + Number(nuevoSubtotal)
               const responseUpdateVenta = await axios.patch(`ventas/update/${venta.id}/`, {
                   total: nuevoTotal
               })
               if (responseUpdateVenta.status === 200){
                   showAlert('success-message', {
                       title: 'Venta editada con exito'
                   })
                   $('.btn-success-confirm').on('click', function () {
                       location.reload()
                   })
               }
            } catch(err) {
                console.log(err)
                showAlert('error-message', {title: 'No se pudo editar el lote vendido, intente nuevamente'})             
            }
        })
     })
}

const DetalleVentaEliminar = async (detalleVentaId) => {
    showAlert('warning-message-and-cancel', {
        title: 'Eliminar Venta',
        text: 'Esta seguro que desea eliminar la venta?'
    })
    $('.swal-button--confirm').on('click', async () => {
        try {
            MostrarLoader()
            const responseDetalleVenta = await axios.get(`detalles-venta/${detalleVentaId}/`)
            const nuevoTotal = (Number(venta.total) - Number(responseDetalleVenta.data.subtotal)).toFixed(2)
            const response = await axios.patch(`ventas/update/${venta.id}/`, {
                total: nuevoTotal
            })
            const deleteDetalleResponse = await axios.patch(`detalles-venta/update/${detalleVentaId}/`, {
                estado: 2
            })
            if (deleteDetalleResponse.status === 200){
                showAlert('success-message', {
                    title: 'Elemento de la venta eliminado',
                    button: {
                        text: 'Continuar'
                    }
                })
            }
            OcultarLoader()
            $('.btn-success-confirm').on('click', () => {
                location.reload()
            })
        } catch (err) {
            OcultarLoader()
            showAlert('error-message', {
                title: 'No se pudo eliminar el elemento de la venta, intente nuevamente'
            })
            console.log(err)
        }
    })
}