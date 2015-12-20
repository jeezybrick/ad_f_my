angular
    .module('myApp')
    .controller('PublisherController', PublisherController);

function PublisherController(Sponsor, $log, $location,$state) {
     var vm = this;
    vm.addSponsors = addSponsors;
    vm.isSponsorsLoad = false;
    vm.clear = clear;
    vm.sponsors_type = {};
    vm.publisher_default = {};

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