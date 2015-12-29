angular
    .module('myApp')
    .controller('PublisherController', PublisherController);

function PublisherController(Sponsor,Publisher, $log, $location, $state, $stateParams) {
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

        vm.getCodeScriptText = '<div id="ad-adfits-'+response.id+'">' +
        '<script src="http://adfits.com/static/js/tag/ads.js"></script>' +
        '</div>';

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
