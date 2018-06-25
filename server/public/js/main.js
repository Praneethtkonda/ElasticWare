//var sourceFile = require('../../app.js');
var socket = io();
//console.log(sourceFile.clients);
//$("#clients").html("<h3>"+sourceFile.clients+"<h3>");
$(document).ready(function(){
    $("#send-message").click(function(){
        var msg = $('#filename').val();
        $el = msg;
    	socket.emit('message', msg); 
    	//$("#messages").prepend("<div id='messages'><h3 style='text-align:center;background-color:#20c997'>"+$el +"</h3></div>")
       // $("#messages").prepend("<div class='alert alert-success' role='alert'>"+ $el +"</div>");
    	$('#filename').val('');
    	return false;
    });
    
});
socket.on('message', function (msg) {
	$el = msg;
  	//$("#messages").prepend("<div id='messages'><h3 style='text-align:center;background-color:#20c997'>"+ $el +"</h3></div>")
    $("#messages").prepend("<div class='alert alert-success' role='alert'>"+ $el +"</div>");
});