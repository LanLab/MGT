
// LAYOUT OF ALL TABLES #################################
var ServerStatus = {"U": "Reads uploaded", 'V': "Alleles uploaded", 'I': "In server queue", 'R': 'Running reads to alleles', 'S': 'Running alleles to MGT', 'H': "Job held", 'C': "Job complete", 'D': 'To download NCBI reads'}, value=1, key; // TODO: complete this.

var AssignStatus = {'A': 'MGT assigned', 'F': 'Failed: contamination', 'G': 'Failed: genome quality', 'S': 'Failed: serovar incompatibility', 'E': 'Error: other'}, value=1, key;

var IsoPrivStatus = {"PU": "Public", "PV": "Private"}, value=1, key;



function getCellInnerHtml(table_name, display_name, tnStr, sessionVar, searchVar_str){
	// console.log(table_name + " " + display_name + " " + tnStr + " " + sessionVar + " " + searchVar_str);
	var tnToChk = tnStr + "." + table_name;
	var innerStr = '<b> <button id=\'' + table_name + '\'';

	if (sessionVar[0].hasOwnProperty('orderBy') && tnToChk == sessionVar[0].orderBy) {
		innerStr  =  innerStr + ' class=\'' +  sessionVar[0].dir + ' btn btn-link\' ';
	}
	else{
		innerStr = innerStr + ' class="btn btn-link" ';
	}
	innerStr = innerStr +  ' onclick="javascript:doTheOrderBy(\'' + table_name + '\', \'' + searchVar_str + '\', \'' + tnStr + '\')"> ' + display_name ;
	if (sessionVar[0].hasOwnProperty('orderBy') && tnToChk == sessionVar[0].orderBy && sessionVar[0].dir == sort_forward) {
		innerStr  =  innerStr + '<sup>v</sup>';
	}
	else if (sessionVar[0].hasOwnProperty('orderBy') && tnToChk == sessionVar[0].orderBy && sessionVar[0].dir == sort_reverse){
		innerStr  =  innerStr + '<sup>^</sup>';
	}
	else{
	}
	innerStr = innerStr + " </button> </b>";

	return (innerStr);
}


function printHeader(row, isoInfo, isAp, apOrCcHeader, epiHeader, locHeader, islnHeader, searchVar){ // , apOrCcHeader, isAp, epiHeader, locHeader, isolnHeader, isPriv){

	row.classList.add('is-selected');

	var dispColCounter = 0;

	// console.log("over here!!!!");
	// console.log(isoInfo);

	var searchVar_str = JSON.stringify(searchVar);
	searchVar_str = searchVar_str.replace(/\"/g, "\\'");

	// searchVar_str = searchVar_str.replace(/\".i)
	// searchVar_str = searchVar_str.replace(/\\/g, '\'');

	for (var i = 0; i<isoInfo.length; i++){
		var cell = row.insertCell(dispColCounter++);
		var innerStr = getCellInnerHtml(isoInfo[i].table_name, isoInfo[i].display_name, 'i', searchVar, searchVar_str);
		cell.innerHTML = innerStr;
	}

	console.log(apOrCcHeader);
	for  (var i = 0; i< apOrCcHeader.length; i++){
		var cell = row.insertCell(dispColCounter++);

		if (! isAp || isAp == false) {
			// cell.innerHTML = "<b>" + apOrCcHeader[i].display_name.replace(/[\"]/g, "") + "</b>";
			var innerStr = getCellInnerHtml(apOrCcHeader[i].table_name, apOrCcHeader[i].display_name.replace(/[\"]/g, ""), 'v', searchVar, searchVar_str);
		}
		else {
			// cell.innerHTML = "<b>" + apOrCcHeader[i].scheme__display_name.replace(/[\"]/g, "") + "</b>";
			console.log(apOrCcHeader[i]);
			var innerStr = getCellInnerHtml(apOrCcHeader[i].table_name + "_st", apOrCcHeader[i].scheme__display_name.replace(/[\"]/g, ""), 'v', searchVar, searchVar_str);
		}
		cell.innerHTML = innerStr;
	}

	// printing an empty column
	var cell = row.insertCell(dispColCounter++);
	cell.innerHTML = "";


	// console.log(epiHeader);
	for (var i = 0; i< epiHeader.length; i++) {
		var cell = row.insertCell(dispColCounter++);
		var innerStr = getCellInnerHtml(epiHeader[i].table_name, epiHeader[i].display_name.replace(/[\"]/g, ""), 'v', searchVar, searchVar_str);
		// cell.innerHTML = "<b>" + epiHeader[i].display_name.replace(/[\"]/g, "") + "</b>";
		cell.innerHTML = innerStr;
	}


	for (var i = 0; i < locHeader.length; i++) {
		var cell = row.insertCell(dispColCounter++);
		var innerStr = getCellInnerHtml(locHeader[i].table_name, locHeader[i].display_name, 'iM_l', searchVar, searchVar_str);
		cell.innerHTML = innerStr;  // "<b>" + locHeader[i].display_name + "</b>";
	}

	for (var i = 0; i< islnHeader.length; i++) {
		var cell = row.insertCell(dispColCounter++);
		var innerStr = getCellInnerHtml(islnHeader[i].table_name, islnHeader[i].display_name, 'iM_i', searchVar, searchVar_str);
		cell.innerHTML =  innerStr; // "<b>" + islnHeader[i].display_name + "</b>";
	}

}

function printEpidemeologyCols(isolate, colEpiStart, colEpiEnd, dispColCounter, row){

	for (var j=parseInt(colEpiStart); j <= colEpiEnd; j=j+2){
		cell = row.insertCell(dispColCounter++);

		if (isolate[j] == null){
			cell.innerHTML = "-";
		}
		else {
			cell.innerHTML = isolate[j];
		}
	}

	return dispColCounter;

}


function printIsoMeta(isolate, dispColCounter, row, locInfo){

	for (var i = 0; i<locInfo.length; i++){
		cell = row.insertCell(dispColCounter++);

		if (isolate[parseInt(locInfo[i].db_col)] == null){
			cell.innerHTML = "-";
		}
		else {
			cell.innerHTML = isolate[parseInt(locInfo[i].db_col)];
		}
	}
	return dispColCounter;

}


function isValExist(val){
	// console.log(val);
	if (typeof val === 'undefined' || val === ''){
		return false;
	}

	return true;
}

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  rgbaCol = hexToRgbA(color);
  return rgbaCol;
}

function hexToRgbA(hex){
    var c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+',0.5)';
    }
    throw new Error('Bad Hex');
}

function doCcLayout(isolates, colIsoId, isoInfo, ccInfo, mgtInfo, epiInfo, locInfo, islnInfo, searchVar, isShowCol){
	console.log("doLayoutCC - searchVar");
	console.log(searchVar);

	$('#isolateTable').show();

	removeClassFromBtn("apView", "is-primary");
	addClassToBtn("ccView", "is-primary");

	// console.log(locHeader);
	// var isolateHeader = ["Isolate name", "Status"];

	/* TODO: move these two to the return of the ajax function itself. */
	// hideDiv("apSearch", "apView");
	// showDiv("ccSearch", "ccView")

	var tab = document.getElementById("infoTable");
	tab.innerHTML = "";

	if (isolates.length == 0){
		tab.innerHTML = "No isolates here.";
		return;
	}

	var dispRowCounter = 0;

	var tab = document.getElementById("infoTable");
	tab.innerHTML = "";


	// console.log(isolnHeader);
	// var tabHeader = tab.createTHead();

	var row = tab.insertRow(dispRowCounter++);
	printHeader(row, isoInfo, false, ccInfo, epiInfo, locInfo, islnInfo, searchVar);

	var cell = null;
	var row = null;

	var hue = 0;
	var theColor = getRandomColor(); // getColor(hue);

	var stCol = {};
	var stColKey = "";

	for (var i=0; i<isolates.length; i++){
		row = tab.insertRow(dispRowCounter++);

		var dispColCounter = 0;

		dispColCounter = printIsolateCols(row, isolates[i], dispColCounter, colIsoId, isoInfo);

		// dispColCounter = printEpidemeologyCols(isolates[i], mgtInfo[0].ccStart, mgtInfo[0].ccEnd, dispColCounter, row);

		for (var j=parseInt(mgtInfo[0].ccStart); j <= mgtInfo[0].ccEnd; j=j+2){
			cell = row.insertCell(dispColCounter++);

			if (isolates[i][j] == null){
				cell.innerHTML = "-";
			}
			else {
				if (isolates[i][j+1] != null){
					var minCc = Math.min(isolates[i][j], isolates[i][(j+1)]);
					cell.innerHTML = minCc;
					stColKey = j +"_" + minCc;

				}
				else{
					cell.innerHTML = isolates[i][j];
					stColKey = j +"_" + isolates[i][j];
				}

				if (!stCol.hasOwnProperty(stColKey)){
					hue = updateHue(hue);
					theColor = getRandomColor(); // getColor(hue);
					stCol[stColKey] = theColor;
					// stCol[stColKey] = getRandomColor();
				}
				else if ( stCol.hasOwnProperty(stColKey)){
					theColor = stCol[stColKey];
				}

				if (isShowCol == true){
					cell.style.backgroundColor = theColor;
				}

			}
		}


		//setColour(isolates[i], isolates[i-1], tab.rows[(i)].cells[(dispColCounter-1)].style.backgroundColor);


		cell = row.insertCell(dispColCounter++);
		cell.innerHTML = ""; // empty col.



		// dispColCounter = printEpidemeologyCols(isolates[i], mgtInfo[0].epiStart, mgtInfo[0].epiEnd, dispColCounter, row);

		for (var j=parseInt(mgtInfo[0].epiStart); j <= mgtInfo[0].epiEnd; j=j+2){
			cell = row.insertCell(dispColCounter++);

			if (isolates[i][j] == null){
				cell.innerHTML = "-";
			}
			else {


				if (isolates[i][j+1] != null){
					var minCc = Math.min(isolates[i][j], isolates[i][(j+1)]);
					cell.innerHTML = minCc;
					stColKey = j +"_" + minCc;

				}
				else{
					cell.innerHTML = isolates[i][j];
					stColKey = j +"_" + isolates[i][j];
				}
				// cell.innerHTML = isolates[i][j];

				if (!stCol.hasOwnProperty(stColKey)){
					hue = updateHue(hue);
					theColor = getRandomColor(); // getColor(hue);
					stCol[stColKey] = theColor;
				}
				else if ( stCol.hasOwnProperty(stColKey)){
					theColor = stCol[stColKey];
				}

				if (isShowCol == true){
					cell.style.backgroundColor = theColor;
				}


			}
		}

		dispColCounter = printIsoMeta(isolates[i], dispColCounter, row, locInfo);

		dispColCounter = printIsoMeta(isolates[i], dispColCounter, row, islnInfo);
	}
}




function updateHue(hue){

	hue = hue + 9;

	if (hue > 360){
		hue = hue % 360;
	}
	return (hue);
}

function getColor(hue){
	return ("hsl(" + hue + ", 90%, 80% )");
	// https://stackoverflow.com/questions/43193341/how-to-generate-random-pastel-or-brighter-color-in-javascript
}


function doApLayout(isolates, colIsoId, isoInfo, apInfo, mgtInfo, epiInfo, locInfo, islnInfo, searchVar, isShowCol, isShowDst){

	console.log("is showmgt color  is " + isShowCol);

	// console.log(".... |||| ....");
	// console.log(isoInfo);

	// console.log(searchVar);


	$('#isolateTable').show();


	/* TODO: move these two to the return of the ajax function itself. */
	// hideDiv("ccSearch", "ccView");
	// showDiv("apSearch", "apView");
	removeClassFromBtn("ccView", "is-primary");
	addClassToBtn("apView", "is-primary");

	var tab = document.getElementById("infoTable");
	tab.innerHTML = "";

	if (isolates.length == 0){
		tab.innerHTML = "No isolates here.";
		return;
	}

	var dispRowCounter = 0;

	var row = tab.insertRow(dispRowCounter++);

	printHeader(row, isoInfo, true, apInfo, epiInfo, locInfo, islnInfo, searchVar); //, apHeader, true, epiHeader, locHeader, isolnHeader, isPriv);

	var cell = null;
	// var prevVal = null;
	var hue = 0;
	var theColor = getRandomColor(); // getColor(hue);

	var stCol = {};
	var stColKey = "";

	for (var i=0; i<isolates.length; i++){
		row = tab.insertRow(dispRowCounter++);

		var dispColCounter = 0;

		dispColCounter = printIsolateCols(row, isolates[i], dispColCounter, colIsoId, isoInfo);

		for (var j=parseInt(mgtInfo[0].apStart); j <= mgtInfo[0].apEnd; j=j+3){
			cell = row.insertCell(dispColCounter++);
			if (isolates[i][(j+1)] == null){
				cell.innerHTML = "-";
			}
			else {
				cell.innerHTML = isolates[i][(j+1)];

				stColKey = (j+1) + "_" + isolates[i][(j+1)];
				/* start: set color */

				// console.log(stColKey);
				if (!stCol.hasOwnProperty(stColKey)){
					hue = updateHue(hue);
					theColor = getRandomColor(); // getColor(hue);
					stCol[stColKey] = theColor;
				}
				else if ( stCol.hasOwnProperty(stColKey)){
					theColor = stCol[stColKey];
				}

				if (isShowCol == true) {
					cell.style.backgroundColor = theColor;
				}

				/* end: set color */
				if (isShowDst == true){
					if (isolates[i][(j+2)] != 0){
						cell.innerHTML = cell.innerHTML + "." + isolates[i][(j+2)];
					}
				}

			}
		}


		cell = row.insertCell(dispColCounter++);
		cell.innerHTML = ""; // empty col.


		// dispColCounter = printEpidemeologyCols(isolates[i], mgtInfo[0].epiStart, mgtInfo[0].epiEnd, dispColCounter, row);

		for (var j=parseInt(mgtInfo[0].epiStart); j <= mgtInfo[0].epiEnd; j=j+2){
			cell = row.insertCell(dispColCounter++);

			if (isolates[i][j] == null){
				cell.innerHTML = "-";
			}
			else {

				if (isolates[i][j+1] != null){
					var minCc = Math.min(isolates[i][j], isolates[i][(j+1)]);
					cell.innerHTML = minCc;
					stColKey = j +"_" + minCc;

				}
				else{
					cell.innerHTML = isolates[i][j];
					stColKey = j +"_" + isolates[i][j];
				}

				if (!stCol.hasOwnProperty(stColKey)){
					hue = updateHue(hue);
					theColor = getRandomColor(); // getColor(hue);
					stCol[stColKey] = theColor;
				}
				else if ( stCol.hasOwnProperty(stColKey)){
					theColor = stCol[stColKey];
				}

				if (isShowCol == true){
					cell.style.backgroundColor = theColor;
				}


			}
		}

		dispColCounter = printIsoMeta(isolates[i], dispColCounter, row, locInfo);


		dispColCounter = printIsoMeta(isolates[i], dispColCounter, row, islnInfo);

	}
}

function printIsolateCols(row, isolate, dispColCounter, colIsoId, isoInfo){

	var cell;

	for (var i = 0; i<isoInfo.length; i++){
		cell = row.insertCell(dispColCounter++);

		if (isoInfo[i].table_name == 'identifier'){
			cell.innerHTML = "<a href=\"/salmonella/isolate-" + isolate[parseInt(colIsoId)] + "-detail\">" +  isolate[parseInt(isoInfo[i].db_col)] + "</a>";
		}
		else if (isoInfo[i].table_name == serverStatus) {
			cell.innerHTML = ServerStatus[isolate[parseInt(isoInfo[i].db_col)]];
		}
		else if (isoInfo[i].table_name == assignStatus) {
			if (isolate[parseInt(isoInfo[i].db_col)]){
				cell.innerHTML = AssignStatus[isolate[parseInt(isoInfo[i].db_col)]];
			}
			else {
				cell.innerHTML = "-"
			}

		}
		else if (isoInfo[i].table_name == privacyStatus){
			cell.innerHTML = IsoPrivStatus[isolate[parseInt(isoInfo[i].db_col)]];
		}
		else{
			cell.innerHTML = isolate[parseInt(isoInfo[i].db_col)];
		}

	}

	return dispColCounter;
}
