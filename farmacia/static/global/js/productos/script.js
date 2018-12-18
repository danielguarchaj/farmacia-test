const getProductos = async () => {
    try {
        const { data } = await axios.get('productos/')
        //await actualizarEstadoVisitas(data)
        let productosHtml = ''
        let cont = 0
        for (producto of data) {
            cont++
            let existencias = 0
            for (lote of producto.lotes) {
                existencias += await getExistenciaActual(lote.id, lote.cantidad_comprada)
            }
            
            let estado = '<div class="badge badge-success">Abastecido</div>'
                    
            if (existencias <= producto.minimo_permitido)
                estado = '<div class="badge badge-warning">Cantidad baja</div>'
            if (existencias == 0)
                estado = '<div class="badge badge-danger">Agotado</div>'
            productosHtml +=
                `
                    <tr>
                        <td>${cont}</td>
                        <td>${producto.nombre}</td>
                        <td>${producto.marca.nombre}</td>
                        <td>${producto.presentacion.nombre}</td>
                        <td>Q${producto.precio_venta}</td>
                        <td>${producto.minimo_permitido}</td>
                        <td>${existencias}</td>
                        <td>${estado}</td>
                        <td>
                            <i class="mdi mdi-eye-outline mr-3" onclick="window.location.href='${producto.id}/'"></i>
                            <i class="mdi mdi-trash-can adminonly" onclick="ProductoEliminar(${producto.id})"></i>
                        </td>
                    </tr>
                `
        }
        $('#productos-t-body').html(productosHtml)
        InitDataTable()
    } catch (err) {
        showAlert('error-message', {
            title: 'No se pudieron cargar los productos, intente mas tarde'
        })
        console.log(err)
    }
}

const ProductoEliminar = (productoId) => {
    if (!productoId) productoId = getUrlParameter()
    showAlert('warning-message-and-cancel', {
        title: 'Eliminar Producto',
        text: 'Esta seguro que desea eliminar el producto?'
    })
    $('.swal-button--confirm').on('click', async () => {
        try {
            MostrarLoader()
            const response = await axios.patch(`productos/${productoId}/`, {estado: 2})
            showAlert('success-message', {
                title: 'Producto eliminado',
                button: {
                    text: 'Continuar'
                }
            })
            OcultarLoader()
            $('.btn-success-confirm').on('click', () => {
                location.reload()
            })

        } catch (err) {
            showAlert('error-message', {title: 'No se ha podido eliminar el producto, intente mas tarde'})
            console.log(err)
        }
    })
}

const getMarcas = async () => {
    try {
        MostrarLoader()
        const {data} = await axios.get('marcas/')
        if (!data[0]) showAlert('error-message', {title: 'No existen marcas registradas'})
        const selectMarcasHtml = data.reduce(
            (acc, marca) => acc += `
            <option value="${marca.id}">${marca.id} - ${marca.nombre}</option>
            `,
            '<option value="0" disabled selected>Seleccione la marca del producto</option>'
        )
        $('#producto_marca').html(selectMarcasHtml)
        $(".select-2").select2({
            theme: "bootstrap",
            width: 'auto',
            dropdownAutoWidth: true
        }); 
        OcultarLoader()
    } catch (err) {
        OcultarLoader()
        showAlert('error-message', {title: 'No se pudieron cargar las marcas, intente mas tarde'})
    }
}

const getPresentaciones = async () => {
    try {
        MostrarLoader()
        const {data} = await axios.get('presentaciones/')
        if (!data[0]) showAlert('error-message', {title: 'No existen presentaciones registradas'})
        const selectPresentacionesHtml = data.reduce(
            (acc, presentacion) => acc += `
                <option value="${presentacion.id}">${presentacion.id} - ${presentacion.nombre}</option>
            `,
            '<option value="0" disabled selected>Seleccione la presentacion del producto</option>'
        )
        $('#producto_presentacion').html(selectPresentacionesHtml)
        $(".select-2").select2({
            theme: "bootstrap",
            width: 'auto',
            dropdownAutoWidth: true
        });
        OcultarLoader()
    } catch (err) {
        OcultarLoader()
        showAlert('error-message', {title: 'No se pudieron cargar las presentaciones, intente mas tarde'})
    }
}

const getCategorias = async () => {
    try {
        MostrarLoader()
        const {data} = await axios.get('categorias/')
        if (!data[0]) showAlert('error-message', {title: 'No existen categorias registradas'})
        const selectCategoriasHtml = data.reduce(
            (acc, categoria) => acc += `
                <option value="${categoria.id}">${categoria.id} - ${categoria.nombre}</option>
            `,
            '<option value="0" disabled selected>Seleccione la categoria del producto</option>'
        )
        $('#producto_categoria').html(selectCategoriasHtml)
        $(".select-2").select2({
            theme: "bootstrap",
            width: 'auto',
            dropdownAutoWidth: true
        });
        OcultarLoader()
    } catch (err) {
        OcultarLoader()
        showAlert('error-message', {title: 'No se pudieron cargar las categorias, intente mas tarde'})
    }
}

const CrearProducto = (refresh) => {
    const producto_marca = $('#producto_marca').val()
    const producto_presentacion = $('#producto_presentacion').val()
    const producto_nombre = $('#producto_nombre').val()
    const producto_precio_venta = $('#producto_precio_venta').val()
    const producto_minimo_permitido = $('#producto_minimo_permitido').val()
    const producto_referencia_ubicacion = $('#producto_referencia_ubicacion').val()
    const producto_categoria = $('#producto_categoria').val()
    let errores = false
    if (!producto_marca) {
        showDangerToast('Seleccione la marca del producto')
        errores = true
    }
    if (!producto_presentacion) {
        showDangerToast('Seleccione la presentacion del producto')
        errores = true
    }
    if (producto_nombre == '') {
        showDangerToast('El nombre del producto es requerido')
        errores = true
    }
    if (producto_precio_venta == '') {
        showDangerToast('El precio de venta del producto es requerido')
        errores = true
    }
    if (!ValidarContenidoInput(producto_precio_venta, 'float82')) {
        showDangerToast('El formato del precio de venta del producto invalido')
        errores = true
    }
    if (producto_minimo_permitido == '') {
        showDangerToast('El minimo permitido del producto es requerido')
        errores = true
    }
    if (!ValidarContenidoInput(producto_minimo_permitido, 'int')) {
        showDangerToast('El formato de la cantidad minima es invalido')
        errores = true
    }
    if (!producto_categoria) {
        showDangerToast('Seleccione la categoria del producto')
        errores = true
    }
    
    if (errores) return
    

    const data = {
        nombre: producto_nombre,
        precio_venta: producto_precio_venta,
        referencia_ubicacion: producto_referencia_ubicacion,
        minimo_permitido: producto_minimo_permitido,
        presentacion: producto_presentacion,
        marca: producto_marca,
        categoria: producto_categoria
    }

    showAlert('warning-message-and-cancel', {
        title: 'Crear Producto',
        text: 'Esta seguro que quiere crear el producto?'
    })

    $('.swal-button--confirm').on('click', async function () {
        try {
            MostrarLoader()
            const response = await axios.post('productos/create/', data)
            if (response.status === 201) {
                OcultarLoader()
                showAlert('success-message', {
                    title: 'Producto creado con exito'
                })
                $('.btn-success-confirm').on('click', async function () {
                    if (refresh === 'refresh') {
                        await getProductosSelectCompras()
                        $('#modal').modal('toggle')
                    }else location.reload()
                })
            }
        } catch (err) {
            OcultarLoader()
            showAlert('error-message', {
                title: 'No se pudo crear el producto, intente mas tarde'
            })
        }
    })
}

const CrearCategoria = (refresh) => {
    const categoria_nombre = $('#categoria_nombre').val()
    const categoria_descripcion = $('#categoria_descripcion').val()   

    if (categoria_nombre === '') {
        showDangerToast('Ingrese el nombre de la categoria')
        return
    }

    const data = {
        nombre: categoria_nombre,
        descripcion: categoria_descripcion
    }

    showAlert('warning-message-and-cancel', {
        title: 'Crear Categoria',
        text: 'Esta seguro que quiere crear la categoria?'
    })

    $('.swal-button--confirm').on('click', async function () {
        try {
            MostrarLoader()
            const response = await axios.post('categorias/', data)
            if (response.status === 201) {
                OcultarLoader()
                showAlert('success-message', {
                    title: 'Categoria creada con exito'
                })
                $('.btn-success-confirm').on('click', async function () {
                    if (refresh === 'refresh') {
                        await getCategorias()
                        $('#modal').modal('toggle')
                    } else if (refresh == 'sub-modal') {
                        await getCategorias()
                        $('#sub-modal').modal('toggle')
                    } else location.reload()
                })
            }
        } catch (err) {
            OcultarLoader()
            showAlert('error-message', {
                title: 'No se pudo crear la categoria, intente mas tarde'
            })
        }
    })
}

const CrearMarca = (refresh) => {
    const marca_nombre = $('#marca_nombre').val()
    const marca_descripcion = $('#marca_descripcion').val()   

    if (marca_nombre === '') {
        showDangerToast('Ingrese el nombre de la marca')
        return
    }

    const data = {
        nombre: marca_nombre,
        descripcion: marca_descripcion
    }

    showAlert('warning-message-and-cancel', {
        title: 'Crear Marca',
        text: 'Esta seguro que quiere crear la marca?'
    })

    $('.swal-button--confirm').on('click', async function () {
        try {
            MostrarLoader()
            const response = await axios.post('marcas/', data)
            if (response.status === 201) {
                OcultarLoader()
                showAlert('success-message', {
                    title: 'Marca creada con exito'
                })
                $('.btn-success-confirm').on('click', async function () {
                    if (refresh === 'refresh') {
                        await getMarcas()
                        $('#modal').modal('toggle')
                    } else if (refresh == 'sub-modal') {
                        await getMarcas()
                        $('#sub-modal').modal('toggle')
                    } else location.reload()
                })
            }
        } catch (err) {
            OcultarLoader()
            showAlert('error-message', {
                title: 'No se pudo crear la marca, intente mas tarde'
            })
        }
    })
}

const CrearPresentacion = (refresh) => {
    const presentacion_nombre = $('#presentacion_nombre').val()
    const presentacion_descripcion = $('#presentacion_descripcion').val()   

    if (presentacion_nombre === '') {
        showDangerToast('Ingrese el nombre de la presentacion')
        return
    }

    const data = {
        nombre: presentacion_nombre,
        descripcion: presentacion_descripcion
    }

    showAlert('warning-message-and-cancel', {
        title: 'Crear Presentacion',
        text: 'Esta seguro que quiere crear la presentacion?'
    })

    $('.swal-button--confirm').on('click', async function () {
        try {
            MostrarLoader()
            const response = await axios.post('presentaciones/', data)
            if (response.status === 201) {
                OcultarLoader()
                showAlert('success-message', {
                    title: 'Presentacion creada con exito'
                })
                $('.btn-success-confirm').on('click', async function () {
                    if (refresh === 'refresh') {
                        await getPresentaciones()
                        $('#modal').modal('toggle')
                    } else if (refresh == 'sub-modal') {
                        await getPresentaciones()
                        $('#sub-modal').modal('toggle')
                    } else location.reload()
                })
            }
        } catch (err) {
            OcultarLoader()
            showAlert('error-message', {
                title: 'No se pudo crear la presentacion, intente mas tarde'
            })
        }
    })
}

const CrearCategoriaForm = () => {
    const formHtml = `
        <form class="form-sample">
            <div class="col-sm-12 row">
                <div class="form-group col-sm-6">
                    <label for="categoria_nombre">Nombre de la categoria</label>
                    <input type="text" class="form-control input-limpiable" id="categoria_nombre" placeholder="Nombre">
                </div>
                <div class="form-group col-sm-6">
                    <label for="categoria_descripcion">Descripcion</label>
                    <input type="text" class="form-control input-limpiable" id="categoria_descripcion" placeholder="Descripcion">
                </div>
            </div>
        </form>
    `
    const footerHtml = `
        <button type="button" class="btn btn-info btn-rounded btn-fw" onclick="CrearCategoria('sub-modal')">Crear Categoria</button>
        <button type="button" class="btn btn-light btn-rounded btn-fw" data-dismiss="modal">Cancelar</button>
    `
    ShowModal('sub-modal', 'Crear Nueva Categoria', formHtml, footerHtml)
    $('.modal-dialog-centered').removeClass('modal-lg')
}

const CrearMarcaForm = () => {
    const formHtml = `
        <form class="form-sample">
            <div class="col-sm-12 row">
                <div class="form-group col-sm-6">
                    <label for="marca_nombre">Nombre de la marca</label>
                    <input type="text" class="form-control input-limpiable" id="marca_nombre" placeholder="Nombre">
                </div>
                <div class="form-group col-sm-6">
                    <label for="marca_descripcion">Descripcion</label>
                    <input type="text" class="form-control input-limpiable" id="marca_descripcion" placeholder="Descripcion">
                </div>
            </div>
        </form>
    `
    const footerHtml = `
        <button type="button" class="btn btn-info btn-rounded btn-fw" onclick="CrearMarca('sub-modal')">Crear Marca</button>
        <button type="button" class="btn btn-light btn-rounded btn-fw" data-dismiss="modal">Cancelar</button>
    `
    ShowModal('sub-modal', 'Crear Nueva Marca', formHtml, footerHtml)
    $('.modal-dialog-centered').removeClass('modal-lg')
}

const CrearPresentacionForm = () => {
    const formHtml = `
        <form class="form-sample">
            <div class="col-sm-12 row">
                <div class="form-group col-sm-6">
                    <label for="presentacion_nombre">Nombre de la presentacion</label>
                    <input type="text" class="form-control input-limpiable" id="presentacion_nombre" placeholder="Nombre">
                </div>
                <div class="form-group col-sm-6">
                    <label for="presentacion_descripcion">Descripcion</label>
                    <input type="text" class="form-control input-limpiable" id="presentacion_descripcion" placeholder="Descripcion">
                </div>
            </div>
        </form>
    `
    const footerHtml = `
        <button type="button" class="btn btn-info btn-rounded btn-fw" onclick="CrearPresentacion('sub-modal')">Crear Presentacion</button>
        <button type="button" class="btn btn-light btn-rounded btn-fw" data-dismiss="modal">Cancelar</button>
    `
    ShowModal('sub-modal', 'Crear Nueva Presentacion', formHtml, footerHtml)
    $('.modal-dialog-centered').removeClass('modal-lg')
}
