angular
    .module('myApp')
    .controller('PublisherSitesController', PublisherSitesController);

function PublisherSitesController(Website, $log, $state, $http) {
    var vm = this;
    vm.addWebsite = addWebsite;
    vm.clear = clear;
    vm.pagination = pagination;
    vm.isWebsitesNotPrevious = isWebsitesNotPrevious;
    vm.isWebsitesNotNext = isWebsitesNotNext;
    vm.filterByDefaultCategory = filterByDefaultCategory;

    vm.publisher = {};
    vm.website = {};
    vm.websitesLoad = false;
    vm.websitesLoadError = '';

    vm.website = Website.query(function (response) {

        vm.websitesLoad = true;
    }, function (error) {

        vm.websitesLoadError = error.data;

    });

    function pagination(page) {

        if (page !== null) {

            vm.websitesLoad = false;
            $http.get(page, {cache: true}).success(function (data) {
                vm.websitesLoad = true;
                vm.website = data;

            });
        }

    }


    function isWebsitesNotPrevious(websites) {
        return !websites.previous;
    }

    function isWebsitesNotNext(websites) {
        return !websites.next;
    }

    function filterByDefaultCategory(category) {

        return category
    }


    function addWebsite() {

    }

    function clear() {

    }

}