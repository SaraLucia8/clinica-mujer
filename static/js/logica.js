let formulario = document.getElementById('formulario');

let cedula = document.getElementById("cedula");
let nombre = document.getElementById("nombre");
let apellido = document.getElementById("apellido");
let nacimiento = document.getElementById("nacimiento");
let eps = document.getElementById("eps");
let email = document.getElementById("email");
let tel = document.getElementById("tel");
let dir = document.getElementById("dir");
let ciudad = document.getElementById("ciudad");
let contrasena = document.getElementById("contrasena");
let politica = document.getElementById("politica");


formulario.addEventListener("submit", e=>{
    
    let validarCedula = /[0123456789]{8,10}/;
    let validarNombre= /^[a-zA-ZÀ-ÿ\s]{1,40}$/;
    let validarApellido= /^[a-zA-ZÀ-ÿ\s]{1,40}$/;
    let validarEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    let validarContrasena = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])([A-Za-z\d$@$!%*?&]|[^ ]){8,15}$/;
    let validarTel = /^\d{7,10}$/
    
    if (!validarNombre.test(nombre.value)){
        alert("El(los) Nombre(s) debe(n) llevar solo letras. Min 4, Max 30 caractéres")
        e.preventDefault()
    }
    if (!validarApellido.test(apellido.value)){
        alert("El(los) Apellido(s) debe(n) llevar solo letras. Min 4, Max 30 caractéres")
        e.preventDefault()
    }

    if (!validarCedula.test(cedula.value)){
        alert("La cedula debe contener entre 8 y 10 caracteres \nRecuerda que deben ser sólo números");
        e.preventDefault()
    }
    if (!validarEmail.test(email.value)){
        alert("El email debe contener un @ y un .com, .es, .edu, etc");
        e.preventDefault()
    }if(!validarContrasena.test(contrasena.value)){
        alert("La contraseña debe cumplir con los siguientes requisitos: 8 a 15 caracteres, Al menos una letra mayúscula, Al menos una letra minúscula, Al menos un dígito, No espacios en blanco, Al menos 1 caracter especial.")
        e.preventDefault()
    }
    if(!validarTel.test(tel.value)){
        alert("El teléfono debe tener entre 7 y 10 números.")
        e.preventDefault()
    }
})