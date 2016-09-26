// TODO LOW PRIORITY - Make colors prettier

function randomColorFactor() {
    return Math.round(Math.random() * 255);
}

function randomColor(opacity) {
	return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',' + (opacity || '.3') + ')';
}

function addColorOptionsToChart(chartData){
    $.each(chartData.data.datasets, function(i, dataset) {
			dataset.borderColor = randomColor(0.4);
			dataset.backgroundColor = randomColor(0.5);
			dataset.pointBorderColor = randomColor(0.7);
			dataset.pointBackgroundColor = randomColor(0.5);
			dataset.pointBorderWidth = 1;
	});
}

function formatTimesAsMoments(chartData){
    $.each(chartData.data.datasets, function(i, dataset) {
        $.each(dataset.data, function(i, datapoint) {
            datapoint.x = moment(x, "mm:ss")
        })
    });
}