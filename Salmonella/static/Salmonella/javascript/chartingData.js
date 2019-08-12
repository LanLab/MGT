
function getDataForCharting(tn, url){
	// console.log(tn);
	// console.log(url);
	$("#btn_"+tn).attr("disabled", true);

	var tnDiv = document.getElementById(tn);

	console.log(tnDiv);
	if (tnDiv.style.display !== 'none'){
		 //  if active then make inactive and hide
		 console.log("it is non!");
		 tnDiv.style.display = 'none';
		 $("#btn_"+tn).attr("disabled", false);
	 	return;
	}

	else if (tnDiv.style.display === 'none'){
		if(document.getElementById("theChart_"+tn).getElementsByTagName('svg').length > 0 ){
			tnDiv.style.display = '';
			// console.log("it has children");
			// console.log(tnDiv);
			$("#btn_"+tn).attr("disabled", false);
			return;
		}
	}

	// else if: already added just show,

	// else:  send ajax request.
	getDataAndDoTopInfoPlot(tn, url);

}

function getDataAndDoTopInfoPlot(tn, url){
	$.ajax({
		type: 'POST',
		url: url,
		data: {
			'tn': tn,
		},
		// dataType: 'html',
		success: function(response){
			// make div active!
			// console.log("Response recieved");
			var isoCountByLoc = response.shift();

			// console.log(response);
			// convert data to right format
			[data, totalLeft] = convertCountToRatio(response[0], isoCountByLoc);

			// Do the plotting
			addThePlot(tn, data, totalLeft);

			// Show the plot
			$('#'+tn).show();
			$("#btn_"+tn).attr("disabled", false);
		},
		error: function (xhr, status, error) {
			// alert('AJAX error.');
			xhr.abort();
			console.log(error);
		}
	});
}

function convertCountToRatio(data, isoCountByLocTot){
	// console.log("convertCountToRatio");
	/// console.log(totalNumIsolates);
	// console.log(data)


	// console.log(isoCountByLocTot)
	// console.log(data);

	var totalLeft = {};

	for (var i = 0; i < data.length; i++){
		if (data[i].hasOwnProperty('continent') && data[i].continent != null){
			// if (!totalLeft.hasOwnProperty(data[i].continent)){
			//	totalLeft[data[i].continent] = parseFloat(isoCountByLocTot[0][data[i].continent]) - parseFloat(data[i].count);
			//}
			//else{

			//}

			// continent = data[i].continent;
			// console.log(data[i].count + " " + continent + " " + isoCountByLocTot[0][data[i].continent]);
			res =(parseFloat(data[i].count)/parseFloat(isoCountByLocTot[0][data[i].continent]) * 100).toFixed(2);

			data[i].ratio = parseFloat(res);

			if (!totalLeft.hasOwnProperty(data[i].continent)){
				totalLeft[data[i].continent] = data[i].ratio;
			}
			else{
				totalLeft[data[i].continent] = totalLeft[data[i].continent] + data[i].ratio;
			}
			// if
			// totalLeft =
		}
	}

	for (var continent in totalLeft){
    	if (totalLeft.hasOwnProperty(continent)) {
        	totalLeft[continent] = 100 - totalLeft[continent];
    	}
	}


	console.log(totalLeft);
	// console.log(data)

	return [data, totalLeft];
}

function addThePlot(tn, data, totalLeft){


	const width = 300;
	const height = 500;

	// set up svg
	var theChart_svg = d3.select("#theChart_" + tn).append('svg');
	theChart_svg.attr('width', width).attr('height', height);


	// tool tip
	var toolTip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

	// console.log(theChart_svg);

	const xScale = d3.scaleLinear()
		.domain([0, 300])
		.range([0, 300])

	// append wrap
	const g = theChart_svg.append('g');

		// .attr('class', 'ratio-wrap');


	// append rectangles & text

	var dict_stToCol = {};
	var rectCol = "";

	var barX = 0;
	var barY = 10;
	for (var continent in totalLeft){

		var barHeight = 200;
		barY = 100;
		for (var i = 0; i < data.length; i++){
			if (data[i].hasOwnProperty('continent') && data[i].continent != null && data[i].continent == continent){

				if (dict_stToCol.hasOwnProperty(data[i].st)){
					rectCol = dict_stToCol[data[i].st];
				}
				else {
					rectCol = getRandomColor();
					dict_stToCol[data[i].st] = rectCol;
				}

			 	bar = g.append('rect')
					.attr('width', 40)
					.attr('height', data[i].ratio * 4)
					.attr('x', barX)
					.attr('y', barY)
					.style('fill', rectCol)
					.style('opacity', 0.5)
					.style('stroke', rectCol);

				bar.data([data[i]])
					.on("mouseover", function(d) {
						// console.log("d is here " + d.count);
						toolTip.transition()
							.duration(200)
							.style("opacity", .9);
							toolTip.html("ST-" + d.st + "<br> Count: "+ d.count)
								.style("left", (d3.event.pageX) + "px")
								.style("top", (d3.event.pageY) + "px");
					})
					.on("mouseout", function(d) {
						toolTip.transition()
						// .duration(500)
						.style("opacity", 0);
					});




				barY = barY + data[i].ratio * 4;

				// console.log(continent + " 10 " + data[i].count + " " + barX + " " + barY);


			}
		}

		g.append('rect')
			.attr('width', 40)
			.attr('height', totalLeft[continent] * 4)
			.attr('x', barX)
			.attr('y', barY)
			.style('fill', "#F5F5F5");



		var counter = 1;
		g.append("text")
			.attr("class", "x axis")
			.text(continent)
			.style("font-size", "11px")
			.classed('rotation', true)
		  	.attr('fill', 'black')
		  	.attr('transform', (d,i)=>{
			   return 'translate( '+xScale(barX+25) +' , '+95+'),'+ 'rotate(-90)';})
		  	.attr('x', 0)
		  	.attr('y', 0);


		barX = barX + 40;
		console.log(continent);
	}


}


function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}
