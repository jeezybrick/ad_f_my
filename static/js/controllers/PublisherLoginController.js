angular
    .module('myApp')
    .controller('PublisherLoginController', PublisherLoginController);

function PublisherLoginController() {
    var vm = this;
    vm.loginProcess = false;
    vm.not_auth_completed = false;
    vm.sendLoginData = sendLoginData;


    function sendLoginData() {
        vm.loginProcess = true;
    }

}