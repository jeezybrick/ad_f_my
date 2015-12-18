angular
    .module('myApp')
    .controller('AdvertisersController', AdvertisersController);

function AdvertisersController(Sponsor, $log) {
    var vm = this;
    vm.addSponsors = addSponsors;
    vm.clear = clear;
    vm.sponsors_type = {};
    vm.publisher_default = {};

    vm.sponsors_type = Sponsor.query(function (response) {



    }, function () {

    });

    function addSponsors() {

    }

    function clear() {

    }

}