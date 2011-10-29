'use strict'

DomReady.ready(function() {
    addEditHandlers()
})

function makeEditable() {
    var editable = document.getElementsByClassName('editable')
    for (var e in editable) {
        editable[e].contentEditable = true
    }
}

function addEditHandlers() {
    var editableElements = document.getElementsByClassName('editable')
    for (e in editableElements) {
        editableElements[e].onclick = "makeEditable()"
    }
}
