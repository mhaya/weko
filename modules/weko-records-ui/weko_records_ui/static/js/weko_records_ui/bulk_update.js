require([
  "jquery",
  "bootstrap"
], function() {

    $(document).ready(function() {
      newField = $('.field-row-default').first().clone(true)
      $(newField).attr('class', 'row field-row');
      $(newField).removeAttr("hidden");

      $(newField).insertBefore($('#add-field-row'));

    });

    // Add field
    $('#add-field-link').on('click', function() {
      newField = $('.field-row-default').first().clone(true)
      $(newField).attr('class', 'row field-row');
      $(newField).removeAttr("hidden");

      $(newField).insertBefore($('#add-field-row'));

      return false;
    });

    // Remove field
    $('.del-field').on('click', function() {
      if($('#field-panel').find('.field-row').length > 1) {
        $(this).parents('.field-row').remove();
      }
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

    // Select All
    $('#select-all').on('click', function() {
      hasChecked = false;
      hasCanceled = false;

      checkboxes = $(this).parent().find('input[type="checkbox"]');
      checkboxes.each(function(i, elem) {
        if($(elem).prop('checked') === false){
          hasCanceled = true;
        }else {
          hasChecked = true;
        }
      });

      // Cancel all
      if(hasChecked && !hasCanceled) {
        checkboxes.each(function(i, elem) {
//          $(elem).removeAttr("checked");
          $(elem).prop("checked", false);
        });

      // Check all
      }else {
        checkboxes.each(function(i, elem) {
          $(elem).prop("checked", true);
//          $(elem).attr('checked', 'checked');

        });
      }

      return false;
    });

    // Bulk Update
    $('#submit-btn').on('click', function() {

      $.ajax({
        method: 'GET',
        url: '/bulk_update/items_metadata',
        async: false,
        success: function(data, status){
          alert(data);
//          properties_obj = data;
//
//          defProps = data.defaults;
//          isSelected = true;
//          Object.keys(defProps).forEach(function(key) {
//            if (isSelected) {
//              select_option = select_option + '<option value="' + defProps[key].value + '" selected>' + defProps[key].name + '</option>';
//              isSelected = false;
//            } else {
//              select_option = select_option + '<option value="' + defProps[key].value + '">' + defProps[key].name + '</option>';
//            }
//          });
//
//          odered = {}
//          others = ''
//          for (var key in data) {
//            if (key == 'defaults') continue;
//
//            option = '<option value="cus_' + key + '">' + data[key].name + '</option>'
//            if (data[key].sort != null) {
//              odered[data[key].sort] = option;
//            } else {
//              others = others + option;
//            }
//          }
//
//          Object.keys(odered).forEach(function(key) {
//            select_option = select_option + odered[key];
//          });
//          select_option = select_option + others;

        },
        error: function(status, error){
          console.log(error);
        }
      });


    });

});
