% rebase base config=config, helpers=helpers, auth=auth

<article>
    % include post-content post=post, helpers=helpers
</article>

<button id="enable">Edit</button>
<button id="disable">Save</button>

<script src="/static/jquery-1.7.1.min.js"></script>
<script src="/static/jquery-ui-1.8.18.custom.min.js"></script>

<script src="/static/rangy-core-1.2.3.js"></script>
<script src="/static/hallo-min.js"></script>

<script>
  jQuery('#enable').button().click(function() {
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
    jQuery('.editable').bind('hallomodified', function(event, data) {
        jQuery('#modified').html("Editables modified");
    });
    jQuery('.editable').bind('halloselected', function(event, data) {
        jQuery('#modified').html("Selection made");
    });
    jQuery('.editable').bind('hallounselected', function(event, data) {
        jQuery('#modified').html("Selection removed");
    });
    jQuery('.editable').bind('hallorestored', function(event, data) {
        jQuery('#modified').html("restored");
    });
  });
  jQuery('#disable').button().click(function() {
    jQuery('.editable').hallo({editable: false});
    jQuery.post("/{{post.title}}", {
        content: jQuery("#post").html(),
        name: "John",
        email: "john@example.org",
        message: "javascript edit"
    });
  });
  jQuery('.editable').bind('hellodeactivated', function() {
      alert("foobar");
    $(this).hallo({editable:false});
  });
</script>
