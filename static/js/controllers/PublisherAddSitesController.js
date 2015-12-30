angular
    .module('myApp')
    .controller('PublisherAddSitesController', PublisherAddSitesController);

function PublisherAddSitesController(Website, $log, $state, Upload) {
    var vm = this;
    vm.addWebsite = addWebsite;
    vm.clear = clear;

    vm.publisher = {};
    vm.addWebsiteProcess = false;
    vm.addWebsiteProcessError = {};
    vm.fileReader = new FileReader();

    vm.website = new Website();


    function addWebsite(next_page) {
         vm.addWebsiteProcess = true;

        Upload.upload({
            url: '/api/publisher/website/',
            data: vm.website
        }).then(function (resp) {
            $state.go(next_page);
        }, function (err) {
            vm.addWebsiteProcessError = err;
            console.log('Error status: '+ err);
        }, function (evt) {
        });

    }

    function clear() {

    }

}