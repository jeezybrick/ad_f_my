angular
    .module('myApp')
    .controller('PublisherEditSitesController', PublisherEditSitesController);

function PublisherEditSitesController(Website, $log, $state, $stateParams, Upload) {
     var vm = this;
    vm.editWebsite = editWebsite;
    vm.clear = clear;
    vm.publisher = {};
    vm.website = {};
    vm.test = {};

    /**
     * Get item detail
     */
    vm.website = Website.get({id: $stateParams.id}, function (response) {
            vm.test = response.website_logo;

    }, function (error) {

    });



    function editWebsite() {

        Upload.upload({
            url: '/api/publisher/website/'+ $stateParams.id + '/',
            data: {
                website_name:vm.website.website_name,
                website_domain:vm.website.website_domain,
                website_logo:vm.website.website_logo,
            },
            method:'PUT'
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