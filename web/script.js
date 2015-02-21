//in case I want to do external JS

function socket(){
	var connection = new WebSocket('ws://ocean.redspin.net:8000');
	var index = 0
	var parser = document.createElement('a');

	connection.onopen = function () {
	  //connection.send('Ping'); // Send the message 'Ping' to the server
	  connection.send(welcomeGen());
	};

	// Log errors
	connection.onerror = function (error) {
	  console.log('WebSocket Error ' + error);
	};

	// Log messages from the server
	connection.onmessage = function (e) {
	  //alert('Server: ' + JSON.stringify(e.data));
	  console.log(e);
	  console.log(e.data);
	  if (JSON.parse(e.data).type == "INIT"){
	  	//do the thing?
	  	addRow(JSON.parse(e.data).message, index);
		index++;
	  }
	  else if (JSON.parse(e.data).type == "NORMAL"){
		  addRow(JSON.parse(e.data).message, index);
		  index++;
	  }
	};
	
	function welcomeGen(){
	var id = window.location.hash
	var welcome = '{ "message" : "None",' +
		' "type" : "NEWWEB" ,' +
		' "uid" : "' + id.substring(1) + '"' +
		'}';
	return welcome;
	};

	function addRow(line, index){
		var table = document.getElementById("code-table");
	    var row = table.insertRow(-1);
	    var cell1 = row.insertCell(0);
	    var cell2 = row.insertCell(1);
	    cell1.className = "numbering ::selection";
	    cell1.innerHTML = index;
	    cell2.innerHTML = "<script type='text/plain'>" + line + "</script>";
	}
}