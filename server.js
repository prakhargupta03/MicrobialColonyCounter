const express = require('express');
const path = require('path');
var bodyParser = require('body-parser');
const multer = require('multer');
var fs = require('fs');

// function to encode file data to base64 encoded string
function base64_encode(file) {
    // read binary data
    var bitmap = fs.readFileSync(file);
    // convert binary data to base64 encoded string
    return new Buffer(bitmap).toString('base64');
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, './images/');
  },
  filename: (req, file, cb) => {
    cb(null,file.originalname);
  },
});
// create the multer instance that will be used to upload/save the file
const upload = multer({ storage });

const app = express();


app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json());
app.use(bodyParser());

// Serve static files from the React app
app.use(express.static(path.join(__dirname, './client/build')));


app.post('/submit', upload.any(), (req, res) => {
  console.log('file count '+req.files.length);

  let {PythonShell} = require('python-shell')
  var pyshell = new PythonShell('code.py');
  pyshell.send(req.files[0].filename);
  pyshell.on('message', function (message) {
	console.log('inside python-shell')
    console.log('result',message);  
	var k=fs.readFileSync(path.join(__dirname, './images', 'output.png'))
	k = k.toString('base64')
	// console.log(k);
	var image = 'data:image/png;base64,'+k;
	var colonycount = message
	var data = {
		image :'data:image/png;base64,'+k,
		colonycount :message
	}
	res.send(data);
	// res.sendFile(path.join(__dirname, './images', 'output.png'));
	// res.download(path.join(__dirname, './images', 'output.png'));
  });
  console.log('outside python-shell');
  // res.send('Done uploading files: '+req.files.length);
});
const port = process.env.PORT || 8000;
app.listen(port);

console.log(`Microbial Colony Counter listening on ${port}`);
