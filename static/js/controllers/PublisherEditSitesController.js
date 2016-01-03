angular
    .module('myApp')
    .controller('PublisherEditSitesController', PublisherEditSitesController);

function PublisherEditSitesController(Website, Publisher, $log, $state, $stateParams, Upload, $mdDialog) {
    var vm = this;
    vm.editWebsite = editWebsite;
    vm.clear = clear;
    vm.showJsTag = showJsTag;

    vm.publisher = {};
    vm.website = {};
    vm.test = {};
    vm.jsTag = '';
    vm.editWebsiteProcess = false;

    /**
     * Get website detail
     */
    vm.website = Website.get({id: $stateParams.id}, function (response) {
        vm.publisher = Publisher.query(function (response) {
            vm.jsTag = '<div id="ad-adfits" pub_id="' + vm.publisher.id + '" web_id="' + vm.website.id + '">' +
                '<script src="http://adfits.com/static/js/tag/ads.js"></script>' +
                '</div>';
        }, function () {

        });
        vm.test = response.website_logo;

    }, function (error) {

    });

    function showJsTag(ev) {

        $mdDialog.show(
            $mdDialog.alert()
                .parent(angular.element(document.querySelector('#popupContainer')))
                .clickOutsideToClose(true)
                .title('JS tag')
                .textContent(vm.jsTag)
                .ariaLabel('Alert Dialog Demo')
                .ok('Got it!')
                .targetEvent(ev)
        );
    }


    function editWebsite() {
        vm.editWebsiteProcess = true;

        /*vm.website.$update(function (response) {


        }, function (error) {

        });*/

        /*if (vm.website.website_logo === null) {
            var sendData = {
                website_name: vm.website.website_name,
                website_domain: vm.website.website_domain,
            };

        } else {

            var sendData = {
                website_name: vm.website.website_name,
                website_domain: vm.website.website_domain,
                website_logo: vm.website.website_logo,
            };

        }*/

        Upload.upload({
            url: '/api/publisher/website/' + $stateParams.id + '/',
            data: {
                website_name:vm.website.website_name,
                website_domain:vm.website.website_domain,
                twitter_name:vm.website.twitter_name,
                facebook_page:vm.website.facebook_page,
            },
            file:vm.website_logo,
            method: 'PUT'
        }).then(function (resp) {
            vm.editWebsiteProcess = false;
            $state.go('publisher.sites');
        }, function (err) {
            vm.editWebsiteProcess = false;
        }, function (evt) {
        });


    }

    function clear() {

    }

}