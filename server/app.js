var app = require('express')();
var express = require('express');
var http = require('http').Server(app);
var io = require('socket.io')(http);
var path = require('path');


var routes = require('./routes/index');

app.set('views',path.join(__dirname,'views'));
app.set('view engine', 'pug');


app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('message', function(msg){
  	socket.broadcast.emit('message',msg)
    console.log('message: ' + msg);
  });
});

http.listen(3000, function(){
  console.log('listening on port 3000');
});