angular
    .module('myApp')
    .controller('EditProfileController', EditProfileController);

function EditProfileController(Publisher, $log, $http) {
    var vm = this;
    vm.updateProfile = updateProfile;
    vm.clear = clear;
    vm.changePassword = changePassword;

    vm.authUser = {};
    vm.publisher = {};
    vm.publisher_default = {};
    vm.editableName = false;
    vm.editablePhone = false;
    vm.changePasswordPage = '/rest-auth/password/change/';

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

    function changePassword() {

        $http.post(vm.changePasswordPage, vm.authUser).success(function (data) {


        });
    }

}