require([
  "jquery",
  "bootstrap"
], function() {

    $('#add-field-link').on('click', function(){
      insetTo = $('#add-link-row');
      $('.field-row').first().clone(true).insertBefore(insetTo);
      return false;
    });

    $('select[name="field-select"]').change(function() {
        alert('Change!!!');
        var text = this.value();

        alert( text );
    });
});
