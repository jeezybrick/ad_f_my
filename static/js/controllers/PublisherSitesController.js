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
        vm.website.$save(function (response) {
            vm.website.industry = vm.website.industry.originalObject;

            $state.go('publisher.getcode');

        }, function (error) {

        });
    }

    function clear() {

    }

}