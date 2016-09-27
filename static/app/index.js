// TODO - Clean up frontend code. Consider splitting into multiple controllers and maybe using services/factories for data parsing. Directives maybe?
// TODO HIGH PRIORITY - Auto-refresh graph
// TODO MEDIUM PRIORITY - Refresh button
// TODO MEDIUM PRIORITY - Graph zooming

var app = angular.module("mainApp", ["checklist-model"]);

app.controller("mainController", function($scope, $http) {
    //High level information regarding the game selected
    $scope.gameMetadata = [];
    //User help text
    $scope.gameSelHelpText = "";
    //Players to be graphed
    $scope.selectedPlayersHome = [];
    $scope.selectedPlayersAway = [];
    //Home and away team
    $scope.homeTeam;
    $scope.awayTeam;
    //Toggle visibility of checklists and stat selector
    $scope.hide = true;

    //Get games that occur on user provided date
    //TODO HIGH PRIORITY - Validate date given
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

    //Load the checklists which contain all the players playing in the game, so user can selecte players to graph
    $scope.loadChecklists = function(game)
    {
        //Need to reset these every time a new game is selected
        $scope.selectedPlayersHome = [];
        $scope.selectedPlayersAway = [];

        //Not sure if this really needs to be a $scope variable, but leave it for now
        $scope.selectedGame = game;

        //Un-hide content
        $scope.hide = false;

        //0 is away team, 1 is home team
        var teams = game['name'].split("@");

        //TODO MEDIUM PRIORITY - Better error messages
        $http.get("/roster/" + teams[0]).success(function (data, status, headers, config) {
            if(data['result'] === "Success") $scope.awayRoster = data['roster']
            else alert("Error obtaining roster data for" + teams[0]);
        })
        .error(function () {
            alert("There was an error reaching the server. Yay.");
        });

        $http.get("/team/fullname/" + teams[0]).success(function (data, status, headers, config) {
            $scope.awayTeam = data;
            $scope.awayTeamChecklist = data + " (team)";
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

        $http.get("/team/fullname/" + teams[1]).success(function (data, status, headers, config) {
            $scope.homeTeam = data;
            $scope.homeTeamChecklist = data + " (team)";
        })
        .error(function () {
            alert("There was an error reaching the server. Yay.");
        });
    }

    //Debug function
    $scope.printSelected = function(chosenPlayers)
    {
        console.log("Selected: " + chosenPlayers);
    }

    $scope.generateGraphData = function(chosenPlayersHome, chosenPlayersAway, chosenStat)
    {
        if(!chosenStat || (chosenPlayersHome.length === 0 && chosenPlayersAway.length === 0))
        {
            alert("Please select a stat AND players to graph");
        }
        else if (chosenPlayersHome.length + chosenPlayersAway.length > 4)
        {
            alert("Please choose at most 4 players to graph. Sorry for now.")
        }
        else
        {
            var homePlayers = "NOPLAYERS";
            if(chosenPlayersHome.length != 0)
            {
                homePlayers = generatePlayersString(chosenPlayersHome.slice(0), Object.keys($scope.homeRoster));
            }

            var awayPlayers = "NOPLAYERS";
            if(chosenPlayersAway.length != 0)
            {
                awayPlayers = generatePlayersString(chosenPlayersAway.slice(0), Object.keys($scope.awayRoster));
            }

            $http.get("/graphdata/" + $scope.selectedGame['id'] + "/" + chosenStat + "/" + homePlayers + "/" + awayPlayers).success(function (data, status, headers, config) {
                window.myLine = null;
                addColorOptionsToChart(data);
                console.log(data);
                var ctx = document.getElementById("myChart").getContext("2d");
                if(window.myLine){
                    window.myLine.destroy();
                }
			    window.myLine = new Chart(ctx, data);
            })
            .error(function () {
                alert("There was an error reaching the server. Yay.");
            });

        }

        //Join names together to pass to API endpoint while also identifying players who share a common last name with a teammate
        //TODO LOW PRIORITY - Consider moving this to the backend and making an extra API call to get the full roster to fully separate frontend and backend
        function generatePlayersString(chosenPlayersList, fullRoster){
            //console.log("Length of full roster: " + fullRoster.length);
            for(var i = 0; i < chosenPlayersList.length; i++){
                for(var j = 0; j < fullRoster.length; j++){
                    //console.log(chosenPlayersList[i] + ' ' + fullRoster[j] + " ===> " + fullRoster[j].indexOf(chosenPlayersList[i].split(' ')[1]))
                    if(chosenPlayersList[i] != fullRoster[j] && fullRoster[j].split(' ')[1] == chosenPlayersList[i].split(' ')[1]){
                        console.log(chosenPlayersList[i] + " shares the same last name as " + fullRoster[j]);
                        if(chosenPlayersList[i].indexOf("sharedlast") < 0){
                            chosenPlayersList[i] = "sharedlast" + chosenPlayersList[i];
                            break;
                        }
                    }
                }
            }

            //console.log("Chosen players modded: " + chosenPlayersList);
            return encodeURIComponent(chosenPlayersList.join('_'));
        }
    }
});