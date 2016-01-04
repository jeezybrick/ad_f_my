angular
    .module('myApp')
    .controller('AdvertisersController', AdvertisersController);

function AdvertisersController($scope, $state, $location, Sponsor, Publisher, $log, $http) {
    var vm = this;
    vm.addSponsors = addSponsors;
    vm.clear = clear;
    vm.toggle = toggle;
    vm.exists = exists;
    vm.toggleSelectAll = toggleSelectAll;

    vm.isSponsorsLoad = false;
    vm.sponsors_type = {};
    vm.publisher = {};
    vm.selected = [];
    vm.page = '/static/pages/widget.html';
    vm.addSponsorsProcess = false;
    vm.test = {};

    $scope.selected = [];
    $scope.selectedAll = [];

    var myEl = angular.element(document.querySelector('#ad-adfits'));

    $http.get(vm.page).success(function (data) {

        myEl.html(data);

    });


    vm.sponsors_type = Sponsor.query(function (response) {

        vm.isSponsorsLoad = true;

    }, function () {

    });


    function addSponsors() {
        vm.addSponsorsProcess = true;

        vm.publisher = new Publisher();
        vm.publisher.sponsor = $scope.selected;

        vm.publisher.$update(function (response) {

            $state.go('publisher.addsites');

        }, function (error) {

        });

    }

    function clear() {

    }

    $scope.toggle = function (item, list) {
        var idx = list.indexOf(item);
        if (idx > -1) list.splice(idx, 1);
        else list.push(item);
    };
    $scope.exists = function (item, list) {
        return list.indexOf(item) > -1;
    };

    $scope.toggleAll = function (list, sponsor_type) {

        var test = $.grep(vm.sponsors_type, function (n, i) {
            return n.type === sponsor_type;
        });

        for (var i = 0; i < test[0].sponsor_set.length; i++) {

            var idx = list.indexOf(test[0].sponsor_set[i]);
            if (idx > -1) list.splice(idx, 1);
            else list.push(test[0].sponsor_set[i]);
        }
    };

    function toggle(item, list) {
        var idx = list.indexOf(item);
        if (idx > -1) list.splice(idx, 1);
        else list.push(item);
    }

    function toggleSelectAll(sponsor, list) {
        var idx = list.indexOf(sponsor);
        if (idx > -1) {
            list.splice(idx, 1);
        }else{
            list.push(sponsor);
        }
    }


    function exists(item, list) {
        return list.indexOf(item) > -1;
    }

}