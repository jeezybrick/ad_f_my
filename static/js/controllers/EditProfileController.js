angular
    .module('myApp')
    .controller('EditProfileController', EditProfileController);

function EditProfileController($log) {
    var vm = this;
    vm.sendMessage = sendMessage;
    vm.test = 'Hello!';

    function sendMessage() {

        $log.info('function work');

    }

}