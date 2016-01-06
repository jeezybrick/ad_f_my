angular
    .module('myApp')
    .controller('PublisherController', PublisherController);

function PublisherController(Sponsor, Publisher, Website, $log, $location, $state, $stateParams, $http) {
    var vm = this;
    vm.addSponsors = addSponsors;
    vm.completeRegistration = completeRegistration;
    vm.clear = clear;

    vm.isSponsorsLoad = false;
    vm.publisherLoadError = '';
    vm.sponsors_type = {};
    vm.publisher_default = {};
    vm.getCodeScriptText = '';
    vm.completeRegisterPage = '/api/complete-setup/';

    vm.sponsors_type = Sponsor.query(function (response) {

        vm.isSponsorsLoad = true;

    }, function () {

    });

    vm.publisher = Publisher.query(function (response) {

        if(angular.equals(response.is_completed_auth, 'get_code')) {
           $state.go('publisher.getcode');
        }else if(angular.equals(response.is_completed_auth, 'add_website')){
            $state.go('publisher.addsites');
        }else if(angular.equals(response.is_completed_auth, 'advertisers')){
            $state.go('publisher.advertisers');
        }

        vm.website = Website.query(function (response) {
            if(response.results){
                vm.getCodeScriptText = '<div id="ad-adfits" pub_id="' + vm.publisher.id + '" web_id="' + vm.website.results[0].id + '">' +
                '<script src="http://adfits.com/static/js/tag/ads.js"></script>' +
                '</div>';
            }

        }, function (error) {

            vm.websitesLoadError = error.data;

        });


    }, function (error) {
        vm.publisherLoadError = error.data[0];
    });

    function addSponsors() {

        $state.go('publisher.dashboard');

    }

    function completeRegistration() {
        $http.post(vm.completeRegisterPage, {publisher_id: vm.publisher.id}).success(function (data) {

            //$state.go('publisher.dashboard', {}, {reload: true});
            window.location.href = '/publisher/';

        });

    }

    function clear() {

        $state.transitionTo($state.current, $stateParams, {
            reload: true, inherit: false, notify: false
        });

    }

}
