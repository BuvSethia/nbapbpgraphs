var app = angular.module("mainApp", ["checklist-model"]);

app.controller("mainController", function($scope, $http) {
    $scope.gamedate = "4-29-2016";
    $scope.gameMetadata = [];
    $scope.gameSelHelpText = "";
    $scope.selectedPlayers = [];
    
    $scope.getGamesForDate = function(date)
    {
        console.log(date);
        var games = $http.get("/games/" + date);
        games.success(function (data, status, headers, config) {
            if(data['result'] === "Success")
            {
                console.log(data['gameList']);
                $scope.gameMetadata = data['gameList'];
                $scope.gameSelHelpText = "Games found. Please select one.";
            }
            else
            {
                $scope.gameSelHelpText = "Games not found for date. Ensure valid date is input as mm-dd-yyyy.";
            }
        });
        games.error(function () {
            $scope.gameSelHelpText = "There was an error obtaining the games for the specified date. Please try again later.";
        });
    };

    $scope.loadChecklists = function(game)
    {
        //0 is away team, 1 is home team
        var teams = game['name'].split("@");

        $http.get("/roster/" + teams[0]).success(function (data, status, headers, config) {
            if(data['result'] === "Success") $scope.awayRoster = data['roster']
            else alert("Error obtaining roster data for" + teams[0]);
        })
        .error(function () {
            alert("There was an error reaching the server. Yay.");
        });

        $http.get("/roster/" + teams[1]).success(function (data, status, headers, config) {
            if(data['result'] === "Success") $scope.homeRoster = data['roster']
            else alert("Error obtaining roster data for" + teams[1]);
        })
        .error(function () {
            alert("There was an error reaching the server. Yay.");
        });
    }
    $scope.printSelected = function()
    {
        console.log("Selected: " + $scope.selectedPlayers);
    }
});