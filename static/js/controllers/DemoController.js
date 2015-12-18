angular
    .module('myApp')
    .controller('DemoController', DemoController);

function DemoController($scope) {

    $scope.alerts = [
        {type: 'danger', msg: 'Oh snap! Change a few things up and try submitting again.'},
        {type: 'success', msg: 'Well done! You successfully read this important alert message.'}
    ];
    $scope.timeout = 3000;

    $scope.addAlert = function () {
        $scope.alerts.push({msg: 'Another alert!'});
    };

    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };
}