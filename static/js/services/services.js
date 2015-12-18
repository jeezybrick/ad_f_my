/**
 * Created by user on 05.10.15.
 */


angular.module('myApp.services', ['ngResource'])

    .factory('Publisher', function ($resource) {
        return $resource('/api/publisher/'
            , {}, {
                'update': {method: 'PUT'},
                'query': {method: 'GET', isArray: false}
            });
    })
    .factory('Sponsor', function ($resource) {
        return $resource('/api/advertisers/'
            , {}, {
                'query': {method: 'GET', isArray: true}
            });
    });

