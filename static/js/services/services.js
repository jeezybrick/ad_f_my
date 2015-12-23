

angular.module('myApp.services', ['ngResource'])

    .factory('Publisher', function ($resource) {
        return $resource('/api/publisher/'
            , {}, {
                'update': {method: 'PUT'},
                'query': {method: 'GET', isArray: false}
            });
    })

    .factory('Sponsor', function ($resource) {
        return $resource('/api/sponsor/'
            , {}, {
                'query': {method: 'GET', isArray: true}
            });
    })
    
    .factory('Website', function ($resource) {
        return $resource('/api/publisher/website/:id/'
            , {id: '@id'}, {
                'update': {method: 'PUT'},
                'query': {method: 'GET', isArray: true}
            });
    });

