angular
    .module('myApp', [
        'ngRoute',
        'ngResource',
        'ngSanitize',
        'ngMessages',
        'ngAnimate',
        'ui.router',
        'myApp.services',

        'ngMaterial',
        'ngMdIcons',
        'angucomplete-alt',
        'ui.bootstrap'
    ])
    .config(function ($locationProvider, $httpProvider, $resourceProvider, $interpolateProvider, $routeProvider,
                      $compileProvider, $stateProvider, $urlRouterProvider) {


        // CSRF Support
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $resourceProvider.defaults.stripTrailingSlashes = false;

        // Force angular to use square brackets for template tag
        // The alternative is using {% verbatim %}
        $interpolateProvider.startSymbol('[[').endSymbol(']]');

        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension):/);

        // enable html5Mode for pushstate ('#'-less URLs)
        //$locationProvider.html5Mode(true);
        //$locationProvider.hashPrefix('!');


        // Routing
        $urlRouterProvider.otherwise('/');
        $stateProvider

            .state('publisher', {
                url: '/',
                templateUrl: '/static/pages/publisher/index.html',
                controller: 'PublisherController',
                controllerAs: 'vm',

            })
            .state('publisher.advertisers', {
                url: 'advertisers/',
                templateUrl: '/static/pages/publisher/advertisers.html',
                controller: 'AdvertisersController',
                controllerAs: 'vm',

            })
            .state('publisher.dashboard', {
                url: 'dashboard/',
                templateUrl: '/static/pages/publisher/dashboard.html',
                controller: 'PublisherController',
                controllerAs: 'vm'
            })
            .state('publisher.profile', {
                url: 'profile/',
                templateUrl: '/static/pages/publisher/profile.html',
                controller: 'EditProfileController',
                controllerAs: 'vm'
            })
            .state('publisher.sites', {
                url: 'publisher/sites/',
                templateUrl: '/static/pages/publisher/sites/index.html',
                controller: 'PublisherSitesController',
                controllerAs: 'vm'
            })
            .state('publisher.addsites', {
                url: 'sites/add-sites/',
                templateUrl: '/static/pages/publisher/sites/add.html',
                controller: 'PublisherSitesController',
                controllerAs: 'vm'
            })
            .state('publisher.getcode', {
                url: 'publisher/sites/get-code/',
                templateUrl: '/static/pages/publisher/sites/get_code.html',
                controller: 'PublisherController',
                controllerAs: 'vm'
            })
            .state('publisher.login', {
                url: 'publisher/login/',
                templateUrl: '/static/pages/publisher/login.html',
                controller: 'PublisherController',
                controllerAs: 'vm'
            })

    });