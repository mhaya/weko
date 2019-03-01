  require([
    "jquery",
    "bootstrap",
    "node_modules/bootstrap-datepicker/dist/js/bootstrap-datepicker"
    ], function() {
    // loading all the jQuery modules for the not require.js ready scripts
    // everywhere.
    $(function(){
      $('#myModal').modal({
        show: false
      })
      page_global = {
        queryObj: null
      }
      page_global.queryObj = query_to_hash();
      $('#page_count').val(page_global.queryObj['size'])
      $('#page_count').on('change', function(){
        if(page_global.queryObj['size'] != $('#page_count').val()) {
          page_global.queryObj['size'] = $('#page_count').val();
          queryStr = hash_to_query(page_global.queryObj);
          window.location.href = window.location.pathname + '?' + queryStr;
        }
      });
      function query_to_hash(queryString) {
        var query = queryString || location.search.replace(/\?/, "");
        return query.split("&").reduce(function(obj, item, i) {
          if(item) {
            item = item.split('=');
            obj[item[0]] = item[1];
            return obj;
          }
        }, {});
      };
      function hash_to_query(queryObj) {
        var str = '';
        Object.keys(queryObj).forEach(function(key){
          if(str.length > 0) {
            str = str + '&' + key + '=' + queryObj[key];
          } else {
            str = key + '=' + queryObj[key];
          }
        });
        return str;
      }
    });
});

//add controller to invenioSearch
// add by ryuu. at 20181129 start

function searchResCtrl($scope, $rootScope, $http, $location) {
    var commInfo=$("#community").val();
     if(commInfo != ""){
        $rootScope.commInfo="?community="+commInfo;
        $rootScope.commInfoIndex="&community="+commInfo;
     }else{
        $rootScope.commInfo="";
        $rootScope.commInfoIndex="";
     }
//   button setting
     $rootScope.disable_flg = true;
     $rootScope.display_flg = true;
     $rootScope.index_id_q = $location.search().q;


     $scope.itemManagementTabDisplay= function(){
        $rootScope.disable_flg = true;
        $rootScope.display_flg = true;
     }

     $scope.itemManagementEdit= function(){
        $rootScope.disable_flg = false;
        $rootScope.display_flg = false;
     }

     $scope.itemManagementSave= function(){
        var data = $scope.vm.invenioSearchResults.hits.hits
        var custom_sort_list =[]
        for(var x of data){
           var sub = {"id":"", "custom_sort":""}
           sub.id= x.id;
           sub.custom_sort=x.metadata.custom_sort;
           custom_sort_list.push(sub);
        }
        var post_data ={"q_id":$rootScope.index_id_q, "sort":custom_sort_list, "es_data":data}

　　   // request api
        $http({
            method: 'POST',
            url: '/item_management/save',
            data: post_data,
          headers: {'Content-Type': 'application/json'},
        }).then(function successCallback(response) {
          window.location.href = '/search?search_type=2&q='+$rootScope.index_id_q + "&management=item&sort=custom_sort";
        }, function errorCallback(response) {
          window.location.href = '/search?search_type=2&q='+$rootScope.index_id_q+ "&management=item&sort=custom_sort";
        });
     }

     $scope.itemManagementCancel= function(){
        $rootScope.disable_flg = true;
        $rootScope.display_flg = true;
        $("#tab_display").addClass("active")
     }

    $scope.showChangeLog = function(record) {
      // call api for itself to catch field deposit
      const id = record['id'];
      $http({
        method: 'GET',
        url: `/api/records/${id}`,
      }).then(function successCallback(response) {
        // Success
        const deposit = response['data']['metadata']['_buckets']['deposit'];
        // Call service to catch version by deposit with api /api/files/
        $http({
          method: 'GET',
          url: `/api/files/${deposit}`,
        }).then(function successCallback(response) {
          $('#bodyModal').append(createRow(response['data']));
          $('#basicExampleModal').modal({
            show: true
          });
          $('#basicExampleModal').on('hidden.bs.modal', function (e) {
            // Event will be trigger when modal absolute hidded
            $('#bodyModal').children().remove();
          });
        }, function errorCallback(response) {
          console.log('Error when trigger api /api/files');
        });
      }, function errorCallback(response) {
        // Error
        console.log('Error when trigger api /api/records');
      });
    }

    function createRow(response) {
      let results = '';
      const contents = response.contents;
      for (let index = 0; index < contents.length; index++) {
        const ele = contents[index];

        // const isPublic = ele.pubPri === 'Public' ? 1 : 0;
        const nameRadio = `radio${index}`;
        let radio = `
          <div class="radio">
            <div class="row">
              <div class="col-md-6">
                <label><input type="radio" name="${nameRadio}">Public</label>
              </div>
              <div class="col-md-6">
                <label><input type="radio" name="${nameRadio}">Private</label>
              </div>
            </div>
          </div>
        `;
        // if (!isPublic) {
        //   radio = `
        //     <div class="radio">
        //       <div class="row">
        //         <div class="col-md-6">
        //             <label><input type="radio" name="${nameRadio}">Public</label>
        //         </div>
        //         <div class="col-md-6">
        //           <label><input type="radio" name="${nameRadio}" checked>Private</label>
        //         </div>
        //       </div>
        //     </div>
        //   `;
        // }

        let version = ele.version_id;
        if (index === 0) {
          version = 'Current';
        }

        results += `
          <tr>
            <td>
              <div class="row">
                <div class="col-md-12 margin_top_10">
                  <p>${version}</p>
                </div>
              </div>
            </td>
            <td>
              <div class="row">
                <div class="col-md-12 margin_top_10">
                  <p>${formatDate(new Date(ele.updated))}</p>
                </div>
              </div>
            </td>
            <td>
              <div class="row">
                <div class="col-md-12 margin_top_10">
                  <a href="${ele.links.self}">${ele.key}</a>
                </div>
              </div>
            </td>
            <td>
              <div class="row">
                <div class="col-md-12 margin_top_10">
                  <p>${ele.size}</p>
                </div>
              </div>
            </td>
            <td>
              <div class="row">
                <div class="col-md-12 margin_top_10">
                  <p>${ele.size}</p>
                </div>
              </div>
            </td>
            <td>
              <div class="row">
                <div class="col-md-12 margin_top_10">
                  <p>${ele.key}</p>
                </div>
              </div>
            </td>
            <td>${radio}</td>
          </tr>
        `;

      }
      return results;
    }

    function formatDate(date) {
      let month = '' + (date.getMonth() + 1);
      let day = '' + date.getDate();
      let year = date.getFullYear();

      let hour = '' + date.getHours();
      let minute = '' + date.getMinutes();
      let second = '' + date.getSeconds();

      if (month.length < 2) month = '0' + month;
      if (day.length < 2) day = '0' + day;
      if (hour.length < 2) hour = '0' + hour;
      if (minute.length < 2) minute = '0' + minute;
      if (second.length < 2) second = '0' + second;

      return `${[year, month, day].join('-')} ${[hour, minute, second].join(':')}`;
    }

     $rootScope.confirmFunc=function(){
        if(!$rootScope.disable_flg){
          return confirm("Is the input contents discarded ?") ;
        }else{
          return true;
        }
     }
  }

angular.module('invenioSearch')
  .controller('searchResCtrl', searchResCtrl);

// add by ryuu. at 20181129 end
