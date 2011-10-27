"use strict";

DomReady.ready(function() {
    makeAllContentEditable()
});

function collectionToArray(collection) {
    var array = [];
    var i = collection.length;
    while (i--) {
        array.push(collection[i]);
    }
    return array;
}

function makeAllContentEditable() {
    var editElements = collectionToArray(document.getElementsByClassName("editable"));
    for (e in editElements) {
        e.contentEditable = !e.isContentEditable;
    }
}
