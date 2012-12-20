String.prototype.startsWith = function(needle) {
    return this.substr(0, needle.length) == needle;
}

String.prototype.endsWith = function(needle) {
    return this.slice(-needle.length) == needle;
}