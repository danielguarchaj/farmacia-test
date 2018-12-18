const getBalanceGeneral = async () => {
    try{

        const comprasTotal = await axios.get('compras/totales/')
        const ventasTotal = await axios.get('ventas/totales/')
        const consultasTotal = await axios.get('consultas/totales/')
        const transaccionesDebitosTotal = await axios.get('transacciones/debitos-totales/')
        const transaccionesCreditosTotal = await axios.get('transacciones/creditos-totales/')        

        const totalVentas = Number(ventasTotal.data.total).toFixed(2)
        const totalConsultas = Number(consultasTotal.data.total).toFixed(2)
        const totalCreditos = Number(transaccionesCreditosTotal.data.total).toFixed(2)
        const totalCompras = Number(comprasTotal.data.total).toFixed(2)
        const totalDebitos = Number(transaccionesDebitosTotal.data.total).toFixed(2)
        
        $('#balance_ventas').html(`Q${totalVentas}`)
        $('#balance_consultas').html(`Q${totalConsultas}`)
        $('#balance_creditos').html(`Q${totalCreditos}`)
        $('#balance_compras').html(`Q${totalCompras}`)
        $('#balance_debitos').html(`Q${totalDebitos}`)

        const balanceGeneral = Number(totalVentas) + Number(totalConsultas) + Number(totalCreditos) - Number(totalCompras) - Number(totalDebitos)
        if ( balanceGeneral < 0 ) {
            $('#balance_general').html(`Q${balanceGeneral.toFixed(2)}`)
            $('#balance_general').addClass('text-danger')
            $('#balance-actual').html(`Balance actual : Q${balanceGeneral.toFixed(2)}`)
            $('#balance-actual').addClass('text-danger')
        }else {
            $('#balance_general').html(`Q${balanceGeneral.toFixed(2)}`)
            $('#balance_general').addClass('text-success')
            $('#balance-actual').html(`Balance actual : Q${balanceGeneral.toFixed(2)}`)
            $('#balance-actual').addClass('text-success')
        }

        const balance = {
            ventas: ventasTotal.data.total,
            consultas: consultasTotal.data.total,
            creditos: transaccionesCreditosTotal.data.total,
            compras: comprasTotal.data.total,
            debitos: transaccionesDebitosTotal.data.total,
            balance: balanceGeneral
        }

        return balance

    }catch(err){
        showAlert('error-message', {title: 'No se pudo cargar el balance general, intente nuevamente'})
        console.log(err)
    }
}

const getGananciasDetalleVenta = detalleVenta => {
    let ganancias = 0
    for (detalle of detalleVenta){
        const costoSubtotal = Number(detalle.lote.costo_unitario) * Number(detalle.cantidad)
        const ventaSubtotal = Number(detalle.precio_venta_real) * Number(detalle.cantidad)
        ganancias += (ventaSubtotal - costoSubtotal)
    }
    return ganancias
    
}