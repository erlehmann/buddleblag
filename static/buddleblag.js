jQuery(function() {
    jQuery('.editable').hallo({
      plugins: {
        'halloformat': {},
        'halloblock': {},
        'hallojustify': {},
        'hallolists': {},
        'hallolink': {},
        'halloreundo': {}
      },
      editable: true,
      toolbar: 'halloToolbarFixed'
    });

    jQuery('.editable').bind('blur', function(event, data) {
        jQuery.post(this.dataset['url'], {
            content: jQuery(this).html(),
            name: "John",
            email: "john@example.org",
            message: "javascript edit"
        });
        this.hallo({editable: false});
    });
});
