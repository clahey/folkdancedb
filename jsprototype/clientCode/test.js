clahey = {};
clahey.dancedb = {};
clahey.dancedb.createListing = function(listing) {
    return $("<span/>").addClass("danceListing").text(dance.title).data("listing", listing);
};