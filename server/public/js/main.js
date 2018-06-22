var socket = io();

$(document).ready(function(){
    $("#send-message").click(function(){
        var msg = $('#filename').val();
    	socket.emit('message', msg);
    	$('#messages').append($('<p>').text(msg));
    	$('#filename').val('');
    	return false;
    });
    
});
socket.on('message', function (msg) {
    $('#messages').append($('<p>').text(msg));
});