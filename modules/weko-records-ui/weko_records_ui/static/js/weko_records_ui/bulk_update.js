require([
  "jquery",
  "bootstrap"
], function() {
    $('#add-field-link').on('click', function(){

      insetTo = $('#add-link-row');
      $('.field-row').first().clone(true).after('<br>').insertBefore(insetTo);


      return false;
    });

});
