angular
    .module('myApp')
    .controller('SidebarController', SidebarController);

function SidebarController($mdSidenav, $log) {
    var vm = this;
    vm.close = close;

     function close () {
      $mdSidenav('right').close()
        .then(function () {
         // $log.debug("close LEFT is done");
        });
    }

}