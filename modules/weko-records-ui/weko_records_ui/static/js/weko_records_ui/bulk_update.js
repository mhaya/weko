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
      var selected = $(this).val();

      contents = $(this).parents('.field-row').find('.field-content');
      contents.each(function(i, elem) {
          if('3' === str(selected)){
            $(elem).removeAttr("hidden");
          }

      });


    });
});
