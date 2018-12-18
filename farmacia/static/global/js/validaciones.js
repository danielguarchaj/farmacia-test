/*
Codigos y equivalentes en teclado
0 -> Caracter nulo
8 -> retroceso
32 -> espacio
46 -> punto
47 -> slash /
*/
const ValidarTeclaEnInput = (e, tipo) => {
    tecla = (document.all) ? e.keyCode : e.which;
    //Tecla de retroceso para borrar, siempre la permite
    switch (tipo){
        case 'decimal':
            if (tecla == 8 || tecla == 46) return true;
            // Patron de entrada para letras
            patron =/[0-9]/;
            break;
        case 'int':
            if (tecla == 8 ) return true;
            // Patron de entrada para letras
            patron =/[0-9]/;
            break;
        case 'fraction':
            if (tecla == 8 || tecla == 47) return true;
            // Patron de entrada para letras
            patron =/[0-9]/;
            break;
        case 'datepicker':
            return false
            break;
        default:
            break;
    }
    tecla_final = String.fromCharCode(tecla);
    return patron.test(tecla_final);
 } 
 
 const ValidarContenidoInput = (value, tipo) => {
    switch (tipo) {
        case 'float82':
            return /^(\d{1,8})(\.\d{1,2})?$/.test(value)
            break
        case 'fraction3/3':
            return /^(\d{1,3})(\/\d{1,3})$/.test(value)
            break
        case 'int':
            return /^[0-9]+$/.test(value)
            break
        case 'date':
            return '00/00/0000'.length == value.length 
            break
        default:break
     }
 }
 // const x = (x, y) => { return x * y };
 