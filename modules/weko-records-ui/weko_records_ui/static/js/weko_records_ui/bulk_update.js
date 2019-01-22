require([
  "jquery",
  "bootstrap"
], function() {
    $('#add-field-link').on('click', function(){

      insetTo = $('#add-field-row');
      $('.field-row-default').clone(true).insertBefore(insetTo);


      return false;
    });

});
