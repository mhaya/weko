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
      contents = $(this).parents('.field-row').find('.field-content');
      contents.each(function(i, elem) {
        var elemAttr = $(elem).attr('class');
        // Access Type
        if(elemAttr.indexOf('access-type-select') >= 0){
          if('1' === selected.toString()){
            $(elem).removeAttr("hidden");
          }else {
            $(elem).attr('hidden', 'hidden');
          }

        // Licence
        }else if(elemAttr.indexOf('licence-select') >= 0){
          if('2' === selected.toString()){
            $(elem).removeAttr("hidden");
          }else {
            $(elem).attr('hidden', 'hidden');
          }

        // Licence Description
        }else if(elemAttr.indexOf('licence-description') >= 0){
          if('3' === selected.toString()){
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

      // Get id
      pids = '';
      $('input[type="checkbox"]').each(function(i, elem) {
        if($(elem).prop('checked') === true){
          if(pids === '') {
            pids = $(elem).prop('value');
          } else {
            pids = pids + '/' + $(elem).prop('value');
          }
        }
      });
      if (pids === '') {
        alert('Please select items to update.');
        return;
      }

      // Get setting fields
      $('.row.field-row').each(function(i, row) {
        $(row).find('select[name="field-select"]').each( function(i, field) {
          // Access Type
          if($(field).prop('value') === '1') {
            alert($(row).find('input[name="access_type"]:checked').length);
//            $(row).find('input[name="access_type"]:checked').each( function(i, field) {
//            
//
//            });

          }else if($(field).prop('value') === '2') {
            alert('Licence');

          }else if($(field).prop('value') === '3') {
            alert('Licence Description');

          }
        });



      });



      accessTypes = [];
      $('input[name="access_type"]:checked').each( function(i, elem) {
//        alert($(elem).prop('value'));
//        if($(elem).prop('value') !== 'unselected'){
//          licences.push($(elem).prop('value'));
//        }
      });

      licences = [];
      $('select[name="licence-select"]').each( function(i, elem) {
        if($(elem).prop('value') !== 'unselected'){
          licences.push($(elem).prop('value'));
        }
      });



//      getUrl = '/bulk_update/items_metadata?pids=' + pids;
//      $.ajax({
//        method: 'GET',
//        url: getUrl,
//        async: false,
//        success: function(data, status){
//
//          var redirect_url = "/api/deposits/redirect";
//          var items_url = "/api/deposits/items";
//
//          itemsMeta = data;
//          Object.keys(itemsMeta).forEach(function(pid) {
//
//            if (Object.keys(itemsMeta[pid].contents).length !== 0) {
//
//              Object.keys(itemsMeta[pid].contents).forEach( function(contentKey) {
//                var contentsMeta = itemsMeta[pid].contents[contentKey];
//                $.each( contentsMeta, function( key, value ) {
//                  value.licensetype = 'license_1';
//
//
//
//
//                });
//                itemsMeta[pid].meta[contentKey] = contentsMeta
//
//              });
//
//            }
//
//            meta = JSON.stringify(itemsMeta[pid].meta);
//            index = JSON.stringify(itemsMeta[pid].index);
//
//            index_url = redirect_url + "/" + pid;
//            self_url = items_url + "/" + pid;
//
//            // Update items
//            updateItems(index_url,
//                        self_url,
//                        meta,
//                        index);
//
//          });
//
//        },
//        error: function(status, error){
//          console.log(error);
//        }
//      });


    });

    function updateItems(index_url, self_url, itemData, indexData) {
      // Post to index select
      $.ajax({
        type: "PUT",
        url: index_url,
        async: false,
        cache: false,
        data: itemData,
        contentType: "application/json",
        success: function() {
          // Post item data
          $.ajax({
            type: "PUT",
            url: self_url,
            async: false,
            cache: false,
            data: indexData,
            contentType: "application/json",
            success: function(){
              alert('Success!!!!');
            },
            error: function() {
              alert('Error at Post item data');

            }
          });
        },
        error: function() {
          alert('Error at Post to index select');
        }
      });
    }


});
