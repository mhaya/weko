require([
  "jquery",
  "bootstrap"
], function() {

    // Add field
    $('#add-field-link').on('click', function(){
      insetTo = $('#add-link-row');
      $('.field-row').first().clone(true).insertBefore(insetTo);
      return false;
    });

    // Remove field
    $('.del-field').on('click', function(){
      $(this).parents('.field-row').remove();
      return false;
    });

    $('input[name="access_type"]').change(function() {
      var selected = $(this).val();
      accessDate = $(this).parents('.access-type-select').find('input[name="access_date"]');
      if(selected == 'open_access_date'){
        $(accessDate).removeAttr("disabled");
      }else {
        $(accessDate).attr('disabled', 'disabled');
      }
    });

    $('select[name="field-select"]').change(function() {
      var selected = $(this).val();
//      alert($('input[name="access_type"]:checked').val());
      contents = $(this).parents('.field-row').find('.field-content');
      contents.each(function(i, elem) {
        var elemAttr = $(elem).attr('class');

        // Access Type
        if(elemAttr.indexOf('access-type-select') >= 0){
          if('1' == selected.toString()){
            $(elem).removeAttr("hidden");
          }else {
            $(elem).attr('hidden', 'hidden');
          }

        // Licence
        }else if(elemAttr.indexOf('licence-select') >= 0){
          if('2' == selected.toString()){
            $(elem).removeAttr("hidden");
          }else {
            $(elem).attr('hidden', 'hidden');
          }

        // Licence Description
        }else if(elemAttr.indexOf('licence-description') >= 0){
          if('3' == selected.toString()){
            $(elem).removeAttr("hidden");
          }else {
            $(elem).attr('hidden', 'hidden');
          }

        }

      });


    });
});
