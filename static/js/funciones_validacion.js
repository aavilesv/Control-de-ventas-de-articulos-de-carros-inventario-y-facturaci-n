$('.myTable').DataTable({
    resposive:true,
    language:{
        "sProcessing":     "Procesando...",
        "sLengthMenu":     "Mostrar _MENU_ registros",
        "sZeroRecords":    "No se encontraron resultados",
        "sEmptyTable":     "Ningún dato disponible en esta tabla =(",
        "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
        "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
        "sInfoPostFix":    "",
        "sSearch":         "Buscar:",
        "sUrl":            "",
        "sShow":            "Mostrar",
        "sInfoThousands":  ",",
        "sLoadingRecords": "Cargando...",
        "oPaginate": {
            "sFirst":    "Primero",
            "sLast":     "Último",
            "sNext":     "Siguiente",
            "sPrevious": "Anterior"
        },
        "oAria": {
            "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
        },
        "buttons": {
            "copy": "Copiar",
            "colvis": "Visibilidad"
        }
    }
});
function todo()
{
    if (valruc()==false) {
        return false;
    }else {
        return true;
    }
}

function todocedula()
{
    if (valCedula()==false) {
        return false;
    }else {
        return true;
    }
}
function valCedula() {

    var cedula = document.getElementById("cedula").value;
    if(cedula.length == 10){
        //Obtenemos el digito de la region que sonlos dos primeros digitos
        var digito_region = cedula.substring(0,2);
        //Pregunto si la region existe ecuador se divide en 24 regiones
        if( digito_region >= 1 && digito_region <=24 ){
            var dig;
            var suma_total=0;
            for (var i=0;i<9;i++){
                dig = parseInt(cedula.substring(i,i+1));
                if (i%2==0){
                    dig = dig*2 ;
                    if ( dig > 9)
                        dig = dig - 9;
                }
                suma_total = suma_total + dig;
            }
            // Extraigo el ultimo digito
            var ultimo_digito   = parseInt(cedula.substring(9,10));
            //Obtenemos la decena inmediata
            var z = 0;
            while (suma_total % 10 != 0) {
                suma_total++;
                z++;
            }
            //Validamos que el digito validador sea igual al de la cedula
            if(z == ultimo_digito){
                // alert('la cedula:' + cedula + ' es correcta');
                return true;
            }else{

            Swal.fire({
                title: 'Información!',
                icon: 'info',
                text: 'Cédula: ' + String(document.getElementById("cedula").value)  +' es incorrecta, por favor revisar digitos',
                html:'Cédula: ' + String(document.getElementById("cedula").value) +' es incorrecta, por favor revisar digitos',
                showCloseButton: true,
                confirmButtonColor: "#33ECFF",
                confirmButtonText: 'OK',
                imageWidth: 400,
                imageHeight: 200,
                imageAlt: 'Custom image',
            });

                return false;
            }
        }else{
            // imprimimos en consola si la region no pertenece
        Swal.fire({
            title: 'Información!',
            icon: 'info',
            text: 'Esta cedula no pertenece a ninguna region',
            html:'Esta cedula no pertenece a ninguna region',
            showCloseButton: true,
            confirmButtonColor: "#33ECFF",
            confirmButtonText: 'OK',
            imageWidth: 400,
            imageHeight: 200,
            imageAlt: 'Custom image',
        });


            return false;
        }
    }
    return false;
}

function valruc() {
    var cedula = document.getElementsByName("ruc").value;
    var ruc=cedula.substring(10,13);
    cedula=cedula.substring(0,10);
    //Obtenemos el digito de la region que sonlos dos primeros digitos
    var digito_region = cedula.substring(0,2);
    //Pregunto si la region existe ecuador se divide en 24 regiones
    if( digito_region >= 1 && digito_region <=24 ){
        var dig;
        var suma_total=0;
        for (var i=0;i<9;i++){
            dig = parseInt(cedula.substring(i,i+1));
            if (i%2==0){
                dig = dig*2 ;
                if ( dig > 9)
                    dig = dig - 9;
            }
            suma_total = suma_total + dig;
        }
        // Extraigo el ultimo digito
        var ultimo_digito   = parseInt(cedula.substring(9,10));
        //Obtenemos la decena inmediata
        var z = 0;
        while (suma_total % 10 != 0) {
            suma_total++;
            z++;
        }
        //Validamos que el digito validador sea igual al de la cedula
        if(z == ultimo_digito){
            // alert('la cedula:' + cedula + ' es correcta');
            return true;
        }else{
            Swal.fire({
                title: 'Información!',
                icon: 'info',
                text: 'Ruc:' + String(document.getElementById("ruc").value)  +' es incorrecto, por favor revisar digitos',
                html:'Ruc:' + String(document.getElementById("ruc").value) +' es incorrecto, por favor revisar digitos',
                showCloseButton: true,
                confirmButtonColor: "#33ECFF",
                confirmButtonText: 'OK',
                imageWidth: 400,
                imageHeight: 200,
                imageAlt: 'Custom image',
            });

            return false;
        }
    }else{
        // imprimimos en consola si la region no pertenece
        Swal.fire({
            title: 'Información!',
            icon: 'info',
            text: 'Esta cedula no pertenece a ninguna region',
            html:'Esta cedula no pertenece a ninguna region',
            showCloseButton: true,
            confirmButtonColor: "#33ECFF",
            confirmButtonText: 'OK',
            imageWidth: 400,
            imageHeight: 200,
            imageAlt: 'Custom image',
        });

        return false;
    }



}
function sololetrassin(e) {
    tecla = (document.all) ? e.keyCode : e.which; // 2
    if (tecla == 8)
        return true; // 3
    patron = /[A-Za-z]/; // 4
    te = String.fromCharCode(tecla); // 5
    return patron.test(te); // 6
}

function soloNumeros(e) {
    var key = window.Event ? e.which : e.keyCode;
    return (key >= 48 && key <= 57)
}

function soloNumerospunto(e) {
    var key = window.Event ? e.which : e.keyCode;

    return ((key >= 48 && key <= 57) || key == 46)
}


function sololetras(e) {
    tecla = (document.all) ? e.keyCode : e.which; // 2
    if (tecla == 8)
        return true; // 3
    patron = /[A-Za-z\s]/; // 4
    te = String.fromCharCode(tecla); // 5
    return patron.test(te); // 6
}



function sololetrasynumeros(e) {

       tecla = (document.all) ? e.keyCode : e.which; // 2
    if (tecla == 8)
        return true; // 3
    patron = /[A-Za-z\9123456780]/; // 4
    te = String.fromCharCode(tecla); // 5
    return patron.test(te); // 6
    }


function elimina()
{
    Swal.fire({
        title: "Usuario #123465",
        text: "¿Eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
    })
    .then(resultado => {
        if (resultado.value) {
            // Hicieron click en "Sí"
 return true;
        } else {
            // Dijeron que no
             return false;
        }
    });
}