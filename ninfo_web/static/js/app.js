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
    $scope.status = {
        total:0,
        running:0,
        finished:0
    };
    $http.get("/info/plugins").success(function(data){
        $.each(data, function(i,p){
            p.checked=true;
            $scope.status.total++;
        });
        $scope.plugins = data;
    });

    $scope.percent = function() {
        return 100 * ($scope.status.finished / $scope.status.total);
    };
    $scope.bar_style = function() {
        return {"width": $scope.percent() + "%"};
    };

    $scope.scroll_to = function(plugin) {
        var selector = "#result_" + plugin;
        var targetOffset = $(selector).offset().top;
        $('html,body').animate({scrollTop: targetOffset-55}, 500);
    };


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
        if(!$scope.plugin.checked) {
            $scope.result=""
            return;
        }
        $scope.result="Loading...";
        $scope.plugin.running=true;
        $scope.$parent.status.running++;
        $http.get("/info/html/" + $scope.plugin.name + "/" + $scope.arg).success(function(data){
            $scope.plugin.result=data;
            $scope.result=data;
            $scope.plugin.running=false;
            $scope.$parent.status.running--;
            $scope.$parent.status.finished++;
        });
    },
    template:
    '<div ng-show="result" id="result_{{plugin.name}}">' +
    '<h2>{{plugin.name}} - {{plugin.title}} </h2>' +
    '<div ng-bind-html-unsafe="result"></div>' +
    '<hr>' +
    '</div>'
    };
});

