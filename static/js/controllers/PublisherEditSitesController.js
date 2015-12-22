angular
    .module('myApp')
    .controller('PublisherEditSitesController', PublisherEditSitesController);

function PublisherEditSitesController(Website, $log, $state, $stateParams) {
     var vm = this;
    vm.editWebsite = editWebsite;
    vm.clear = clear;
    vm.publisher = {};
    vm.website = {};

    /**
     * Get item detail
     */
    vm.website = Website.get({id: $stateParams.id}, function (response) {


    }, function (error) {

    });



    function editWebsite() {

        vm.website.$update(function (response) {

        }, function (error) {

        });

    }

    function clear() {

    }

}