angular
    .module('myApp')
    .controller('EditProfileController', EditProfileController);

function EditProfileController(Publisher, $log, $http, $mdToast, Flash) {
    var vm = this;
    vm.updateProfile = updateProfile;
    vm.clear = clear;
    vm.changePassword = changePassword;
    vm.sanitizePosition = sanitizePosition;

    vm.authUser = {};
    vm.publisher = {};
    vm.publisher_default = {};
    vm.editableName = false;
    vm.editablePhone = false;
    vm.publisherLoadError = '';
    vm.changePasswordPage = '/rest-auth/password/change/';
    vm.successChangePasswordMessage = 'Password changed!';
    vm.successEditProfileMessage = 'Profile saved';
    vm.errorEditProfileMessage = '';
    vm.errorChangePasswordMessage = 'Password mismatch';

    vm.publisher = Publisher.query(function (response) {
        angular.copy(vm.publisher, vm.publisher_default);

    }, function (error) {
        vm.publisherLoadError = error;
    });

    function updateProfile() {
        vm.publisher.$update(function (response) {
            Flash.create('success', vm.successEditProfileMessage, 'flash-message');
        }, function (error) {
            Flash.create('danger', vm.errorEditProfileMessage, 'flash-message');
        });
    }

    function clear() {
        angular.copy(vm.publisher_default, vm.publisher);
    }

    function changePassword() {

        $http.post(vm.changePasswordPage, vm.authUser).success(function (data) {
            Flash.create('success', vm.successChangePasswordMessage, 'flash-message');

        }).error(function (error) {

             // error toast
             Flash.create('danger', vm.errorChangePasswordMessage, 'flash-message');
            /*$mdToast.show(
                $mdToast.simple()
                    .content('jjjjjjjjjjjjjjjj')
                    .position(vm.getToastPosition())
                    .hideDelay(300000)
                    .theme('error-toast')
            );
*/
        });
    }

    // toast position
    var last = {
        bottom: false,
        top: true,
        left: true,
        right: false
    };
    vm.toastPosition = angular.extend({}, last);
    vm.getToastPosition = function () {
        sanitizePosition();
        return Object.keys(vm.toastPosition)
            .filter(function (pos) {
                return vm.toastPosition[pos];
            })
            .join(' ');
    };
    function sanitizePosition() {
        var current = vm.toastPosition;
        if (current.bottom && last.top) current.top = false;
        if (current.top && last.bottom) current.bottom = false;
        if (current.right && last.left) current.left = false;
        if (current.left && last.right) current.right = false;
        last = angular.extend({}, current);
    }



}