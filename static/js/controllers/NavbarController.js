angular
    .module('myApp')
    .controller('NavbarController', NavbarController);

function NavbarController($mdSidenav, $log) {
    var vm = this;
    vm.toggleSideNav = buildToggler('right');
    vm.buildToggler = buildToggler;
    vm.close = close;
    vm.openMenu = openMenu;

    function buildToggler(navID) {
        return function () {
            $mdSidenav(navID)
                .toggle()
                .then(function () {
                    //$log.debug("toggle " + navID + " is done");
                });
        }
    }

    function openMenu($mdOpenMenu, ev) {
        var originatorEv = ev;
        $mdOpenMenu(ev);
    }

    function close() {
        $log.debug("'''''''''''''");
        $mdSidenav('right').close()
            .then(function () {
                // $log.debug("close LEFT is done");
            });
    }


}