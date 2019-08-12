
var rowApId = "rowAp";
var rowCcId = "rowCc";
var rowEpiId = "rowEpi";

var selTdClassName = "theSel";
var hoverTdClassName = "theHl";

var table_loc = "tblLocation";
var table_isln = "tblIsolation";
var table_proj = "tblProject";

function rowLayoutOfApsAndCcs(rowName, jsonApHeader, jsonIsoHgtInfo, isAp){
	var dispColCounter = 0;
	var rowAp = document.getElementById(rowName);

	cell = rowAp.insertCell(dispColCounter++);
	cell.innerHTML = "";

	for (var i=0; i < jsonApHeader.length; i++){

		cell = rowAp.insertCell(dispColCounter++);

		if (isAp == true){
			cell.innerHTML = theApVal(jsonIsoHgtInfo[0].fields, jsonApHeader[i].table_name); // + "|" + jsonIsoHgtInfo[0].fields[jsonApHeader[i].table_name];
		}
		else{
			cell.innerHTML = theCcVal(jsonIsoHgtInfo[0].fields, jsonApHeader[i].table_name);
		}

		cell.id = jsonApHeader[i].table_name;

		cell.setAttribute("onmouseenter", 'doHighlighting("' + rowName + '", ' + i + ', "'+ hoverTdClassName + '");');
		cell.setAttribute("onmouseleave", 'clearHighlighting("' + rowName + '", ' + i + ', "' + hoverTdClassName + '");');
		cell.setAttribute("onclick", 'toggleHighlighting("' + rowName + '", ' + i + ', "' + selTdClassName + '");');
	}

	if (isAp == true){
		cell = rowAp.insertCell(dispColCounter++);
		cell.innerHTML = '<input type="checkbox" id="isPerfectSt"> (only include perfect STs)';
	}
}


function clearHlSelection(className){
	clearAllHighlighting(rowApId, className);
	clearAllHighlighting(rowCcId, className);
	clearAllHighlighting(rowEpiId, className);
	clearAllHighlightingInTbl(table_loc, className);
	clearAllHighlightingInTbl(table_isln, className);
	document.getElementById("isPerfectSt").checked = false;

}

function clearAllHighlightingInTbl(tblName, className){
	// console.log(tblName);
	var cells = document.getElementById(tblName).getElementsByTagName("td");

	// console.log(cells);
	for (var i=0; i < cells.length; i++){
		cells[i].classList.remove(className);
	}

}

function doSimHl(elemId, className){
	var cell = document.getElementById(elemId).classList.add(className);
}

function removeSimHl(elemId, className){
	var cell = document.getElementById(elemId).classList.remove(className);
}

function doSmpToggle(elemId, className){
	var cell = document.getElementById(elemId);
	if(cell.classList.contains(className)){
		cell.classList.remove(className);
	}
	else {
		cell.classList.add(className);
	}
}

function doHighlighting(rowName, colNum, className){
	var cells = document.getElementById(rowName).getElementsByTagName("td");

	cells[colNum+1].classList.add(className);
}

function clearAllHighlighting(rowName, className){
	var cells = document.getElementById(rowName).getElementsByTagName("td");



	for (var i = 1; i < cells.length; i++){
		// console.log(cells[i]);
		cells[i].classList.remove(className)
	}

}
function toggleHighlighting(rowName, colNum, className){
	// console.log(rowName);
	// console.log(colNum);
	var cells = document.getElementById(rowName).getElementsByTagName("td");

	if (cells[colNum+1].classList.contains(className)){
		cells[colNum+1].classList.remove(className);
	}
	else {
		cells[colNum+1].classList.add(className);
	}

}

function clearHighlighting(rowName, colNum, className){
	var cells = document.getElementById(rowName).getElementsByTagName("td");

	cells[colNum+1].classList.remove(className);

}

/* Getting values of the individual cells */
function theApVal(isoHgtVals, fieldName){

	if (isoHgtVals[fieldName] == null){
		return "-";
	}
	else {
		var retStr = isoHgtVals[fieldName+"_st"];

		if (isoHgtVals[fieldName+"_dst"] != 0){
			retStr = retStr + "." + isoHgtVals[fieldName+"_dst"];
		}
	}

	return (retStr);
}

function theCcVal(isoHgtVals, fieldName){

	if (isoHgtVals[fieldName] == null){
		return "-";
	}

	return (isoHgtVals[fieldName]);
}
