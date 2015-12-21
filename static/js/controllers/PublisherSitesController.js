angular
    .module('myApp')
    .controller('PublisherSitesController', PublisherSitesController);

function PublisherSitesController(Website, $log, $state) {
    var vm = this;
    vm.addWebsite = addWebsite;
    vm.clear = clear;
    vm.publisher = {};

    vm.website = new Website();


    function addWebsite() {

        if (angular.isDefined(vm.website.industry.originalObject)) {
                vm.website.industry = [vm.website.industry.originalObject];
        }

        vm.website.$save(function (response) {

            $state.go('publisher.getcode');

        }, function (error) {

        });
    }

    function clear() {

    }

}