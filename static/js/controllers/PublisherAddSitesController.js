angular
    .module('myApp')
    .controller('PublisherAddSitesController', PublisherAddSitesController);

function PublisherAddSitesController(Website, $log, $state) {
    var vm = this;
    vm.addWebsite = addWebsite;
    vm.clear = clear;
    vm.publisher = {};
    vm.fileReader = new FileReader();

    vm.website = new Website();


    function addWebsite() {
        var f = document.getElementById("website_logo").files[0],
            r = new FileReader();
        r.onloadend = function (e) {
            vm.website.website_logo = e.target.result;

        };
        r.readAsBinaryString(f);

        if (angular.isDefined(vm.website.industry)) {
            vm.website.industry = [vm.website.industry.originalObject];
        }

        vm.website.$save(function (response) {

            $state.go('publisher.getcode');

        }, function (error) {

        });
    }

    function clear() {

    }

}