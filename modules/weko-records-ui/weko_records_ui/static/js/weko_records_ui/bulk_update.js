require([
  "jquery",
  "bootstrap"
], function() {
    $('#add-field-link').on('click', function(){

      insetTo = this.parent().parent();
      $('.field-row-default').clone(true).insertBefore(insetTo);


      return false;
    });

});
