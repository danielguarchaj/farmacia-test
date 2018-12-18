const getProveedores = async () => {
    try {
        MostrarLoader()
        const {
            data
        } = await axios.get('proveedores/')
        if (!data[0]) showAlert('error-message', {
            title: 'No existen proveedores registrados'
        })
        const selectProveedoresHtml = data.reduce(
            (acc, proveedor) => acc += `
            <option value="${proveedor.id}">${proveedor.id} - ${proveedor.nombre}</option>
            `,
            '<option value="0" disabled selected>Seleccione el proveedor de la compra</option>'
        )
        $('#compra_proveedor').html(selectProveedoresHtml)
        $(".select-2").select2({
            theme: "bootstrap",
            width: 'auto',
            dropdownAutoWidth: true
        });
        OcultarLoader()
    } catch (err) {
        OcultarLoader()
        showAlert('error-message', {
            title: 'No se pudieron cargar los proveedores, intente mas tarde'
        })
    }
}

const getProductosSelectCompras = async () => {
    try {
        MostrarLoader()
        const {
            data
        } = await axios.get('productos/')
        if (!data[0]) showAlert('error-message', {
            title: 'No existen productos registrados'
        })
        const selectProductosHtml = data.reduce(
            (acc, producto) => acc += `
            <option value="${producto.id}">
                ${producto.id} -
                ${producto.nombre} -
                ${producto.marca.nombre} -
                ${producto.presentacion.nombre}
            </option>
            `,
            '<option value="0" disabled selected>Seleccione el producto a comprar</option>'
        )
        $('#lote_producto').html(selectProductosHtml)
        $(".select-2").select2({
            theme: "bootstrap",
            width: 'auto',
            dropdownAutoWidth: true
        });
        OcultarLoader()
    } catch (err) {
        OcultarLoader()
        showAlert('error-message', {
            title: 'No se pudieron cargar los productos, intente mas tarde'
        })
    }
}


const CompraEliminar = async (compraId) => {
    let redirect = ''
    if (!compraId) {
        compraId = getUrlParameter()
        redirect = '/compras/'
    }
    showAlert('warning-message-and-cancel', {
        title: 'Eliminar Compra',
        text: 'Esta seguro que desea eliminar la compra?'
    })
    $('.swal-button--confirm').on('click', async () => {
        try {
            MostrarLoader()
            for (lote of lotes){
                await axios.patch(`lotes/${lote.id}/`, { estado: 2 })    
            }
            const response = await axios.patch(`compras/update/${compraId}/`, { estado: 2 })
            showAlert('success-message', {
                title: 'Compra eliminada',
                button: {
                    text: 'Continuar'
                }
            })
            OcultarLoader()
            $('.btn-success-confirm').on('click', () => {
                if (redirect == '') location.reload()
                else window.location.href = redirect
            })

        } catch (err) {
            OcultarLoader()
            showAlert('error-message', { title: 'No se pudo eliminar la compra, intente nuevamente' })
        }
    })
}

const LoteEliminar = loteId => {
    showAlert('warning-message-and-cancel', {
        title: 'Eliminar Lote',
        text: 'Esta seguro que desea eliminar el lote?'
    })
    $('.swal-button--confirm').on('click', async () => {
        for (lote of lotes) {
            if ( lote.id == loteId) {
                $(`#tr${loteId}`).remove()
                lotesEliminar.push(loteId)
                let currentPage = window.location.pathname
                currentPage = currentPage.split('/')
                if ( currentPage[currentPage.length - 3]==='compras' ) {
                    total = total - lote.subtotal
                    $('#total').html('Total de la compra: Q'+Number(total).toFixed(2))
                }
                else if (currentPage[currentPage.length - 3] === 'productos') {
                    let totalExistenciasActual = $('#total-existencias').text()
                    totalExistenciasActual = totalExistenciasActual.split(':')
                    totalExistenciasActual = Number(totalExistenciasActual[totalExistenciasActual.length-1])
                    const loteExistencias = await getExistenciaActual(lote.id, lote.cantidad_comprada)
                    $('#total-existencias').html('Total de existencias : '+ (Number(totalExistenciasActual) - Number(loteExistencias).toFixed(2)) )
                }
            }
        }
    })
}
const LoteDetalle = async (loteId) => {
    const bodyHtml = `
        <form class="form-sample">
            <p class="card-description" id="existencias"></p>
            <hr>
            <div class="col-sm-12 row">
                <div class="form-group col-sm-12">
                    <label>Producto</label>
                    <select class="select-2 select-limpiable" id="lote_producto"></select>
                </div>
            </div>
            <div class="col-sm-12 row">
                <div class="form-group col-sm-12">
                    <label>Observaciones</label>
                    <textarea class="form-control input-limpiable" id="lote_observaciones"></textarea>
                </div>
            </div>
            <div class="col-sm-12 row">
                <div class="form-group col-sm-6 mt-3">
                    <label for="lote_producto_vencimiento">Fecha de vencimiento</label>
                    <div id="" class="input-group date datepicker datepicker-popup">
                        <input type="text" class="form-control input-limpiable" id="lote_producto_vencimiento"
                                onkeypress="return ValidarTeclaEnInput(event, 'datepicker')">
                        <span class="input-group-addon input-group-append border-left">
                            <span class="mdi mdi-calendar input-group-text"></span>
                        </span>
                    </div>
                </div>
                <div class="form-group col-sm-6 mt-3">
                    <label>Cantidad comprada</label>
                    <input class="form-control input-limpiable" id="lote_cantidad"
                            onkeypress="return ValidarTeclaEnInput(event, 'int')">
                </div>
            </div>
            <div class="col-sm-12 row">
                <div class="form-group col-sm-6">
                    <div class="form-check">
                        <label class="form-check-label">
                        <input type="radio" class="form-check-input" name="optionsRadios" id="radioCostoUnitario" value="0" checked
                                onclick="ToggleRadio()">
                        Costo Unitario
                        <i class="input-helper"></i></label>
                        <input class="form-control input-limpiable" id="lote_costo_unitario"
                            onkeypress="return ValidarTeclaEnInput(event, 'decimal')">
                    </div>
                </div>
                <div class="form-group col-sm-6">
                    <div class="form-check">
                        <label class="form-check-label">
                        <input type="radio" class="form-check-input" name="optionsRadios" id="radioSubtotal" value="1"
                                onclick="ToggleRadio()">
                        Subtotal
                        <i class="input-helper"></i></label>
                        <input class="form-control input-limpiable" id="lote_subtotal"
                            onkeypress="return ValidarTeclaEnInput(event, 'decimal')" disabled>
                    </div>
                </div>
            </div>
        </form>
    `
    const footerHtml = `
        <button type="button" class="btn btn-warning btn-rounded btn-fw adminonly" id="btn_crear_visita"
                onclick="LoteGuardarCambios(${loteId})">
            Guardar Cambios
        </button>
        <button type="button" class="btn btn-light btn-rounded btn-fw" data-dismiss="modal">Cancelar</button>
    `
    ShowModal('modal', 'Detalle del lote', bodyHtml, footerHtml)
    await ValidarPermisos()
    try {
        MostrarLoader()
        await getProductosSelectCompras()
        for (lote of lotes) {
            if ( lote.id == loteId) {
                if (lote.producto.id)
                    $('#lote_producto').val(lote.producto.id)
                else
                    $('#lote_producto').val(lote.producto)
                $('#lote_observaciones').val(lote.descripcion)
                $('#lote_cantidad').val(lote.cantidad_comprada)
                if (lote.fecha_vencimiento) {
                    $('#lote_producto_vencimiento').val(moment(lote.fecha_vencimiento, 'Y-MM-DD').format('DD/MM/Y'))
                }
                $('#lote_subtotal').val(lote.subtotal)
                $('#lote_costo_unitario').val(lote.costo_unitario)
                $('#modal-title').html(`Detalle del lote : ${lote.codigo}`)
                $('#existencias').html(`<b>Unidades en existencia : ${await getExistenciaActual(loteId, lote.cantidad_comprada)} </b>`)
                $(".select-2").select2({
                    theme: "bootstrap",
                    width: 'auto',
                    dropdownAutoWidth: true
                })
                InitDatePickers()
            }
        }
        OcultarLoader()
    } catch(err) {
        OcultarLoader()
        showAlert('error-message', {title: 'No se pudo cargar el detalle del lote, intente nuevamente'})
        console.log(err)
    }
}

const LoteGuardarCambios = (loteId) => {
    const lote_producto = $('#lote_producto').val()
    const lote_observaciones = $('#lote_observaciones').val()
    const lote_cantidad = $('#lote_cantidad').val()
    const lote_costo_unitario = $('#lote_costo_unitario').val()
    let lote_producto_vencimiento = $('#lote_producto_vencimiento').val()
    const lote_subtotal = $('#lote_subtotal').val()
    const radioSelected = $('input[name=optionsRadios]:checked').val()

    showAlert('warning-message-and-cancel', {
        title: 'Guardar Cambios',
        text: 'Esta seguro que desea guardar los cambios en el lote?'
    })
    $('.swal-button--confirm').on('click', async () => {
        let totalExistencias = 0
        for (lote of lotes) {
            if (lote.id == loteId){
                const existenciaActual = await getExistenciaActual(lote.id, lote.cantidad_comprada)
                if (Number(lote.cantidad_comprada) > Number(lote_cantidad)) {
                    const diferencia = Number(lote.cantidad_comprada) - Number(lote_cantidad)
                    const existencia_nueva = existenciaActual - Number(diferencia)
                    if (existencia_nueva < 0) {
                        showAlert('error-message', {title: 'La cantidad comprada que se quiere ingresar es menor a las unidades vendidas de este lote'})
                        return
                    }
                }
                if (lote_producto_vencimiento == '') lote.fecha_vencimiento = null
                else lote.fecha_vencimiento = moment(lote_producto_vencimiento, 'DD/MM/Y').format('Y-MM-DD')
                lote.cantidad_comprada = lote_cantidad
                lote.descripcion = lote_observaciones
                lote.producto = lote_producto
                if (radioSelected === '0') {
                    lote.subtotal = (Number(lote_costo_unitario)*Number(lote_cantidad)).toFixed(2)
                    lote.costo_unitario = lote_costo_unitario
                } else if (radioSelected === '1'){
                    lote.costo_unitario = (Number(lote_subtotal)/Number(lote_cantidad)).toFixed(2)
                    lote.subtotal = lote_subtotal
                }
                $(`#td_producto${loteId}`).html($("#lote_producto option:selected").text())
                if (lote_producto_vencimiento == '') lote_producto_vencimiento = 'N/A'
                $(`#td_fecha${loteId}`).html(lote_producto_vencimiento)
                $(`#td_codigo${loteId}`).html(lote.codigo)
                $(`#td_cantidad${loteId}`).html(lote.cantidad_comprada)
                $(`#td_costo_unitario${loteId}`).html('Q'+lote.costo_unitario)
                $(`#td_subtotal${loteId}`).html('Q'+lote.subtotal)
                let currentPage = window.location.pathname
                currentPage = currentPage.split('/')
                $('#total').html(`Total de la compra: Q${RecalcularTotal()}`)
                $('#modal').modal('toggle')
                lotesEditar.push(loteId)
            }
        }
    })
}

const VentaEliminar = async () => {
    showAlert('warning-message-and-cancel', {
        title: 'Eliminar Venta',
        text: 'Esta seguro que desea eliminar la venta?'
    })
    $('.swal-button--confirm').on('click', async () => {
        try {
            MostrarLoader()
            for (detalle of estaVenta.detalle_venta){
                const response = await axios.patch(`detalles-venta/update/${detalle.id}/`, {
                    estado: 2
                })
            }
            console.log(estaVenta)
            const response = await axios.patch(`ventas/update/${getUrlParameter()}/`, {
                estado: 2
            })
            if (response.status === 200){
                showAlert('success-message', {
                    title: 'Venta eliminada',
                    button: {
                        text: 'Continuar'
                    }
                })
                $('#card-venta').html(`
                    <h1 class="text-light bg-dark pl-1 display-1">Esta venta ha sido eliminada</h1>
                `)
            }
            OcultarLoader()
        } catch (err) {
            OcultarLoader()
            showAlert('error-message', {
                title: 'No se pudo eliminar la venta, intente nuevamente'
            })
            console.log(err)
        }
    })
}
