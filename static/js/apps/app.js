
angular
    .module('myApp', [
        'ngResource',
        'myApp.services',
    ])
    .config(function ($locationProvider, $httpProvider, $resourceProvider, $interpolateProvider) {

        // CSRF Support
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $resourceProvider.defaults.stripTrailingSlashes = false;

        // Force angular to use square brackets for template tag
        // The alternative is using {% verbatim %}
        $interpolateProvider.startSymbol('[[').endSymbol(']]');


    });