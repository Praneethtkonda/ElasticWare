var socket = io();
$(document).ready(function(){
    $("#send-message").click(function(){
        var msg = $('#filename').val();
        $el = msg;
    	socket.emit('message', msg)
    	$("#messages").prepend("<div id='messages'><h3 style='text-align:center;background-color:#20c997'>"+$el +"</h3></div>")
    	$('#filename').val('');
    	return false;
    });
    
});

socket.on('message', function (msg) {
	$el = msg;
  	$("#messages").prepend("<div id='messages'><h3 style='text-align:center;background-color:#20c997'>"+ $el +"</h3></div>")
});