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

      getUrl = '/bulk_update/items_metadata?pids=' + pids;
      $.ajax({
        method: 'GET',
        url: getUrl,
        async: false,
        success: function(data, status){

          var redirect_url = "/api/deposits/redirect";
          var items_url = "/api/deposits/items";

          itemsMeta = data;
          Object.keys(itemsMeta).forEach(function(key) {
            meta = JSON.stringify(itemsMeta[key].meta);
            index = JSON.stringify(itemsMeta[key].index);

            index_url = redirect_url + "/" + key;
            self_url = items_url + "/" + key;

            // Update items
            updateItems(index_url,
                        self_url,
                        meta,
                        index);

          // Get bucket
//          $.ajax({
//            type: "POST",
//            url: index_url,
//            async: false,
//            cache: false,
//            data: {},
//            contentType: "application/json",
//            processData: false,
//            success: function(data) {
//              // Upload files
//              for (var fileName in files) {
//                file_url = data['links']['bucket'] + "/" + fileName;
//                $.ajax({
//                  type: "PUT",
//                  url: file_url,
//                  async: false,
//                  cache: false,
//                  data: files[fileName],
//                  contentType: "application/json",
//                  processData: false,
//                  success: function() {
//                    // Update items
//                    updateItems(index_url,
//                                self_url,
//                                JSON.stringify(itemData),
//                                JSON.stringify(indexData),
//                                error,
//                                errorFlg);
//                  },
//                  error: function() {
//                    errorFlg = true;
//                    error['eMsg'] = "Error in file uploading.";
//                  }
//                });
//              }
//            },
//            error: function() {
//              errorFlg = true;
//              error['eMsg'] = "Error in bucket requesting.";
//            }
//          });

          });

        },
        error: function(status, error){
          console.log(error);
        }
      });


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
            success: function(){},
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
