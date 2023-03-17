// cambio de tema
const themeMap = {
  dark: "light",
  light: "solar",
  solar: "dark"
};

const theme = localStorage.getItem('theme')
  || (tmp = Object.keys(themeMap)[0],
      localStorage.setItem('theme', tmp),
      tmp);
const bodyClass = document.body.classList;
bodyClass.add(theme);

function toggleTheme() {
  const current = localStorage.getItem('theme');
  const next = themeMap[current];

  bodyClass.replace(current, next);
  localStorage.setItem('theme', next);
}

document.getElementById('themeButton').onclick = toggleTheme;


// Fecha y hora
const time = document.getElementById('time');
const date = document.getElementById('date');
const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];
const interval = setInterval(() => {
    const local = new Date();
    let day = local.getDate(),
        month = local.getMonth(),
        year = local.getFullYear();
    time.innerHTML = local.toLocaleTimeString();
    date.innerHTML = `${day} ${monthNames[month]} ${year}`;
}, 1000);

var tablet= document.querySelector(".container-cart")
var bloques= document.querySelector(".container-bloques")
var pesado= document.querySelector(".container-pesaje")
var bar= document.querySelector("#bar")
var arriba= document.querySelector("#farriba")
var abajo= document.querySelector("#fabajo")
var cargador= document.querySelector("#cargador")

abajo.style.display="block";
bloques.style.display="none";
pesado.style.display="none";
arriba.style.display="none";
tablet.style.display="none";
cargador.style.display="none";

// mostrar tabla 
function mostrarTabla(){
  tablet.style.display="block";
  arriba.style.display="block"; 
  abajo.style.display="none"; 
}
function ocultarTabla(){
  abajo.style.display="block"; 
  arriba.style.display="none"; 
  tablet.style.display="none";  
}

//
function mostrarcarga(){
  cargador.style.display="block";
  bloques.style.display="none"; 
}

function mostrarbloques(){
  bloques.style.display="block"; 
  pesado.style.display="block";
  cargador.style.display="none";
}


//Insertar filas
var total=0;
var elementoTotal = document.getElementById("total");

function insertar1(){
  let tblDatos= document.getElementById('tblDatos').insertRow(1);
  let product= document.getElementById('bot1').innerHTML;
  product= product.split(" ");
  var peso= document.getElementById('peso').innerHTML;
  peso= peso.split(" Kg");
  peso=peso[0]*1;
  var button = document.createElement("button");
  button.innerHTML = '<svg  width="24" height="24" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0H284.2c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64S14.3 32 32 32h96l7.2-14.3zM32 128H416V448c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z"/></svg>'
  var precio = 10*Number(peso);
  precio=precio.toFixed(2);
  precio=precio*1;
  total+=precio;
  let col1 = tblDatos.insertCell(0);
  let col2 = tblDatos.insertCell(1);
  let col3 = tblDatos.insertCell(2);
  let col4 = tblDatos.insertCell(3);
  tblDatos.style.backgroundColor = 'black';

  col1.innerHTML=product;
  col2.innerHTML=peso;
  col3.innerHTML='S/'+precio;
  col4.appendChild(button);
  button.addEventListener("click", function() {
    // Obtén la fila a eliminar
    var fila = this.parentNode.parentNode;
    alert("Producto eliminado")
    // Elimina la fila
    fila.parentNode.removeChild(fila);
    total-=precio;
    console.log(total);
    elementoTotal.innerHTML = total.toFixed(2);
  });
  console.log(total);
  elementoTotal.innerHTML = total.toFixed(2);
}
function insertar2(){
  let tblDatos= document.getElementById('tblDatos').insertRow(1);
  let product= document.getElementById('bot2').innerHTML;
  product= product.split(" ");
  var peso= document.getElementById('peso').innerHTML;
  peso= peso.split(" Kg");
  peso=peso[0]*1;
  var button = document.createElement("button");
  button.innerHTML = '<svg  width="24" height="24" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0H284.2c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64S14.3 32 32 32h96l7.2-14.3zM32 128H416V448c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z"/></svg>'
  var precio = 10*Number(peso);
  precio=precio.toFixed(2);
  precio=precio*1;
  total=total+precio;
  let col1 = tblDatos.insertCell(0);
  let col2 = tblDatos.insertCell(1);
  let col3 = tblDatos.insertCell(2);
  let col4 = tblDatos.insertCell(3);
  tblDatos.style.backgroundColor = 'black';

  col1.innerHTML=product;
  col2.innerHTML=peso;
  col3.innerHTML='S/'+precio;
  col4.appendChild(button);
  button.addEventListener("click", function() {
    // Obtén la fila a eliminar
    var fila = this.parentNode.parentNode;
    alert("Producto eliminado")
    // Elimina la fila
    fila.parentNode.removeChild(fila);
    total-=precio;
    console.log(total);
    elementoTotal.innerHTML = total.toFixed(2);
  });
  console.log(total);
  elementoTotal.innerHTML = total.toFixed(2);

}
function insertar3(){
  let tblDatos= document.getElementById('tblDatos').insertRow(1);
  let product= document.getElementById('bot3').innerHTML;
  product= product.split(" ")
  var peso= document.getElementById('peso').innerHTML;
  peso= peso.split(" Kg");
  peso=peso[0]*1;
  var button = document.createElement("button");
  button.innerHTML = '<svg  width="24" height="24" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0H284.2c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64S14.3 32 32 32h96l7.2-14.3zM32 128H416V448c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z"/></svg>'
  var precio = 10*Number(peso);
  precio=precio.toFixed(2);
  precio=precio*1;
  total+=precio;
  let col1 = tblDatos.insertCell(0);
  let col2 = tblDatos.insertCell(1);
  let col3 = tblDatos.insertCell(2);
  let col4 = tblDatos.insertCell(3);
  tblDatos.style.backgroundColor = 'black';

  col1.innerHTML=product;
  col2.innerHTML=peso;
  col3.innerHTML='S/'+precio;
  col4.appendChild(button);
  button.addEventListener("click", function() {
    // Obtén la fila a eliminar
    var fila = this.parentNode.parentNode;
    alert("Producto eliminado")
    // Elimina la fila
    fila.parentNode.removeChild(fila);
    total-=precio;
    console.log(total);
    elementoTotal.innerHTML = total.toFixed(2);
  });
  console.log(total);
  elementoTotal.innerHTML = total.toFixed(2);
}

const modal = document.getElementById("modal");
modal.style.display ="none";
function muestraQR() {
  const modal = document.getElementById("modal");
  modal.style.display = modal.style.display === "block" ? "none" : "block";
}

  // Cuando se haga clic en el botón "Actualizar contenido", se llamará a la función updateContent
  document.getElementById('update-button').addEventListener('click', updateContent);

  function updateContent() {
    // Realizar la petición AJAX al servidor
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/update-content');
    xhr.onload = function() {
    var message = xhr.responseText.replace(/["'{}]/g, "");
    var values = message.split(',');
    for (var i in values) {
      var sep = values[i].indexOf(":");
      var esp = values[i].length;
      var INI =values[i].substring(0,sep);
      var Valor =values[i].substring(sep+1,esp);
      if (INI==="P1"){
        var B1= Valor
        console.log(B1);
        };
      if (INI==="P2"){
        var B2= Valor
        console.log(B2);
        };
      if (INI==="P3"){
        var B3= Valor
        console.log(B3);
        };
      if (INI==="Peso"){
        var Pes =Valor + " Kg";
        console.log(Pes);
        };
    };
    if (B1!=""){
      mostrarbloques()
    }
    document.getElementById('peso').innerHTML =Pes;
    document.getElementById('bot1').innerHTML =B1;
    document.getElementById('bot2').innerHTML =B2;
    document.getElementById('bot3').innerHTML =B3;
    };
    xhr.send();
  };

  document.getElementById('bot1').addEventListener('click', function() {
    document.getElementById('bot2').disabled = true;
    document.getElementById('bot3').disabled = true;
    document.getElementById('update-button').disabled = false;
    this.disabled = true;
    agregar();
  });
  document.getElementById('bot2').addEventListener('click', function() {
    document.getElementById('bot1').disabled = true;
    document.getElementById('bot3').disabled = true;
    document.getElementById('update-button').disabled = false;
    this.disabled = true;
    agregar();
  });
  document.getElementById('bot3').addEventListener('click', function() {
    document.getElementById('bot2').disabled = true;
    document.getElementById('bot1').disabled = true;
    document.getElementById('update-button').disabled = false;
    this.disabled = true;
    agregar();
  });
  document.getElementById('update-button').addEventListener('click', function() {
    document.getElementById('bot1').disabled = false;
    document.getElementById('bot2').disabled = false;
    document.getElementById('bot3').disabled = false;
    this.disabled = true;
    stop();
  });

  function agregar(){
    let imgDiv = document.getElementById("Video1");
    //alert("video inicio")
    imgDiv.src = "/video_feed";
    let imgDiv2 = document.getElementById("Video2");
    //alert("video inicio")
    imgDiv2.src = "/video2_feed";
  }
  function stop(){
    let imgDiv = document.getElementById("Video1");
    let imgDiv2 = document.getElementById("Video2");
    let timestamp = Math.floor(Date.now());
    console.log("Antes del ajax: " + imgDiv.src);
    //alert("subir foto")
    setTimeout(function() {
      imgDiv.src =
        "static/css/images/temp1.jpg?ver=" + timestamp;
      imgDiv2.src =
        "static/css/images/temp2.jpg?ver=" + timestamp;
      console.log("Después del ajax: " + imgDiv.src);
    }, 500);
    //imgDiv.src = "static/css/images/temp1.jpg";
  }
  

document.addEventListener("DOMContentLoaded", function(event) {
   obtenerRutaImagen()
});

// PROBAR OBTENIENDO EL TEXTO DE PY Y LLEVANDO A JAVA EN JAVA mostraR CON CONDICIONALES LA IMAGEN REAL 

function obtenerRutaImagen() {
  // Realizar la petición AJAX al servidor
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/obtener_imagen');
  xhr.onload = function() {
  var recomenda = xhr.responseText.replace(/["'{}]/g, "");
  var values = recomenda.split(',');
  var miImagen = document.getElementById('recom');
  for (var i in values) {
    var sep = values[i].indexOf(":");
    var esp = values[i].length;
    var INI =values[i].substring(0,sep);
    var Valor =values[i].substring(sep+1,esp);
    Valor=Valor.trim();
    let timestamp = Math.floor(Date.now());
    if (INI==="imagen"){
      console.log(Valor)
      console.log("Antes del ajax: " + miImagen.src);
      if (Valor==="platano"||Valor==="platano "){
        setTimeout(function() {
          miImagen.src =
            "static/css/images/platano.png?ver=" + timestamp;
          console.log("Después del ajax: " + miImagen.src);
        }, 500);
      }
      else if (Valor==="limon"||Valor==="limon "){
        setTimeout(function() {
          miImagen.src =
            "static/css/images/limon.png?ver=" + timestamp;
          console.log("Limon: " + miImagen.src);
        }, 500);
      }
      else if (Valor==="manzana"){
        miImagen.src ="static/css/images/manzana.png";
      }
      else if (Valor==="cebolla"){
        miImagen.src ="static/css/images/cebolla.png";
      }
      else if (Valor==="maiz"){
        miImagen.src ="static/css/images/maiz.png";
      }
      else if (Valor==="papa"){
        miImagen.src ="static/css/images/papa.png";
      }
      else if (Valor==="zanahoria"){
        miImagen.src ="static/css/images/zanahoria.png";
      }
      else if (Valor==="camote"){
        miImagen.src ="static/css/images/camote.png";
      } 
      else if (Valor==="tomate"){
        miImagen.src ="static/css/images/tomate.png";
      }
      else if (Valor==="beterraga"){
        miImagen.src ="static/css/images/beterraga.png";
      }
      else{
        setTimeout(function() {
          miImagen.src =
            "static/css/images/manzana.png?ver=" + timestamp;
        }, 500);
      }
      console.log("Después de iniciar " + miImagen.src);
    };
      };
  };
  
  xhr.send();
};

