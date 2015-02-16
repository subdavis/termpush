//in case I want to do external JS

function socket(){
	var connection = new WebSocket('ws://ocean.redspin.net:8000');
	var index = 0

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
	  //alert('Server: ' + JSON.stringify(e.data));
	  console.log(e)
	  console.log(e.data)
	  addRow(JSON.parse(e.data).message, index)
	  index++;
	};
	
	function welcomeGen(){
	var id = window.location.pathname
	var welcome = '{ "message" : "None",' +
		' "type" : "NEWWEB" ,' +
		' "uid" : "' + prompt("ID?") + '"' +
		'}';
	return welcome;
	};

	function addRow(line, index){
		var table = document.getElementById("code-table");
	    var row = table.insertRow(-1);
	    var cell1 = row.insertCell(0);
	    var cell2 = row.insertCell(1);
	    cell1.className = "numbering";
	    cell1.innerHTML = index;
	    cell2.innerHTML = line;
	}
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