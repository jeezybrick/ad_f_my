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

    /**
     * Get item detail
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

        if (vm.website.website_logo === null) {
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

        }

        Upload.upload({
            url: '/api/publisher/website/' + $stateParams.id + '/',
            data: sendData,
            method: 'PUT'
        }).then(function (resp) {
            $state.go('publisher.sites');
        }, function (err) {
            console.log('Error status: ' + err);
        }, function (evt) {
        });


    }

    function clear() {

    }

}