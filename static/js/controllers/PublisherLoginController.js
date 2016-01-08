
(function () {
    'use strict';
    angular
        .module('myApp')
        .controller('PublisherLoginController', PublisherLoginController);

    function PublisherLoginController(Publisher) {
        var self = this;
        self.loginProcess = false;
        self.not_auth_completed = false;
        self.sendLoginData = sendLoginData;

        self.publisher = Publisher.query(function (response) {

            if(angular.equals(response.is_completed_auth, 'get_code')) {
                window.location.href = '/publisher/#/sites/get-code/';
            }else if(angular.equals(response.is_completed_auth, 'add_website')){
                window.location.href = '/publisher/#/sites/add-sites/';
            }else if(angular.equals(response.is_completed_auth, 'advertisers')){
                window.location.href = '/publisher/#/advertisers/';
            }else if(angular.equals(response.is_completed_auth, 'completed')){
                window.location.href = '/publisher/#/dashboard/';
            }


        }, function (error) {
            self.publisherLoadError = error.data[0];
        });

        function sendLoginData() {
            self.loginProcess = true;
        }
    }
})();
