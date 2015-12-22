angular
    .module('myApp')
    .controller('NavbarController', NavbarController);

function NavbarController($mdSidenav, $log) {
    var vm = this;
    vm.toggleSideNav = buildToggler('right');
    vm.buildToggler = buildToggler;

    function buildToggler(navID) {
      return function() {
        $mdSidenav(navID)
          .toggle()
          .then(function () {
            //$log.debug("toggle " + navID + " is done");
          });
      }
    }


}