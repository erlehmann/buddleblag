jQuery(function() {
    jQuery('.editable').hallo({
      plugins: {
        'halloformat': {},
        'halloblock': {},
        'hallolists': {},
        'hallolink': {},
        'halloreundo': {}
      },
      editable: true,
      toolbar: 'halloToolbarFixed'
    });

    jQuery('.editable').bind('blur', function(event, data) {
        if (this.dataset['url'] != undefined) {
            jQuery.post(this.dataset['url'], {
                content: jQuery(this).html(),
                name: "John",
                email: "john@example.org",
                message: "javascript edit"
            });
        };
        this.hallo({editable: false});
    });

    jQuery('#new-headline').bind('hallomodified', function(event, data) {
        jQuery('#new-content').attr('data-url', '/'+encodeURI(
            jQuery('#new-headline').text()
        ));
    });
});
