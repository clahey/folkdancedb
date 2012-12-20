openDance = function(listing) {
    div = $("<div/>").text("loading");
    $.getJSON("data/" + listing.href, function(dance) {
	div.text(JSON.stringify(dance));
    });
    return div;
}

createListing = function(listing) {
    return $("<div/>").addClass("danceListing").text(listing.title).data("listing", listing);
};

$(function(){
    $("#evening-trash").droppable(
	{ 'accept' : "#evening li",
	  'drop' : function(event, ui) {
	      ui.draggable.hide("slow", function() {
		  ui.draggable.remove();
	      });
	      $("#evening-trash-icon-container").removeClass("trash-drop-size", 50);
	  },
	  'over' : function(event, ui) {
	      $("#evening-trash-icon-container").addClass("trash-drop-size", 50);
	  },
	  'out' : function(event, ui) {
	      $("#evening-trash-icon-container").removeClass("trash-drop-size", 50);
	  },
	  'tolerance': 'pointer' });
    $("#evening").sortable({ 'tolerance': 'pointer' });
    $.getJSON("data/list", function(results) {
	results.result.sort(function(listinga, listingb) {
	    return listinga.title.localeCompare(listingb.title);
	}).forEach(function(listing) {
	    li = $("<li/>").append(createListing(listing)).addClass("ui-state-highlight");
	    li.dblclick(function(event) {
		openDance(listing).dialog({ modal: true });
	    });
	    $("#available").append(li);
	    li.draggable({ 'revert' : 'invalid',
			   'connectToSortable' : '#evening',
			   'helper' : 'clone' });
	});
    });
});
