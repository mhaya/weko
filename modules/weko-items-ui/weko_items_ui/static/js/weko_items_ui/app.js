require([
  'jquery',
  'bootstrap'
],function () {
  $('#weko_id_hidden').hide();
  $("#item-type-lists").change(function (ev) {
    window.location.href = '/items/' + $(this).val();
  });
  $("#btnModalClose").click(function () {
    $('#myModal').modal('toggle');
    $("div.modal-backdrop").remove();
  });

//TODO
  $("#meta-sach-close").click(function () {
    $('#meta-sach').modal('toggle');
    $("div.modal-backdrop").remove();
  });

});

(function (angular) {
  // Bootstrap it!
  angular.element(document).ready(function() {
    angular.module('wekoRecords.controllers', []);
    function WekoRecordsCtrl($scope, $rootScope, $modal, InvenioRecordsAPI){
//      $scope.items = [ 'item1', 'item2', 'item3' ];
      $scope.filemeta_key = '';
      $scope.filemeta_form_idx = -1;

      $scope.searchFilemetaKey = function() {
          if($scope.filemeta_key.length > 0) {
            return $scope.filemeta_key;
          }
          Object.entries($rootScope.recordsVM.invenioRecordsSchema.properties).forEach(
            ([key, value]) => {
              if(value.type == 'array') {
                if(value.items.properties.hasOwnProperty('filename')) {
                  $scope.filemeta_key = key;
                }
              }
            }
          );
      }
      $scope.findFilemetaFormIdx = function() {
          if($scope.filemeta_form_idx >= 0) {
            return $scope.filemeta_form_idx;
          }
          $rootScope.recordsVM.invenioRecordsForm.forEach(
            (element, index) => {
              if(element.hasOwnProperty('key')
                  && element.key == $scope.filemeta_key) {
                $scope.filemeta_form_idx = index;
              }
            }
          );
      }
      $scope.initFilenameList = function() {
        $scope.searchFilemetaKey();
        $scope.findFilemetaFormIdx();
        filemeta_schema = $rootScope.recordsVM.invenioRecordsSchema.properties[$scope.filemeta_key];
        filemeta_schema.items.properties['filename']['enum'] = [];
        filemeta_form = $rootScope.recordsVM.invenioRecordsForm[$scope.filemeta_form_idx];
        filemeta_filename_form = filemeta_form.items[0];
        filemeta_filename_form['titleMap'] = [];
        $rootScope.filesVM.files.forEach(file => {
          if(file.completed) {
            filemeta_schema.items.properties['filename']['enum'].push(file.key);
            filemeta_filename_form['titleMap'].push({name: file.key, value: file.key});
          }
        });
        $rootScope.$broadcast('schemaFormRedraw');
      }

      $rootScope.$on('invenio.records.loading.stop', function(ev){
        $scope.initFilenameList();
        hide_endpoints = $('#hide_endpoints').text()
        if(hide_endpoints.length > 2) {
          endpoints = JSON.parse($('#hide_endpoints').text());
          if(endpoints.hasOwnProperty('bucket')) {
            $rootScope.$broadcast(
              'invenio.records.endpoints.updated', endpoints
            );
          }
        }
      });
      $rootScope.$on('invenio.uploader.upload.completed', function(ev){
        $scope.initFilenameList();
      });
      $scope.$on('invenio.uploader.file.deleted', function(ev, f){
        $scope.initFilenameList();
      });

      // TODO
      $scope.getItemMetadata = function(model_id,arrayFlg,form) {
        $('#meta-sach').modal('show');


      }

      $scope.setItemMetadata = function() {
//        alert('setItemMetadata!!!');

        $.ajax({
          method: 'GET',
          url: '/items/isbn',
          async: false,
          success: function(data, status){

            if(confirm('Set to form ?')){

//              alert(JSON.stringify($rootScope.recordsVM.invenioRecordsModel));

              $rootScope.recordsVM.invenioRecordsModel['title_ja'] = 'アマゾン'
              $rootScope.recordsVM.invenioRecordsModel['title_en'] = 'Amazon'

              $rootScope.recordsVM.invenioRecordsModel['lang'] = 'en'
              $rootScope.recordsVM.invenioRecordsModel['pubdate'] = '2018-01-01'

              $rootScope.recordsVM.invenioRecordsModel['item_1549592380617'][0]['subitem_1522300295150'] = 'ja';
              $rootScope.recordsVM.invenioRecordsModel['item_1549592380617'][0]['subitem_1522300316516'] = 'University of Tokyo';


            }

          },
          error: function(status, error){
            console.log(error);
          }
        });


      }

      $scope.searchAuthor = function(model_id,arrayFlg,form) {
        // add by ryuu. start 20180410
        $("#btn_id").text(model_id);
        $("#array_flg").text(arrayFlg);
        $("#array_index").text(form.key[1]);
        // add by ryuu. end 20180410
        $('#myModal').modal('show');
      }
      // add by ryuu. start 20180410
      $scope.setAuthorInfo = function() {



         var authorInfo = $('#author_info').text();
         var arrayFlg = $('#array_flg').text();
         var modelId = $('#btn_id').text();
         var array_index = $('#array_index').text();
         var authorInfoObj = JSON.parse(authorInfo);
         var updateIndex = 0;
         if(arrayFlg == 'true'){
//            $rootScope.recordsVM.invenioRecordsModel[modelId].push(authorInfoObj[0]);
//              $rootScope.recordsVM.invenioRecordsModel[modelId][array_index]= authorInfoObj[0];


              // 2018/05/28 start
　　　　　　　var familyName ="";
              var givenName = "";
              if(authorInfoObj[0].hasOwnProperty('affiliation')){
                 $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].affiliation = authorInfoObj[0].affiliation;
               }
               if(authorInfoObj[0].hasOwnProperty('creatorAlternatives')){
                 $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].creatorAlternatives = authorInfoObj[0].creatorAlternatives;
               }

               if(authorInfoObj[0].hasOwnProperty('creatorNames')){
                 $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].creatorNames = authorInfoObj[0].creatorNames;
               }

               if(authorInfoObj[0].hasOwnProperty('familyNames')){
                 $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].familyNames = authorInfoObj[0].familyNames;
                 if($rootScope.recordsVM.invenioRecordsModel[modelId][array_index].familyNames.length == 1){
                    familyName = authorInfoObj[0].familyNames[0].familyName;
                 }
               }else{
                 $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].familyNames = {"familyName": "","lang": ""};
               }
               if(authorInfoObj[0].hasOwnProperty('givenNames')){
                 $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].givenNames = authorInfoObj[0].givenNames;
                 if($rootScope.recordsVM.invenioRecordsModel[modelId][array_index].givenNames.length == 1){
                    givenName = authorInfoObj[0].givenNames[0].givenName;
                 }
               }else{
                 $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].givenNames = {"givenName": "","lang": ""};
               }

               if(authorInfoObj[0].hasOwnProperty('familyNames')&&authorInfoObj[0].hasOwnProperty('givenNames')){
                 if(!authorInfoObj[0].hasOwnProperty('creatorNames')){
                   $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].creatorNames = [];
                 }
                 for(var i=0;i<authorInfoObj[0].familyNames.length;i++){
                   var subCreatorName = {"creatorName":"","lang":""};
                   subCreatorName.creatorName = authorInfoObj[0].familyNames[i].familyName + "　"+authorInfoObj[0].givenNames[i].givenName;
                   subCreatorName.lang = authorInfoObj[0].familyNames[i].lang;
                   $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].creatorNames.push(subCreatorName);
                 }
               }

               if(authorInfoObj[0].hasOwnProperty('nameIdentifiers')){
                 $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].nameIdentifiers = authorInfoObj[0].nameIdentifiers;
               }

               var weko_id = $('#weko_id').text();
               $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].weko_id= weko_id;
               $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].weko_id_hidden= weko_id;
               $rootScope.recordsVM.invenioRecordsModel[modelId][array_index].authorLink=['check'];
//            2018/05/28 end
         }else{
             if(authorInfoObj[0].hasOwnProperty('affiliation')){
               $rootScope.recordsVM.invenioRecordsModel[modelId].affiliation = authorInfoObj[0].affiliation;
             }
             if(authorInfoObj[0].hasOwnProperty('creatorAlternatives')){
               $rootScope.recordsVM.invenioRecordsModel[modelId].creatorAlternatives = authorInfoObj[0].creatorAlternatives;
             }
             if(authorInfoObj[0].hasOwnProperty('creatorNames')){
               $rootScope.recordsVM.invenioRecordsModel[modelId].creatorNames = authorInfoObj[0].creatorNames;
             }else{
               $rootScope.recordsVM.invenioRecordsModel[modelId].creatorNames = {};
             }
             if(authorInfoObj[0].hasOwnProperty('familyNames')){
               $rootScope.recordsVM.invenioRecordsModel[modelId].familyNames = authorInfoObj[0].familyNames;
             }else{
               $rootScope.recordsVM.invenioRecordsModel[modelId].familyNames = {};
             }
             if(authorInfoObj[0].hasOwnProperty('givenNames')){
               $rootScope.recordsVM.invenioRecordsModel[modelId].givenNames = authorInfoObj[0].givenNames;
             }else{
               $rootScope.recordsVM.invenioRecordsModel[modelId].givenNames = {};
             }
             if(authorInfoObj[0].hasOwnProperty('nameIdentifiers')){
               $rootScope.recordsVM.invenioRecordsModel[modelId].nameIdentifiers = authorInfoObj[0].nameIdentifiers;
             }

             var weko_id = $('#weko_id').text();
             $rootScope.recordsVM.invenioRecordsModel[modelId].weko_id= weko_id;
             $rootScope.recordsVM.invenioRecordsModel[modelId].weko_id_hidden= weko_id;
             $rootScope.recordsVM.invenioRecordsModel[modelId].authorLink=['check'];

         }
         //画面にデータを設定する
         $("#btn_id").text('');
         $("#author_info").text('');
         $("#array_flg").text('');
      }
      // add by ryuu. end 20180410
      $scope.updated=function(model_id,modelValue,form,arrayFlg){
//        2018/05/28 start

         if(arrayFlg){
            var array_index = form.key[1];
            if(modelValue == true){
              $rootScope.recordsVM.invenioRecordsModel[model_id][array_index].weko_id= $rootScope.recordsVM.invenioRecordsModel[model_id][array_index].weko_id_hidden;
            }else{
  　　　　　　delete $rootScope.recordsVM.invenioRecordsModel[model_id][array_index].weko_id;
            }
          }else{
            if(modelValue == true){
              $rootScope.recordsVM.invenioRecordsModel[model_id].weko_id= $rootScope.recordsVM.invenioRecordsModel[model_id].weko_id_hidden;
            }else{
  　　　　　　delete $rootScope.recordsVM.invenioRecordsModel[model_id].weko_id;
            }
          }
//        2018/05/28 end
      }
//    authorLink condition
      $scope.linkCondition=function(val){
        var linkStus = val.hasOwnProperty('authorLink');
        if(linkStus){
          return true;
        }else{
          return false;
        }
      }
//    authorId condition
      $scope.idCondition=function(val){
        var c = val.hasOwnProperty('authorLink');
        if(!c){
          return false;
        }else{
          return true;
        }
      }
      $scope.updateDataJson = function(){
        var str = JSON.stringify($rootScope.recordsVM.invenioRecordsModel);
        var indexOfLink = str.indexOf("authorLink");
        if(indexOfLink != -1){
          str = str.split(',"authorLink":[]').join('');
        }
        $rootScope.recordsVM.invenioRecordsModel = JSON.parse(str);
      }
      $scope.saveDataJson = function(item_save_uri){
        var metainfo = {'metainfo': $rootScope.recordsVM.invenioRecordsModel};
        if(!angular.isUndefined($rootScope.filesVM)) {
          metainfo = angular.merge(
            {},
            metainfo,
            {
              'files': $rootScope.filesVM.files,
              'endpoints': $rootScope.filesVM.invenioFilesEndpoints
            }
          );
        }
        var request = {
          url: item_save_uri,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          data: JSON.stringify(metainfo)
        };
        InvenioRecordsAPI.request(request).then(
          function success(response){
            alert(response.data.msg);
          },
          function error(response){
            alert(response);
          }
        );
      }
    }
    // Inject depedencies
    WekoRecordsCtrl.$inject = [
      '$scope',
      '$rootScope',
      '$modal',
      'InvenioRecordsAPI',
    ];
    angular.module('wekoRecords.controllers')
      .controller('WekoRecordsCtrl', WekoRecordsCtrl);

    var ModalInstanceCtrl = function($scope, $modalInstance, items) {
      $scope.items = items;
      $scope.searchKey = '';
      $scope.selected = {
        item : $scope.items[0]
      };
      $scope.ok = function() {
        $modalInstance.close($scope.selected);
      };
      $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
      };
      $scope.search = function() {
        $scope.items.push($scope.searchKey);
      }
    };

    angular.module('wekoRecords', [
      'invenioRecords',
      'wekoRecords.controllers',
    ]);

    angular.bootstrap(
      document.getElementById('weko-records'), [
        'wekoRecords', 'invenioRecords', 'schemaForm', 'mgcrea.ngStrap',
        'mgcrea.ngStrap.modal', 'pascalprecht.translate', 'ui.sortable',
        'ui.select', 'mgcrea.ngStrap.select', 'mgcrea.ngStrap.datepicker',
        'mgcrea.ngStrap.helpers.dateParser', 'mgcrea.ngStrap.tooltip',
        'invenioFiles'
      ]
    );
  });
})(angular);
