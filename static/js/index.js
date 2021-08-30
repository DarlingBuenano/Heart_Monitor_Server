var webSocket = new WebSocket('ws://localhost:8000/wsocket/guardarSalurCardiaca/');
webSocket.onopen = function(event){console.log("Conexion abierta")}
webSocket.onclose = function(event){console.log("Conexion cerrada")}
webSocket.onmessage = function(event){console.log(event.data)}

var fecha = new Date();
var msg = {
    usuario: 1,
    paciente: 1,
    familiar: 1,
    bpm: "85",
    fecha: (fecha.getFullYear() + "-" + (fecha.getMonth() + 1) + "-" + fecha.getDate()),
    hora: new Date().toLocaleTimeString()
};
//webSocket.send(JSON.stringify(msg));