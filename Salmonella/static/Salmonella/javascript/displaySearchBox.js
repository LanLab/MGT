// SEARCH - ENTER BUTTON

function bindEnterToSearch(btnId){
	$(document).keypress(function(e){
		if (e.which == 13){ // 13 == enter key
			document.getElementById(btnId).click();
		}
	});
}



// TOGGLE DST/MGT_COLOR


function toggleDst(btnId, isDstBtn, isolates, colIsoId, isoInfo, apInfo, ccInfo, mgtInfo, epiInfo, locInfo, islnInfo, searchVar){
	var btn = $("#" + btnId);
	var isShowCol = null;
	var isShowDst = null;

	if (btn.hasClass('btn-outline-success')){
		btn.removeClass('btn-outline-success').addClass('btn-outline-secondary');
		if (isDstBtn == true){
			isShowDst = false;
		}
		else{
			isShowCol = false;
		}

	}
	else if (btn.hasClass('btn-outline-secondary')){
		btn.removeClass('btn-outline-secondary').addClass('btn-outline-success');
		if (isDstBtn == true){
			isShowDst = true;
		}
		else{
			isShowCol = true;
		}
	}


	if ($("#apView").hasClass('is-primary')){
		console.log("call the doApLayout fn.");
		if (isDstBtn == true){
			isShowCol = $("#btn_toggleCol").hasClass('btn-outline-success');
			doApLayout(isolates, colIsoId, isoInfo, apInfo, mgtInfo, epiInfo, locInfo, islnInfo, searchVar, isShowCol, isShowDst);
		}
		else{
			isShowDst = $("#btn_toggleDst").hasClass('btn-outline-success')
			doApLayout(isolates, colIsoId, isoInfo, apInfo, mgtInfo, epiInfo, locInfo, islnInfo, searchVar, isShowCol, isShowDst);
		}
	}
	else{
		if (isDstBtn == false){ // dont need to replot for dst
			console.log("call the doCcLayout fn.")
			doCcLayout(isolates, colIsoId, isoInfo, ccInfo, mgtInfo, epiInfo, locInfo, islnInfo, searchVar, isShowCol);
		}
	}

}


// [CC|EPI] MERGE INFO DISPLAY

function printCcMergeInfo(mergedInfo, ccInfo, epiInfo){
	mergedInfo = mergedInfo.replace(/\'/g, "\"");

	var mergedInfo_prs = JSON.parse(mergedInfo);
	var ccInfo_p = JSON.parse(ccInfo);
	var epiInfo_p = JSON.parse(epiInfo);

	var tableStr = "<div class=\"box\"> <b> Merged clonal and epidemeology clusters: </b> <table class=\"table is-bordered\">";

	var isAnyMerged = false;

	for (var tn in mergedInfo_prs){
		if (mergedInfo_prs.hasOwnProperty(tn)){
			if (mergedInfo_prs[tn].length > 1){

				isAnyMerged = true;
				var dispName = getDisplayName(tn, ccInfo_p, epiInfo_p);

				tableStr = tableStr + "<tr> <td> " + dispName + " </td> <td>";
				for (var i=0; i < mergedInfo_prs[tn].length; i++){
					if (i != 0){
						tableStr = tableStr + ", ";
					}
					tableStr = tableStr + mergedInfo_prs[tn][i] ;
				}
				tableStr = tableStr + "</td> </tr>";
			}
		}
	}
 	tableStr = tableStr + "</table> </box>";

	if (isAnyMerged == true){
		document.getElementById('mergedIdsInfo').insertAdjacentHTML('beforeend', tableStr);
	}

	// .append(tableStr);
}



function getDisplayName(tn, ccInfo, epiInfo){

	for (var i=0; i<ccInfo.length; i++){
		if (ccInfo[i].table_name == tn){
			// console.log("Display name: " + ccInfo[i].display_name);
			return ccInfo[i].display_name;
		}
	}

	for (var i=0; i<epiInfo.length; i++){
		if (epiInfo[i].table_name == tn){
			// console.log("Display name: " + ccInfo[i].display_name);
			return epiInfo[i].display_name;
		}
	}
}



function addRowFromBtn(addBtn, isoInfo, apInfo, ccInfo, epiInfo, isoMIsln, isoMLoc){

	var tbl = addBtn.parentNode.parentNode.parentNode;
	addRowToTbl(tbl, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln);
}
function addRowToTbl(tbl, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln){

	var innerStr = "<tr>";

	// tr:select
	innerStr = innerStr + "<td> <select onchange=\"javascript:checkCol2(this);\">" + printSelectCcStr(isoInfo, "Isolate", null) + printSelectApStr(apInfo, "Sequence types", "ST") +  printSelectCcStr(ccInfo, "Clonal clusters", "CC") + printSelectCcStr(epiInfo, "Outbreak clusters") +  printSelectCcStr(isoMLoc, "Location") + printSelectCcStr(isoMIsln, "Isolation") + " </select> </td>";

	// tr:input box
	innerStr = innerStr + "<td> <input class=\"txtInpt\" type=\"text\"/> </td>";

	// tr:"+" and pass data required for recursive call
	innerStr = innerStr + "<td> <button onclick='javascript:addRowFromBtn(this, " + JSON.stringify(isoInfo) + ", " + JSON.stringify(apInfo) + ", " + JSON.stringify(ccInfo) + ", " + JSON.stringify(epiInfo) + ", " + JSON.stringify(isoMIsln) + ", " + JSON.stringify(isoMLoc) + ");'> + </button> </td>";

	// "-"
	innerStr = innerStr + "<td> <button onclick=\"javascript:delCurrRow(this);\"> - </button> </td>";
	innerStr = innerStr + "</tr>";

	var newRow = tbl.insertRow();
	newRow.innerHTML = innerStr;

}


function delCurrRow(delBtn){

	var row = delBtn.parentNode.parentNode;
	row.parentNode.removeChild(row);
}


// SEARCH BOX DISPLAY IMPL.
serverStatus = "server_status";
serverStatusStr = [{option: "Uploaded reads", value:'U'}, {option:"Uploaded alleles", value: 'V'}, {option: "In queue", value:'A'}, {option: "Running reads to alleles", value:'R'}, {option: "Running alleles to MGT", value:'S'},  {option: "Holding", value:'H'}, {option: "Complete", value:'C'}, {option: "To download NCBI reads", value:'D'}];

assignStatus = "assignment_status"
assignStatusStr = [{option:"Assigned", value:'A'}, {option:"Failed: contamination", value:'F'}, {option:"Failed: genome quality", value:'G'}, {option:"Failed: serovar incompatibility", value:'S'}, {option:"Error: other", value:'E'}]

privacyStatus = "privacy_status";
privacyStatusStr = [{option: "Public", value:"PU"}, {option: "Private", value:"PV"}];

islnYear = "year";
islnDate = "date";
locPostcode = "postcode";

function checkCol2(selObj){
	// console.log("now go thru, check and update where necessary");
	// console.log(selObj.value);
	var tr = $(selObj).closest('tr');

	if (selObj.value == serverStatus){
		// console.log(tr[0].cells[1].innerHTML);
		// console.log("change to sel box");

		var selStr = "<select class=\"srvrStatusSel\">";
		for (var i=0; i<serverStatusStr.length; i++){
			selStr = selStr + " <option value=\"" + serverStatusStr[i].value + "\"> " + serverStatusStr[i].option + "</option>";
		}
		selStr = selStr + "</select>";
		tr[0].cells[1].innerHTML = selStr;
	}
	else if (selObj.value == assignStatus){
		var selStr = "<select class=\"assignStatusSel\">";
		for (var i=0; i<assignStatusStr.length; i++){
			selStr = selStr + " <option value=\"" + assignStatusStr[i].value + "\"> " + assignStatusStr[i].option + "</option>";
		}
		selStr = selStr + "</select>";
		tr[0].cells[1].innerHTML = selStr;

	}
	else if (selObj.value == privacyStatus) {
		var selStr = "<select class=\"privStatusSel\">";
		for (var i=0; i<privacyStatusStr.length; i++){
			selStr = selStr + " <option value=\"" + privacyStatusStr[i].value + "\"> " + privacyStatusStr[i].option + "</option>";
		}
		selStr = selStr + "</select>";
		tr[0].cells[1].innerHTML = selStr;
	}
	else if (selObj.value == islnYear) {
		tr[0].cells[1].innerHTML = "Start year: <input class=\"startTime\" type=\"text\" size=4> &nbsp;&nbsp; End year: <input class=\"endTime\" type=\"text\" size=4>";
	}
	else if (selObj.value == islnDate){
		tr[0].cells[1].innerHTML = "Start date: <input type=\"date\" class=\"startTime\"> &nbsp;&nbsp; End date: <input type=\"date\" class=\"endTime\">";
	}
	else {
		tr[0].cells[1].innerHTML = "<input class=\"txtInpt\" type=\"text\">";
	}


	// console.log(selObj.value)
}




function printSelectApStr(apInfo, groupStr, typeDispStr){

	var str = "<optgroup label='" + groupStr + "'>";

	for  (var i = 0; i< apInfo.length; i++){
		str = str + "<option value='" + apInfo[i].table_name + "'>";
		str = str + apInfo[i].scheme__display_name;
		if (typeDispStr){
			str = str + " - " + typeDispStr;
		}
		str = str + "</option>";
	}
	str = str + "</optgroup>";

	return str;
}

function printSelectCcStr(apInfo, groupStr, typeDispStr){

	var str = "<optgroup label='" + groupStr + "'>";

	for  (var i = 0; i< apInfo.length; i++){

		str = str + "<option value='" + apInfo[i].table_name + "'>";
		str = str + apInfo[i].display_name;

		if (typeDispStr){
			str = str + " - " + typeDispStr;
		}

		str = str + "</option>";


	}
	str = str + "</optgroup>";

	return str;
}
