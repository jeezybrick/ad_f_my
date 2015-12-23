angular
    .module('myApp')
    .controller('PublisherEditSitesController', PublisherEditSitesController);

function PublisherEditSitesController(Website, $log, $state, $stateParams, Upload) {
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

        Upload.upload({
            url: '/api/publisher/website/'+ $stateParams.id + '/',
            data: vm.website
        }).then(function (resp) {
            $state.go('publisher.sites');
        }, function (err) {
            console.log('Error status: '+ err);
        }, function (evt) {
        });


    }

    function clear() {

    }

}