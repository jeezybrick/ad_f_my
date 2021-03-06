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
        'ui.bootstrap',
        'ngFileUpload',
        'flash'
    ])
    .config(function ($locationProvider, $httpProvider, $resourceProvider, $interpolateProvider, $routeProvider,
                      $compileProvider, $stateProvider, $urlRouterProvider, $mdThemingProvider) {


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

        $mdThemingProvider.theme('error-toast');


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
            .state('publisher.changepassword', {
                url: 'profile/change-password/',
                templateUrl: '/static/pages/publisher/change-password.html',
                controller: 'EditProfileController',
                controllerAs: 'vm'
            })
            .state('publisher.sites', {
                url: 'sites/',
                templateUrl: '/static/pages/publisher/sites/index.html',
                controller: 'PublisherSitesController',
                controllerAs: 'vm'
            })
            .state('publisher.editsites', {
                url: 'sites/edit-sites/:id/',
                templateUrl: '/static/pages/publisher/sites/edit.html',
                controller: 'PublisherEditSitesController',
                controllerAs: 'vm'
            })
            .state('publisher.addsites', {
                url: 'sites/add-sites/',
                templateUrl: '/static/pages/publisher/sites/add.html',
                controller: 'PublisherAddSitesController',
                controllerAs: 'vm'
            })
            .state('publisher.addsite-after', {
                url: 'sites/add/',
                templateUrl: '/static/pages/publisher/sites/add_after.html',
                controller: 'PublisherAddSitesController',
                controllerAs: 'vm'
            })
            .state('publisher.getcode', {
                url: 'sites/get-code/',
                templateUrl: '/static/pages/publisher/sites/get_code.html',
                controller: 'PublisherController',
                controllerAs: 'vm'
            })
            .state('publisher.audience', {
                url: 'audience/',
                templateUrl: '/static/pages/publisher/audience.html',
                controller: 'PublisherController',
                controllerAs: 'vm'
            });

        /*.state('publisher.login', {
         url: 'login/',
         templateUrl: '/static/pages/publisher/login.html',
         controller: 'PublisherController',
         controllerAs: 'vm'
         })*/

    });