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
        if ((this.dataset['url'] !== undefined) &&
            jQuery(this).hasClass('isModified')) {
            // it would be better if hallo.js would not emit <br>
            jQuery(this).find('br').remove();
            jQuery.post(this.dataset['url'], {
                content: jQuery(this).html(),
                name: "John",
                email: "john@example.org",
                message: "javascript edit"
            });
            jQuery(this).removeClass('isModified');
        };
        this.hallo({editable: false});
    });

    jQuery('#new-headline').bind('hallomodified', function(event, data) {
        jQuery('#new-content').attr('data-url', '/'+encodeURI(
            jQuery('#new-headline').text()
        ));
    });
});
