var thisOS = "mac";
var updatable = "true";
const express = require('express');
var bodyParser = require("body-parser");
var PythonShell = require('python-shell');
const app = express();
var lastUpdate;
var localSoftwaresInfo = [];

// how a json that can be uploaded to the ui chrome extension should looks like
// the updatable property in the json indicates that this software is installed via appstore, thus it can be update with mas
// however, this function is know disable. To enable this function, call a mas script command and then parse the result
// here is an example, 
// activateScript("mas outdated", (stdout)=>{
// 	res.send(parseMasOutput(stdout));
// });
var sampleJson = {
	os: "windows",
	softwares: [
		{
			"name": "line",
			"old_version": "1",
			"new_version": "2",
			"id": "0",
			"updatable": "true"
		},
		{
			"name": "wechat",
			"old_version": "1",
			"new_version": "2",
			"id": "1",
			"updatable": "true"
		},
	]
};

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//activate a script command
//command: a string of script command
//callback: a function of callback function
function activateScript(command, callback){
	var exec = require('child_process').exec;
	exec(command, function(error, stdout, stderr) { console.log(stdout) 
		callback(stdout);
	});
}

// parse mas output from string to json
//stdout: string of mas output
function parseMasOutput(stdout){
	var masList = stdout.split("\n");
	var result = {
		os: thisOS,
		softwares: {}
	}
	var softwareList = [];
	masList.forEach((s)=>{
		if (s != ""){
			var slist = s.split(" ");
			var id = slist[0];
			var name = slist[1];
			var old_version = slist[2].split("(")[1];
			var new_version = slist[4].split(")")[0];
			var tempSoftware = {
				"name": name,
				"old_version": old_version,
				"new_version": new_version,
				"id": id,
				"updatable": updatable
			}
			softwareList.push(tempSoftware);
		}
	});
	result.softwares = softwareList;
	return result;
}

//parse the scraper python result
//result: python scraper result
function parsePythonResult(result){
	var parsedList = [];
	for (var i = 0; i < result.length; i++){
		var appStringSplit = result[i].split("->")
		var appName = appStringSplit[0];
		var version = appStringSplit[1];
		parsedList.push({
			"name": appName,
			"old_version": "1",
			"new_version": version,
			"id": "0",
			"updatable": "false"
		});
	}
	return parsedList;
}

//activate python to scrap the latest version of softwares that are install on this computer
//args: argument to send to the python scraper. The software names
//localSoftwares_incomplete: the local softwares json(a list of json of local software's info)
function setCompleteInfo(args, localSoftwares_incomplete){
	var options = {
	    mode: 'text',
	    args: args
	};
	var returnList = [];
	PythonShell.run('/localhost/java_interface.py', options, function (err, results) {
	    if (err) throw err;
	    // results is an array consisting of messages collected during execution
	    console.log('results: %j', results);
	    var parsedList = parsePythonResult(results);
	    for (var i = 0; i < parsedList.length; i++){
	    	for (var j = 0; j < localSoftwares_incomplete.length; j++){
	    		if(parsedList[i].name == localSoftwares_incomplete[j].name){
	    			// if old version equals new version, remove it from parsed list because it doesn't need to update
	    			if (parsedList[i].new_version == localSoftwares_incomplete[j].old_version){
	    				parsedList.splice(i,1)
	    				break;
	    			}
	    			parsedList[i].old_version = localSoftwares_incomplete[j].old_version;
	    			console.log("match found " + parsedList[i].name);
	    			localSoftwares_incomplete.splice(j,1);
	    			break;
	    		}
	    	}
	    }
	    localSoftwaresInfo = parsedList;
	});
}

//get all the apps that's install on the current computer and also get the version of them
//haven't implement the version checking frequency
function checkNewApp (){
	if (lastUpdate == undefined){
		activateScript("system_profiler SPApplicationsDataType", (stdout)=>{
			var softwareInfos = stdout.split("\n\n");
			var softwareName;
			var softwareNames = [];
			var localSoftwares_incomplete = [];
			softwareInfos.forEach((ASoftwareInfo)=>{
				var lines = ASoftwareInfo.split("\n");
				if (lines.length === 1){
					var nameLine = lines[0];
					var nameLineSplit = nameLine.split(":");
					softwareName = nameLineSplit[0].replace(/ /g,'');
				}else {
					var versionLine = lines[0];
					var versionSplit = versionLine.split(": ");
					softwareNames.push(softwareName);
					var tempAppInfo = {
						"name": softwareName,
						"old_version": versionSplit[1],
						"new_version": 2,
						"id": "0",
						"updatable": "false"
					}
					localSoftwares_incomplete.push(tempAppInfo);
				}
			});
			setCompleteInfo(softwareNames, localSoftwares_incomplete);
			lastUpdate = new Date();
		});
	}
}


//activate CORS
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});
app.get('/', (req, res) => {
	console.log("get request");
	var localAppJson = {
		os: "mac",
		softwares: localSoftwaresInfo
	};
	res.send(localAppJson);
	// activateScript("mas outdated", (stdout)=>{
	// 	res.send(parseMasOutput(stdout));
	// });
})
app.post('/updateThis/*', (req, res) => {
	var updateItemID = (req.body).updateItemID;
	console.log("get update command " + updateItemID);
	// res.send(localSoftwares);
	activateScript("mas upgrade " + updateItemID, (stdout)=>{
		res.send(stdout);
	});
})
checkNewApp();
app.listen(3333, () => console.log('Example app listening on port 3333!'))






