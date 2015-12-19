angular
    .module('myApp')
    .controller('PublisherController', PublisherController);

function PublisherController(Sponsor, $log, $location) {
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
        $location.path('/')
    }

    function clear() {

    }


}