angular
    .module('myApp')
    .controller('EditProfileController', EditProfileController);

function EditProfileController(Publisher, $log) {
    var vm = this;
    vm.updateProfile = updateProfile;
    vm.clear = clear;
    vm.publisher = {};
    vm.publisher_default = {};

    vm.publisher = Publisher.query(function (response) {
        angular.copy(vm.publisher, vm.publisher_default);

    }, function () {

    });

    function updateProfile() {
        vm.publisher.$update(function (response) {

        }, function (error) {

        });
    }

    function clear() {
        angular.copy(vm.publisher_default, vm.publisher);
    }

}