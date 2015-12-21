angular
    .module('myApp')
    .controller('PublisherSitesController', PublisherSitesController);

function PublisherSitesController(Website, $log, $state) {
    var vm = this;
    vm.addWebsite = addWebsite;
    vm.clear = clear;
    vm.publisher = {};
    vm.website = {};

    vm.website = Website.query(function (response) {


    }, function () {

    });


    function addWebsite() {

    }

    function clear() {

    }

}