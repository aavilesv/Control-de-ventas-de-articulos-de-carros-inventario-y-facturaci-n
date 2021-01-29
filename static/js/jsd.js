
$('#frm-login').on({
    submit: function (e) {
        e.preventDefault();
        var frmData = new FormData($(this)[0]);
        $.ajax({
            url: '/seguridad/login/',
            data: frmData,
            method: 'POST',
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function () {
                $('.loading span').html('Verificando..');
                $('.loading i').removeClass('glyphicon glyphicon-log-in');
                $('.loading i').addClass('fa fa-refresh glyphicon-refresh-animate');
            }
        }).done(function (data) {
            if (data.resp == true) {

                window.location = '/';
                return false;
            }
            Swal.fire({
  title: data.error,
  confirmButtonColor: "#71C78D",

showCloseButton: true,
  showClass: {
    popup: 'animated fadeInDown faster'
  },
  hideClass: {
    popup: 'animated fadeOutUp faster'
  }
});
          $('.loading span').html('Iniciar Session');
            $('.loading i').removeClass('fa fa-refresh glyphicon-refresh-animate');
            $('.loading i').addClass('glyphicon glyphicon-log-in');
            $('#btnlogin').attr('disabled', false);

        }).fail(function () {

Swal.fire({
  title: 'Error del Servidor!',

  text: 'Por favor comunicar al administrador.',
  showCloseButton: true,
  confirmButtonColor: "#71C78D",
    confirmButtonText: 'OK',
  imageUrl: '/static/img/error.png',
  imageWidth: 400,
  imageHeight: 200,
  imageAlt: 'Custom image',
});


        });
    }
});

function sololetrasynumeros(e) {

       tecla = (document.all) ? e.keyCode : e.which; // 2
    if (tecla == 8)
        return true; // 3
    patron = /[A-Za-z\9123456780]/; // 4
    te = String.fromCharCode(tecla); // 5
    return patron.test(te); // 6
    }

