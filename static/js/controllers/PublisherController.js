angular
    .module('myApp')
    .controller('PublisherController', PublisherController);

function PublisherController(Sponsor, $log, $location, $state, $stateParams) {
    var vm = this;
    vm.addSponsors = addSponsors;
    vm.clear = clear;

    vm.isSponsorsLoad = false;
    vm.sponsors_type = {};
    vm.publisher_default = {};
    vm.getCodeScriptText = '<div id="ad-adfits">' +
        '<script src="http://127.0.0.1:8000/static/js/tag/ads.js"></script>' +
        '</div>';

    vm.sponsors_type = Sponsor.query(function (response) {

        vm.isSponsorsLoad = true;

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