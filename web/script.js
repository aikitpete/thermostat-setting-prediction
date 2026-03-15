$(document).ready(function () {
$("#form1").alpaca({
                "schema": {
                    "title": "What inputs you want to use?",
                    "type": "object",
                        "properties": {
                        	"Temperature": {
                            	"type": "number",
								"minimum": -20,
								"maximum": 50,
								"required": true,
                                "title": "[WEATHER] Temperature (20-45 recommended)"
                        	},
                            "Humidity": {
                            	"type": "number",
								"minimum": 0,
                                "maximum": 100,
								"required": true,
                                "title": "[WEATHER] Humidity (50-90 recommended)"
                        	},
                            "Wind": {
                            	"type": "number",
								"minimum": 0,
                                "maximum": 50,
								"required": true,
                                "title": "[WEATHER] Wind (0-30 recommended)"
                        	},
                        	"Temperature Preference": {
                            	"type": "number",
								"minimum": -20,
								"maximum": 50,
								"required": true,
                                "title": "[GUEST] Temperature Preference (20-45 recommended)"
                        	},
                            "Time": {
								"type":"string",	
                                "title": "[FLIGHT] Arrival Time",
								"required": true,
            					//"format": "HH:mm:ss",
                        		"default": 'morning',
								"enum": ['morning', 'noon', 'evening', 'midnight']
                        }
                    }
                },
		"options": {
                        "form":{
                            //"attributes":{
                            //    "action":"TestScriptManual.fcgi",
                            //    "method":"post"
                            //},
                            "buttons":{
                                "submit":{
                                    "title": "Send to Azure Web Service",
                                    "click": function() {
                                        var val = this.getValue();
                                        submit(val);
					//if (this.isValid(true)) {
                                        //    alert("Values sent: " + JSON.stringify(val, null, "  "));
                                        //    this.ajaxSubmit().done(function() {
                                        //        alert("Posted!");
                                        //    });
                                        //} else {
                                        //    alert("Invalid values: " + JSON.stringify(val, null, "  "));
                                        //}
                                    }
                                }
                            }
			}
			}
            	});

function submit(data) {
	$.ajax({
        	type: 'POST',
        	//url: "http://www.petegerhat.com/azure/TestScriptManual.py",
		//url: "http://www.petegerhat.com/azure/testcgi.py",
        	//url: "http://www.petegerhat.com/azure/main.py",
		url: "http://www.petegerhat.com/azure/TestScriptManual.fcgi?"+$.param(data),
		//data: {
		//	param: data
		//}, //passing some input here
        //dataType: "text",
        success: function(response){
			//alert(data);
			//alert($.param(data));
           	//alert("Response: "+response);
			//data = JSON.parse(response);
			//alert(data['Results']['output1']['value']['Values'][7]);
			//$('#debug').html(output);
			updateTable(response);
   		}
	}).done(function(){
		
	});
}

function updateTable(response){
    	//console.log(data);
    	//alert(data);
		if (response!=null) {
			$('#debug').html(response);
			var data = JSON.parse(response);
			//alert(data.count);
    	} else {
    		var data = new Array();
    	}
		var r = new Array(), j = -1;
		r[++j] ='<thead><tr><th class="tg-baqh" colspan="10">Results</th></tr><tr><th>';
		r[++j] = 'Timestamp';
		r[++j] = '</th><th>';
		r[++j] = 'Temperature';
		r[++j] = '</th><th>';
		r[++j] = 'Wind';
		r[++j] = '</th><th>';
		r[++j] = 'Humidity';
		r[++j] = '</th><th>';
		r[++j] = 'Temperature Preference';
		r[++j] = '</th><th>';
		r[++j] = 'Morning';
		r[++j] = '</th><th>';
		r[++j] = 'Noon';
		r[++j] = '</th><th>';
		r[++j] = 'Evening';
		r[++j] = '</th><th>';
		r[++j] = 'Midnight';
		r[++j] = '</th><th>';
		r[++j] = '<strong>Recommended AC Setting (How long before to turn on AC?)</strong>';
		r[++j] = '</th></tr></thead>';
		var size = 6;
		for (var key=0, size=data.length; key<size; key++){
     			r[++j] ='<tr><td>';
     			r[++j] = data[key][0];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][1];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][2];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][3];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][4];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][5];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][6];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][7];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][8];
     			r[++j] = '</td><td>';
     			r[++j] = data[key][9];
     			r[++j] = '</td></tr>';
		}
		$('#dataTable').html(r.join('')); 
}
/*var param = new Array();
param[0] = new Array;
param[1] = new Array;
param[2] = new Array;
param[0][0] = "00";
param[0][1] = "00";
param[0][2] = "00";
param[1][0] = "00";
param[1][1] = "00";
param[1][2] = "00";
param[2][0] = "00";
param[2][1] = "00";
param[2][2] = "00";*/
//updateTable(new Array());

$.ajax({
    	type: 'POST',
    	//url: "http://www.petegerhat.com/azure/TestScriptManual.py",
	//url: "http://www.petegerhat.com/azure/testcgi.py",
    	//url: "http://www.petegerhat.com/azure/main.py",
	url: "http://www.petegerhat.com/azure/TestScriptManual.fcgi",
	//data: {
	//	param: data
	//}, //passing some input here
    //dataType: "text",
    success: function(response){
		//alert(data);
		//alert($.param(data));
       	//alert("Response: "+response);
		//data = JSON.parse(response);
		//alert(data['Results']['output1']['value']['Values'][7]);
		//$('#debug').html(output);
		updateTable(response);
	}
}).done(function(){
	
});

$("#submit").click(function() {

  //$.ajax({
  //type: "POST",
  //url: "RequestResponse.py",
  //data: { param: ""}
  //}).done(function( o ) {
  //alert("Body!");
});

  //var url = 'https://europewest.services.azureml.net/workspaces/8a441e205cc444b9857777ace9d422bb/services/86c9bc5197f646269ded6dce7e95a2c9/execute?api-version=2.0&details=true';
  //var api_key = 'y02I/HrFvr/Spfuz5LI5VKcdLfEslc+m6HPvLYNrz5s9nAyNkE8DKEnPCmDvuISOXsHHtls2rPTTP94IrtYNvQ==';
  //var headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)};
  
//    alert("Done!");
});

