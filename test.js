var fs = require("fs");

var data = fs.readFileSync(__dirname+"/a2oj_copy.json", 'utf8')
data = JSON.parse(data)

console.log(data.length);