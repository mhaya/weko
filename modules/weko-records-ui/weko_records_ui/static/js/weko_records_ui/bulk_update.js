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
      alert($('input[name="access_type"]:checked').val());

//      if('3' === selected.toString()){
//        content = $(this).parents('.field-row').find('.field-content.licence-select');
//        $(content).removeAttr("hidden");
//      }
//      contents.each(function(i, elem) {
//          if('3' === selected.toString()){
//            $('select[name="licence-select"]')
//
//          }
//
//          if('4' === selected.toString()){
//            $(elem).removeAttr("hidden");
//          }else if($(elem).attr('hidden') == undefined) {
//            $(elem).attr('hidden', 'hidden');
//
//          }
//
//      });


    });
});
