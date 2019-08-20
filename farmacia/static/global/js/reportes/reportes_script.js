const getBalanceGeneral = (comprasTotal, ventasTotal, consultasTotal, transaccionesDebitosTotal, transaccionesCreditosTotal) => {
    const totalVentas = Number(ventasTotal).toFixed(2)
    const totalConsultas = Number(consultasTotal).toFixed(2)
    const totalCreditos = Number(transaccionesCreditosTotal).toFixed(2)
    const totalCompras = Number(comprasTotal).toFixed(2)
    const totalDebitos = Number(transaccionesDebitosTotal).toFixed(2)
    
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
        ventas: ventasTotal,
        consultas: consultasTotal,
        creditos: transaccionesCreditosTotal,
        compras: comprasTotal,
        debitos: transaccionesDebitosTotal,
        balance: balanceGeneral
    }

    return balance

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