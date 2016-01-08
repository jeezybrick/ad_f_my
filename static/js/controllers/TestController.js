(function () {
    'use strict';
    angular
        .module('myApp', ['ngMaterial', 'ngMessages'])
        .controller('DemoCtrl', DemoCtrl);

    function DemoCtrl() {
        var self = this;

        self.simulateQuery = false;
        self.isDisabled = false;

        self.clear = clear;

        function clear() {

        }
    }
})();
