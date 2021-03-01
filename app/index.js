/* csv to json */
const express = require("express"),
  app = express();

var http = require('http');
var path = require("path");
var bodyParser = require('body-parser');
var helmet = require('helmet');

app.use(bodyParser.urlencoded({extended: false}));

const port = process.env.PORT || 4000

app.listen(port, () => { 
	console.log(`server running on port at ${port}`); 
})

app.get('/', function(req, res){
    res.sendFile(path.join(__dirname,'index.html'));
});

app.post('/getscore', getscore);

function getscore(req, res){

	var spawn = require("child_process").spawn;

	console.log(req.body.patentNumber)
	
    var process = spawn('python',["./mainfile.py", req.body.patentNumber]);

	process.stdout.on('data', function(data) {
		res.send("<p>Input patent number: "+req.body.patentNumber+"</p><p>"+data.toString()+"</p>"); 
	})

	process.stderr.on('data', function(data){
		res.send(data.toString());
	});

}

// Express function to get the input of the Patent numbers csv file
// app.post('/getscorecsv', getscorecsv);

// function getscorecsv(req, res){

//     patentNumbersList = req.files.csvfile.data.toString('utf8');
//     filteredArray = cleanArray(patentNumbersList.split(/\r?\n/))
//     patentNumbersList = get_array_string(filteredArray)

// 	var spawn = require("child_process").spawn;
	
//     var process = spawn('python',["./mainfile.py", 
// 							req.body.patentNumbersList]);


// 	dataString = ""
// 	process.stdout.on('data', function(data) {

// 		dataString = dataString + data.toString()
// 		res.setHeader('Content-disposition', 'attachment; filename=test.csv');
// 		res.set('Content-Type', 'text/csv');
// 		res.status(200).send(dataString);
			
// 	})

// 	process.stderr.on('data', function(data){
// 		res.send(data.toString());
// 	});


// }


