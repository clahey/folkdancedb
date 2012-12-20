libxmljs = require("libxmljs");
fs = require("fs");
path = require("path");

parseFigure = function(node) {
    var retval = {};
    retval.figure = node.name();
    if (node.name() == "while") {
	retval.sequence = [];
	node.find("*").forEach(function(childNode) {
	    retval.sequence.push(parseFigure(childNode));
	});
    } else {
	node.find("@*").forEach(function(attr) {
	    retval[attr.name()] = attr.text();
	});
    }
    return retval;
}

exports.parseDance = function(xmldata) {
    var retval = {};
    var xmlDoc = libxmljs.parseXmlString(xmldata);
    ["author", "dancetype", "formation", "goodtune", "note",
     "title", "year"].forEach(function(key) {
	 node = xmlDoc.get(key);
	 if (node) {
	     retval[key] = node.text();
	 }
     });
    retval.sequence = [];
    xmlDoc.find("sequence/*").forEach(function(node) {
	retval.sequence.push(parseFigure(node));
    });
    return retval;
};

exports.loadDance = function(filename, callback) {
    fs.readFile(filename, function(err, data) {
	if (err) {
	    callback(err, null);
	} else {
	    callback(null, exports.parseDance(data));
	}
    });
};

exports.loadDances = function(directory, callback) {
    fs.readdir(directory, function(err, files) {
	if (err) {
	    callback(err, null);
	}
	var count = 1;
	var dances = [];
	function decrement() {
	    count --;
	    if (count == 0) {
		callback(null, dances);
	    }
	}
	files
	    .filter(function(filename) { return path.extname(filename) == ".xml"; })
	    .forEach(function(filename) {
		count ++;
		exports.loadDance(path.join(directory, filename),
				  function(err, dance) {
				      if (err == null) {
					  dances.push(dance);
				      }
				      decrement();
				  });
	    });
	decrement();
    })
};