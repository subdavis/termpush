//in case I want to do external JS

function socket(){
	var connection = new WebSocket('ws://ocean.redspin.net:8000');

	connection.onopen = function () {
	  //connection.send('Ping'); // Send the message 'Ping' to the server
	  connection.send(welcomeGen())
	  alert("connected!");
	};

	// Log errors
	connection.onerror = function (error) {
	  console.log('WebSocket Error ' + error);
	};

	// Log messages from the server
	connection.onmessage = function (e) {
	  alert('Server: ' + JSON.stringify(e.data));
	  console.log(e)
	  console.log(e.data)
	};
	function welcomeGen(){
	var id = window.location.pathname
	var welcome = '{ "message" : "None",' +
		' "type" : "NEWWEB" ,' +
		' "uid" : "' + prompt("ID?") + '"' +
		'}';
	return welcome;
	};
}

/*
function socket(){
	var uri = "ws://ocean.redspin.net:8081";
	ws = new Websock();
	ws.open(uri);
	ws.on('open', function (e) {
        alert("Connected");
        ws.send(welcomeGen());
    });
    ws.on('message', function (e) {
        alert("Received: " + ws.rQshiftStr());
    });
    ws.on('close', function (e) {
        alert("Disconnected");
    });
}
function welcomeGen(){
	var id = window.location.pathname
	var welcome = '{ "message" : "None",' +
		' "type" : "NEWWEB" ,' +
		' "uid" : "' + prompt("ID?") + '"' +
		'}';
	alert(welcome)
	return welcome;
}
*/