angular
    .module('myApp')
    .controller('PublisherController', PublisherController);

function PublisherController(Sponsor, Publisher, Website, $log, $location, $state, $stateParams) {
    var vm = this;
    vm.addSponsors = addSponsors;
    vm.clear = clear;

    vm.isSponsorsLoad = false;
    vm.sponsors_type = {};
    vm.publisher_default = {};
    vm.getCodeScriptText = '';

    vm.sponsors_type = Sponsor.query(function (response) {

        vm.isSponsorsLoad = true;

    }, function () {

    });

    vm.publisher = Publisher.query(function (response) {

        vm.website = Website.query(function (response) {

            vm.getCodeScriptText = '<div id="ad-adfits" pub_id="' + vm.publisher.id + '" web_id="' + vm.website.results[0].id + '">' +
                '<script src="http://adfits.com/static/js/tag/ads.js"></script>' +
                '</div>';
        }, function (error) {

            vm.websitesLoadError = error.data;

        });


    }, function () {

    });

    function addSponsors() {
        // $location.path('/')
        $state.go('publisher.dashboard')
    }

    function clear() {

        $state.transitionTo($state.current, $stateParams, {
            reload: true, inherit: false, notify: false
        });

    }

}
