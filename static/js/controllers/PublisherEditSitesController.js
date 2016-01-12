angular
    .module('myApp')
    .controller('PublisherEditSitesController', PublisherEditSitesController);

function PublisherEditSitesController(Website, Publisher, $log, $state, $stateParams, Upload, $mdDialog, $mdConstant, $http) {
    var vm = this;
    vm.editWebsite = editWebsite;
    vm.clear = clear;
    vm.showJsTag = showJsTag;
    vm.transformChip = transformChip;
    vm.querySearch = querySearch;

    vm.publisher = {};
    vm.website = {};
    vm.test = {};
    vm.jsTag = '';
    vm.editWebsiteProcess = false;

    vm.autocompleteDemoRequireMatch = false;
    vm.selectedCategoryParent = null;
    vm.selectedCategorySub = null;
    vm.searchTextParent = null;
    vm.searchTextSub = null;
    vm.queryResult = {};
    vm.keys = [$mdConstant.KEY_CODE.ENTER, $mdConstant.KEY_CODE.COMMA];

    vm.category_default = [];
    vm.category_sub = [];
    //vm.type_of_category = ['default', 'sub'];

    /**
     * Get website detail
     */
    vm.website = Website.get({id: $stateParams.id}, function (response) {
        vm.publisher = Publisher.query(function (response) {

            vm.jsTag = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.0/jquery.min.js"></script>' +
                '<div id="ad-adfits" pub_id="' + vm.publisher.id + '" web_id="' + vm.website.id + '">' +
                '<script src="http://adfits.com/static/js/tag/ads.js"></script>' +
                '</div>';

            for(var i=0;i<vm.website.industry.length;i++){
                if(angular.equals(vm.website.industry[i].type, 'default')){
                    vm.category_default.push(vm.website.industry[i]);
                }else{
                    vm.category_sub.push(vm.website.industry[i]);
                }
            }

        }, function () {

        });
        vm.test = response.website_logo;

    }, function (error) {

    });

    function showJsTag(ev) {

        $mdDialog.show(
            $mdDialog.alert()
                .parent(angular.element(document.querySelector('#popupContainer')))
                .clickOutsideToClose(true)
                .title('JS tag')
                .textContent(vm.jsTag)
                .ariaLabel('Alert Dialog Demo')
                .ok('Got it!')
                .targetEvent(ev)
        );
    }


    function editWebsite() {
        vm.editWebsiteProcess = true;

        /*vm.website.$update(function (response) {


        }, function (error) {

        });*/

        /*if (vm.website.website_logo === null) {
            var sendData = {
                website_name: vm.website.website_name,
                website_domain: vm.website.website_domain,
            };

        } else {

            var sendData = {
                website_name: vm.website.website_name,
                website_domain: vm.website.website_domain,
                website_logo: vm.website.website_logo,
            };

        }*/

        Upload.upload({
            url: '/api/publisher/website/' + $stateParams.id + '/',
            data: {
                website_name:vm.website.website_name,
                website_domain:vm.website.website_domain,
                category_parent: vm.category_default,
                category_sub: vm.category_sub,
                twitter_name:vm.website.twitter_name,
                facebook_page:vm.website.facebook_page,
            },
            file:vm.website_logo,
            method: 'PUT'
        }).then(function (resp) {
            vm.editWebsiteProcess = false;
            $state.go('publisher.sites');
        }, function (err) {
            vm.editWebsiteProcess = false;
        }, function (evt) {
        });


    }

    function clear() {

    }

    function transformChip(chip, type) {
        // If it is an object, it's already a known chip
        if (angular.isObject(chip)) {
            return chip;
        }
        // Otherwise, create a new one
        return {industry_type: chip, type_public: 'new', type: type}
    }

    function querySearch(query, type) {

        $http.get('/api/category?' + type + '=' + query).success(function (data) {
            vm.queryResult = data;

        }).error(function (error) {

        });

        return vm.queryResult;

    }

}