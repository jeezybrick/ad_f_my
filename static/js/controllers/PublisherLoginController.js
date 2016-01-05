angular
    .module('myApp')
    .controller('PublisherLoginController', PublisherLoginController);

function PublisherLoginController(Publisher, $state) {
    var vm = this;
    vm.loginProcess = false;
    vm.not_auth_completed = false;
    vm.sendLoginData = sendLoginData;

    vm.publisher = Publisher.query(function (response) {

        if(angular.equals(response.is_completed_auth, 'get_code')) {
            window.location.href = '/publisher/#/sites/get-code/';
          // $state.go('publisher.getcode');
        }else if(angular.equals(response.is_completed_auth, 'add_website')){
            window.location.href = '/publisher/#/sites/add-sites/';
           // $state.go('publisher.addsites');
        }else if(angular.equals(response.is_completed_auth, 'advertisers')){
            window.location.href = '/publisher/#/advertisers/';
            //$state.go('publisher.advertisers');
        }else if(angular.equals(response.is_completed_auth, 'completed')){
            window.location.href = '/publisher/#/dashboard/';
           // $state.go('publisher.dashboard');
        }


    }, function (error) {
        vm.publisherLoadError = error.data[0];
    });


    function sendLoginData() {
        vm.loginProcess = true;
    }

}