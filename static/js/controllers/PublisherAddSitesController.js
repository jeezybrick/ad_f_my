angular
    .module('myApp')
    .controller('PublisherAddSitesController', PublisherAddSitesController);

function PublisherAddSitesController(Website, $log, $state, Upload, $http, $mdConstant) {
    var vm = this;
    vm.addWebsite = addWebsite;
    vm.clear = clear;
    vm.transformChip = transformChip;
    vm.querySearch = querySearch;

    vm.autocompleteDemoRequireMatch = false;
    vm.selectedCategoryParent = null;
    vm.selectedCategorySub = null;
    vm.searchTextParent = null;
    vm.searchTextSub = null;
    vm.queryResult = {};
    vm.keys = [$mdConstant.KEY_CODE.ENTER, $mdConstant.KEY_CODE.COMMA];

    vm.publisher = {};
    vm.addWebsiteProcess = false;
    vm.addWebsiteProcessError = {};
    vm.fileReader = new FileReader();

    vm.website = new Website();
    vm.category_default = [];
    vm.category_sub = [];

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

    function addWebsite(next_page) {
        vm.addWebsiteProcess = true;

        /*Upload.upload({
         url: '/api/publisher/website/',
         data: {
         website_name:vm.website.website_name,
         website_domain:vm.website.website_domain,
         category_parent: vm.category_default,
         category_sub: vm.category_sub,
         twitter_name:vm.website.twitter_name,
         facebook_page:vm.website.facebook_page,
         },
         file:vm.website_logo,
         }).then(function (resp) {
         vm.addWebsiteProcess = false;
         //$state.go('publisher.sites');
         }, function (err) {
         vm.addWebsiteProcess = false;
         }, function (evt) {
         });*/


        var test = {
            website_domain: vm.website.website_domain,
            website_name: vm.website.website_name,
            category_parent: vm.category_default,
            category_sub: vm.category_sub,
            twitter_name: vm.website.twitter_name,
            facebook_page: vm.website.facebook_page,
            avg_page_views: vm.website.avg_page_views,
        };

        $http.post('/api/publisher/website/', test).success(function (data) {

            if (angular.isDefined(vm.website.website_logo)) {
                Upload.upload({
                    url: '/api/publisher/website/' + data.id + '/',
                    data: {
                        website_domain: vm.website.website_domain,
                        website_name: vm.website.website_name,
                        website_logo: vm.website.website_logo
                    },
                    method: 'PUT'
                }).then(function (resp) {

                    // $state.go(next_page);

                }, function (err) {
                    vm.addWebsiteProcessError = err;
                    //  $state.go(next_page);

                }, function (evt) {
                });
            }

            $state.go(next_page);

        }).error(function (error) {

        });

    }

    function clear() {

    }

}