var app = angular.module('ninfo', []).
    config(['$routeProvider', function($routeProvider) {
    $routeProvider.
    when('/single',         {templateUrl: '/static/partials/single.html', controller: Single}).
    when('/single/:arg',    {templateUrl: '/static/partials/single.html', controller: SingleArg}).
    when('/multiple',       {templateUrl: '/static/partials/multiple.html', controller: Multiple}).
    otherwise({redirectTo: '/single'});
    }]);

function Single($scope, $routeParams, $location) {
    $scope.results = []
    $scope.lookup = function(){
        $location.url('/single/' + $scope.arg)
    };
}
function SingleArg($scope, $routeParams, $http, $location) {
    $scope.arg = $routeParams['arg'];
    $scope.lookup = function(){
        $location.url('/single/' + $scope.arg)
    };
    $http.get("/info/plugins").success(function(data){
        $.each(data, function(i,p){
            p.checked=true;
        });
        $scope.plugins = data;
    });
}
function Multiple($scope, $routeParams, $http) {
    $http.get("/info/plugins").success(function(data){
        $.each(data, function(i,p){
            p.checked=true;
        });
        $scope.plugins = data;
    });
    $scope.lookup = function(){
        var data = {q: $scope.q};
        $http({method:'GET', url: '/extract', params: data}).success(function(data){
            $scope.args = data.args;
            console.log($scope.args);
        });
    };
}

app.directive('result', function($http) {
    return {
    restrict: 'E',
    scope: {arg: '=arg', plugin: '=plugin'},
    link: function($scope, $element, $attrs){
        console.log($scope.plugin.name, $scope.arg, $scope.plugin.checked);
        if(!$scope.plugin.checked) {
            $scope.result=""
            return;
        }
        $scope.result="Loading...";
        $http.get("/info/html/" + $scope.plugin.name + "/" + $scope.arg).success(function(data){
            $scope.result=data;
        });
    },
    template:
    '<div ng-show="result">' +
    '<h2>{{plugin.name}} - {{plugin.title}} </h2>' +
    '<div ng-bind-html-unsafe="result"></div>' +
    '</div>'
    };
});

