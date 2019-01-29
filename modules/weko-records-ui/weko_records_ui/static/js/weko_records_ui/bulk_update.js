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
      if(selected == 'open_date'){
        $(accessDate).removeAttr("disabled");
      } else {
        $(accessDate).attr('disabled', 'disabled');
      }
    });

    $('select[name="field_sel"]').change(function() {

      var selected = $(this).val();
      var contents = $(this).parents('.field-row').find('.field-content');

      // Get selected fields
      var isDuplicate = false;
      var fields = [];
      $('.row.field-row').each(function(i, row) {


        var field = $($(row).find('select[name="field_sel"]')[0]);
        alert(field.prop('value'));
        if(field.prop('value') !== 'unselected') {
          if($.inArray(selected, fields) !== -1) {
//            alert(fields);
//            alert(field.prop('value'));
//            alert('Field already exists.');
            // Initialize
//            field.val('unselected');
            isDuplicate = true;
          } else {
            fields.push(selected);
          }
        }
      });
//      alert(isDuplicate);

      if(isDuplicate) {
//        alert('Field already exists.');
        $(this).val('unselected');
        contents.each( function(i, elem) {
          $(elem).attr('hidden', 'hidden')
        });
        fields = [];
        isDuplicate = false;
        return;
      }


//      alert(fields +' : ' + selected);
//      alert($.inArray(selected, fields));
//      if(selected !== 'unselected' && $.inArray(selected, fields) !== -1) {
//
//
//      }

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
        } else if(elemAttr.indexOf('licence-select') >= 0){
          if('2' === selected.toString()){
            $(elem).removeAttr("hidden");
          }else {
            $(elem).attr('hidden', 'hidden');
          }
        }
      });
    });

    $('select[name="licence_sel"]').change( function() {
      var selected = $(this).val();
      var des = $($(this).parent().find('.licence-des'));

      if(selected === 'license_free') {
        des.removeAttr("hidden");
      } else {
        des.attr('hidden', 'hidden');
      }
    });

    // Select All
    $('#select-all').on('click', function() {
      hasChecked = false;
      hasCanceled = false;

      checkboxes = $(this).parent().find('input[type="checkbox"]');
      checkboxes.each( function(i, elem) {
        if($(elem).prop('checked') === false){
          hasCanceled = true;
        }else {
          hasChecked = true;
        }
      });

      // Cancel all
      if(hasChecked && !hasCanceled) {
        checkboxes.each( function(i, elem) {
          $(elem).prop("checked", false);
        });

      // Check all
      }else {
        checkboxes.each( function(i, elem) {
          $(elem).prop("checked", true);
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
      var accessType = {};
      var licence= '';
      var licenceDes= '';
      $('.row.field-row').each(function(i, row) {
        var field = $($(row).find('select[name="field_sel"]')[0]);

        // Access Type
        if(field.prop('value') === '1') {
          var type = $($(row).find('input[name="access_type"]:checked')[0]).prop('value');
          accessType = {'accessrole': type};
          if (type === 'open_date') {
            accessType['accessdate'] = $($(row).find('input[name="access_date"]')[0]).prop('value');
          }

        // Licence
        }else if(field.prop('value') === '2') {
          licence = $($(row).find('select[name="licence_sel"]')[0]).prop('value');

          if(licence === 'license_free') {
            licenceDes = $($(row).find('textarea[name="licence_des"]')[0]).prop('value');
          }
        }
      });

      // Update
      getUrl = '/bulk_update/items_metadata?pids=' + pids;
      $.ajax({
        method: 'GET',
        url: getUrl,
        async: false,
        success: function(data, status){

          var redirect_url = "/api/deposits/redirect";
          var items_url = "/api/deposits/items";

          itemsMeta = data;
          Object.keys(itemsMeta).forEach(function(pid) {

            // Contents Meta
            if (Object.keys(itemsMeta[pid].contents).length !== 0) {

              Object.keys(itemsMeta[pid].contents).forEach( function(contentKey) {
                var contentsMeta = itemsMeta[pid].contents[contentKey];
                $.each( contentsMeta, function( key, value ) {
                  // Access Type
                  if (Object.keys(accessType).length !== 0) {
                    Object.keys(accessType).forEach( function(field) {
                    value[field] =  accessType[field];
                    });
                  }
                  // Licence
                  if(licence !== 'unselected') {
                    value['licensetype'] = licence;
                  }
                  // Licence Description
                  if(licenceDes !== '' && licence === 'license_free') {
                    value['licensefree'] = licenceDes;
                  }
                });
                itemsMeta[pid].meta[contentKey] = contentsMeta;

              });

            }

            meta = JSON.stringify(itemsMeta[pid].meta);
            index = JSON.stringify(itemsMeta[pid].index);

            index_url = redirect_url + "/" + pid;
            self_url = items_url + "/" + pid;

            // Update items
            updateItems(index_url,
                        self_url,
                        meta,
                        index);

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
