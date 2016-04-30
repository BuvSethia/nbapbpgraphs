var app = angular.module("mainApp", []);

app.controller("mainController", function($scope, $http) {
    $scope.gamedate = "4-29-2016";
    $scope.gameMetadata = [];
    $scope.gameSelHelpText = "";
    $scope.getGamesForDate = function(date)
    {
        console.log(date);
        var games = $http.get("/games/" + date);
        games.success(function (data, status, headers, config) {
            console.log(data['gameList']);
            $scope.gameMetadata = data['gameList'];
            $scope.gameSelHelpText = "Games found. Please select one.";
        });
        games.error(function () {
            $scope.gameSelHelpText = "There was an error obtaining the games for the specified date. Please try again later.";
        });
    };
});