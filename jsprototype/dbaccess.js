var EventEmitter = require('events').EventEmitter;
loadxml = require('./loadxml');
path = require("path");

module.exports = new EventEmitter();

module.exports.ready = false;
module.exports.mongo = require("mongodb");

client = new module.exports.mongo.Db(
    'dances', new module.exports.mongo.Server("127.0.0.1", 27017, {}))

client.open(function(err, p_client) {
    count = 2;
    finish = function() {
	count--;
	if (count == 0) {
	    module.exports.ready = true;
	    module.exports.emit('ready');
	}
    }
    client.collection('dances', function(err, collection) {
	dancecollection = collection;
	module.exports.dancecollection = collection;
	finish();
    });
    client.collection('evenings', function(err, collection) {
	eveningcollection = collection;
	module.exports.eveningcollection = collection;
	finish();
    });
});

module.exports.whenReady = function(callback) {
    if (module.exports.ready) {
	callback(null);
    } else {
	module.exports.on("ready", function() {
	    callback(null);
	});
    }
}

module.exports.importDance = function (filename, callback) {
    dancecollection.find({ "filesource": path.basename(filename) })
	.toArray(function(err, res) {
	    if (res && res.length > 0) {
		if (callback) {
		    callback("present", null);
		}
	    } else {
		loadxml.loadDance(filename, function(err, dance) {
		    if (err) {
			if (callback) {
			    callback(err, null);
			}
		    } else {
			dance.filesource = path.basename(filename);
			dancecollection.insert(dance, function(err, docs) {
			    if (callback) {
				callback(err, dance);
			    }
			});
		    }
		});
	    }
	});
}

module.exports.importDances = function(directory, callback) {
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
	    .filter(function(filename) {
		return path.extname(filename) == ".xml"; })
	    .forEach(function(filename) {
		count ++;
		module.exports.importDance(path.join(directory, filename),
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
