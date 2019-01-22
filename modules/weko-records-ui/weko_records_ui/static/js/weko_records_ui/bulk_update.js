require([
  "jquery",
  "bootstrap"
], function() {

    $('#add-field-link').on('click', function(){
      insetTo = $('#add-link-row');
      $('.field-row').first().clone(true).insertBefore(insetTo);
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
        alert($(elem).attr('class'));
      });

      if('1' === selected.toString()){
//        contents = $(this).parents('.field-row').find('.field-content');
//        contents.each(function(i, elem) {
//          alert($(elem).attr('class'));
//            if('3' === selected.toString()){
//              $('select[name="licence-select"]')
//
//            }
//
//            if('4' === selected.toString()){
//              $(elem).removeAttr("hidden");
//            }else if($(elem).attr('hidden') == undefined) {
//              $(elem).attr('hidden', 'hidden');
//
//            }

//        });
      }


    });
});
