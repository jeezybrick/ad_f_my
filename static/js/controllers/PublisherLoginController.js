angular
    .module('myApp')
    .controller('PublisherLoginController', PublisherLoginController);

function PublisherLoginController() {
    var vm = this;
    vm.loginProcess = false;
    vm.sendLoginData = sendLoginData;


    function sendLoginData() {
        vm.loginProcess = true;
    }

}