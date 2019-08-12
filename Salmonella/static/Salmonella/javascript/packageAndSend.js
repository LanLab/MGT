// function downloadIsoAsCsv(searchVar)
// function getInitialPvData(url, pageNumToGet, projectId, orderBy, dir, csv)
// function doTheOrderBy(tableName, searchVar, tableId)
// function getOtherPage(pageNumToGet, searchVar,csv)
// function sortElemsAndSendProj(url, tblName, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln, projectId,csv)
// function sortElemsAndSend(url, tblName, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln,csv)
// function sortTheElemsAndSend(tblName, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln)
// function addToIsoDict(isoInfo, arr_iso, inputTd, tn, inputVal)
// function isPresent(apInfo, tn)
// function isOkAddCcToDict(ccInfo, arr_cc, inputTd, tn, inputVal)
// function isOkAddStDstToDict(apInfo, arr_ap, inputTd, tn, inputVal)
// function doTheAjaxOrderBy(url, order_by, dir)
// function doTheAjaxPlusSearch(url, arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc, pageNumToGet, orderBy, dir,csv)
// function getTheBoolsForDisp()
// function getInitialData(url, pageNumToGet, orderBy, dir, csv)

// function ajaxCall (url, data)
// function initialPvSuccess(response)

function ajaxCall(url, data, fnOnSuccess){
	$.ajax({
		type: 'POST',
		url: url,
		data: data,
		// dataType: 'html',
		success: function(response){
			// doSuccesfulThings();
			fnOnSuccess(response);
		},
		error: function (xhr, status, error) {
			xhr.abort();
		}
	});
}

function doNothingSuccess(response){
}
function doVisChngSuccess(response){
	$('#ajaxSearching').hide();
	document.getElementById("filterIsolates").removeAttribute("disabled");
	$('#isolateTable').html(response);
}
function isolateDetailSuccess(response){
	$('#ajaxSearching').hide();
	document.getElementById("searchSimStrains").removeAttribute("disabled");
	$('#isolateTable').html(response);
}
function downloadCsvSuccess(response){
	document.getElementById("csvDownload").style.display='';
	document.getElementById("fetchingcsv").style.display='none';

	var blob=new Blob([response]);
	var link=document.createElement('a');
	link.href=window.URL.createObjectURL(blob);
	link.download="MGT_isolate_data.txt";
	link.click();

}

// ================================================= //


// ORDER_BY IMPL.
var sort_forward = "Ascending";
var sort_reverse = "Descending";
function doTheOrderBy(tableName, searchVar, tableId){

	// 1. toggle a buttons class (so that its sort_ascending or descending direction).
	var dir = '';
	// console.log(document.getElementById(tableName).classList.contains(sort_forward));

	console.log("in the do the order by!");
	if (document.getElementById(tableName).classList.contains(sort_forward)){

		removeClassFromBtn(tableName, sort_forward);
		addClassToBtn(tableName, sort_reverse);
		dir = sort_reverse;
	}
	else if (document.getElementById(tableName).classList.contains(sort_reverse)){
		removeClassFromBtn(tableName, sort_reverse);
		addClassToBtn(tableName, sort_forward);
		dir = sort_forward;
	}
	else{
		dir = sort_forward;
		addClassToBtn(tableName, sort_forward);

	}


	var searchVar_str = searchVar.replace(/\'/g, '\"');

	// console.log("Table name " + tableName);
	// console.log("SearchVar");
	// console.log(JSON.parse(searchVar_str));
	// if ()
	var searchVar_js = JSON.parse(searchVar_str);

	// 2. Package the info, and
	searchVar_js[0]['dir'] = dir;
	searchVar_js[0]['orderBy'] = tableId + "." + tableName;

	// console.log(searchVar_js[0]);
	// console.log("waaaht?");

	console.log(searchVar_js);
	getOtherPage(searchVar[0].pageNumToGet, searchVar_js);
 	// getOtherPage(searchVar);
}

function doTheDownload(searchVar){
	document.getElementById("csvDownload").style.display='none';
	document.getElementById("fetchingcsv").style.display='';
	getOtherPage(null, searchVar, true);
}


// PAGINATION IMPL.

var url_initialIsolates = "initial-isolates";
var url_initialProjIsolates = "initial-projectIsolates"
var url_searchIsoList = "search-isolateList";
var url_searchIsoDetail = "search-isolateDetail";
var url_searchProjDetail = "search-projectDetail"; // url_allIsoPv

function getOtherPage(pageNumToGet, searchVar, isCsv){
	// console.log('isCsv ' + isCsv);

	var orderBy = null;
	var dir = null;

	if (searchVar[0].hasOwnProperty("orderBy")){
		orderBy = searchVar[0].orderBy;
		dir = searchVar[0].dir;
		// console.log (" yep they are being updated here!");
	}


	if (searchVar[0].hasOwnProperty("pageType")){
		if (searchVar[0].pageType == "pg_initialIsolates"){
			//console.log("pg_initialIsolates");
			getInitialData(url_initialIsolates, pageNumToGet, orderBy, dir, isCsv);

		}
		else if (searchVar[0].pageType == "pg_initialProjIsolates"){
			// console.log("pg_initialProjIsolates");
			getInitialProjData(url_initialProjIsolates, null, pageNumToGet, orderBy, dir, isCsv);
		}
		else if (searchVar[0].pageType == "pg_searchIsoList"){
			// console.log("pg_searchIsoList");
			sendToIsolateList(url_searchIsoList, null, null, null, null, null, null, pageNumToGet, orderBy, dir, isCsv);
		}
		else if (searchVar[0].pageType == "pg_searchIsoDetail"){
			console.log("pg_searchIsoDetail");
		 	// console.log("some thing else entirely!!");
			sendToIsolateDetail(url_searchIsoDetail, null,
				null, null, null, null, pageNumToGet, orderBy, dir, isCsv);
		}
		else if (searchVar[0].pageType == "pg_searchProjDetail"){
			// console.log("pg_searchProjDetail");
			sendProjSearchData(url_searchProjDetail, null, null, null, null, null, null, null, pageNumToGet, orderBy, dir, isCsv);
		}
	}
}






// THE +++ AJAX SEARCH TABLE COMPONENT

function sortElemsAndSend(url, tblName, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln){
	var searchVals = sortTheElemsAndSend(tblName, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln);

	if (!searchVals){
		return;
	}

	// 3. pass to ajax function.
	sendToIsolateList(url, searchVals.arr_ap, searchVals.arr_cc, searchVals.arr_epi, searchVals.arr_iso, searchVals.arr_isln, searchVals.arr_loc, null, null, null, null);
}


function sortTheElemsAndSend(tblName, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln){

	// console.log(projectId + " is project Id");

	var arr_iso = [];
	var arr_ap = [];
	var arr_cc = [];
	var arr_epi = [];
	var arr_loc = [];
	var arr_isln = [];

	// 1. get all tds of table, and
	// 2. go through each one and add to dict.
	var tableRows = document.getElementById(tblName).getElementsByTagName("tr");

	for (var i = 0; i <= tableRows.length-1; i++){
		var selectOpts = tableRows[i].getElementsByTagName("select")[0];
		var selectedTn = selectOpts[selectOpts.selectedIndex].value;


		var inputTd = null;
		var inputVal = null;

		var secondSBox = null;
		var secondVal = null;

		if (selectedTn == serverStatus){

			inputTd = $(selBox).closest('tr')[0];

			var selBox = tableRows[i].getElementsByClassName("srvrStatusSel")[0];

			inputVal = selBox.options[selBox.selectedIndex].value;

		}
		else if (selectedTn == assignStatus){
			console.log("now here???")
			inputTd = $(selBox).closest('tr')[0];

			var selBox = tableRows[i].getElementsByClassName("assignStatusSel")[0];

			inputVal = selBox.options[selBox.selectedIndex].value;

		}
		else if (selectedTn == privacyStatus){
			inputTd = $(selBox).closest('tr')[0];

			var selBox = tableRows[i].getElementsByClassName("privStatusSel")[0];

			inputVal = selBox.options[selBox.selectedIndex].value;
		}
		else if (selectedTn == islnYear || selectedTn == islnDate){
			inputTd = tableRows[i].getElementsByClassName("startTime")[0];
			inputVal = inputTd.value;

			secondSBox = tableRows[i].getElementsByClassName("endTime")[0];
			secondVal = secondSBox.value;

		}
		else {
			inputTd = tableRows[i].getElementsByClassName("txtInpt")[0];
			inputVal = inputTd.value;
		}


		// if inputVal is empty or contians not[a-zA-Z0-9.] then return.
		if(selectedTn == islnDate){
			if(!isOkDate(inputVal)){
				inputTd.classList.add("incorrect");
				return;
			}
			if(!isOkDate(secondVal)){
				secondSBox.classList.add("incorrect");
				return;
			}
			if(inputVal > secondVal){
				inputTd.classList.add("incorrect");
				secondSBox.classList.add("incorrect");
				return;
			}

		}
		else if(selectedTn == locPostcode){
			if (!isOkNum(inputVal)){
				inputTd.classList.add("incorrect");
				return;
			}
		}
		else if(!isOkValBasicCheck(inputVal)){
			inputTd.classList.add("incorrect");
			return;
		}
		if (selectedTn == islnYear){
			if (!isOkNum(inputVal)){
				inputTd.classList.add("incorrect");
				return;
			}
			if (!isOkNum(secondVal)){
				secondSBox.classList.add("incorrect");
				return;
			}
			if(parseInt(inputVal) > parseInt(secondVal)){
				inputTd.classList.add("incorrect");
				secondSBox.classList.add("incorrect");
				return;
			}
		}



		if (selectedTn == serverStatus || selectedTn == privacyStatus || selectedTn == assignStatus) {
		}
		else if (selectedTn == islnYear || selectedTn == islnDate){
			inputTd.classList.remove("incorrect");
			secondSBox.classList.remove("incorrect");
		}
		else{
			inputTd.classList.remove("incorrect");
		}


		// add value to appropriate dict. if returns false (means something not ok, and red highlight and return).


		if (isPresent(apInfo, selectedTn)) {
			retVal = isOkAddStDstToDict(apInfo, arr_ap, inputTd, selectedTn, inputVal);
			if (retVal == false){
				return;
			}
			arr_ap = retVal;
		}
		else if (isPresent(ccInfo, selectedTn)) {
			retVal = isOkAddCcToDict(ccInfo, arr_cc, inputTd, selectedTn, inputVal);
			if (retVal == false){
				return;
			}
			arr_cc = retVal;
		}
		else if (isPresent(epiInfo, selectedTn)){
			retVal = isOkAddCcToDict(epiInfo, arr_epi, inputTd, selectedTn, inputVal);
			if(retVal == false){
				return;
			}
			epi_cc = retVal;
		}
		else if (isPresent(isoInfo, selectedTn)){
			// add directly
			arr_iso = addToIsoDict(isoInfo, arr_iso, inputTd, selectedTn, inputVal);
		}
		else if (isPresent(isoMIsln, selectedTn)){
			// also add directly
			if (selectedTn == islnYear || selectedTn == islnDate){
				arr_isln = addToIsoDict(isoMIsln, arr_isln, inputTd, selectedTn+"__gte", inputVal);
				arr_isln = addToIsoDict(isoMIsln, arr_isln, secondSBox, selectedTn+"__lte", secondVal);
			}
			else{
				arr_isln = addToIsoDict(isoMIsln, arr_isln, inputTd, selectedTn, inputVal);
			}

		}
		else if (isPresent(isoMLoc, selectedTn)){
			// also add directly
			arr_loc = addToIsoDict(isoMLoc, arr_loc, inputTd, selectedTn, inputVal);
		}
	}

	$('#ajaxSearching').show();
	document.getElementById("filterIsolates").disabled = true;



	return {
		arr_iso: arr_iso,
		arr_ap: arr_ap,
		arr_cc: arr_cc,
		arr_epi: arr_epi,
		arr_loc: arr_loc,
		arr_isln: arr_isln
	};
}


function addToIsoDict(isoInfo, arr_iso, inputTd, tn, inputVal){

	var jsonObj = {};
	jsonObj[tn] = inputVal;
	arr_iso.push(jsonObj);

	return arr_iso;
}


function isPresent(apInfo, tn){

	for(var i=0; i<apInfo.length; i++){
		if (apInfo[i].table_name == tn){
			return true;
		}
	}
	return false;
}


function isOkAddCcToDict(ccInfo, arr_cc, inputTd, tn, inputVal){
	if (isOkNum(inputVal) == false){
		inputTd.classList.add("incorrect");
		return false;
	}

	var jsonObj = {};
	jsonObj[tn] = inputVal;
	arr_cc.push(jsonObj);

	return arr_cc;
}

function isOkAddStDstToDict(apInfo, arr_ap, inputTd, tn, inputVal){
	// check value is in apInfo


	var arr = inputVal.split('\.');

	if (arr.length > 2){ // more than 1 dot is present.
		inputTd.classList.add("incorrect");
		return false;
	}

	if (isOkNum(arr[0]) == false || (arr.length == 2 && isOkNum(arr[1]) == false)){ // check all values are numeric
		inputTd.classList.add("incorrect");
		return false;
	}

	// add to search array for ajax

	var jsonObj = {};
	jsonObj[tn + "_st"] = arr[0];
	arr_ap.push(jsonObj);

	if (arr.length == 2){
		var jsonObj = {};
		jsonObj[tn + "_dst"] = arr[1];
		arr_ap.push(jsonObj);
	}


	return arr_ap;
}
// AJAX: order_by


// AJAX: SEARCH

function getTheBoolsForDisp(){

	var isAp = !document.getElementById('ccView').classList.contains('is-primary');


	var isDst = false;
	if ($("#btn_toggleDst")){
		isDst = $("#btn_toggleDst").hasClass('btn-outline-success');
	}


	var isMgtColor = true;
	if ($("#btn_toggleCol")){
		isMgtColor = !$("#btn_toggleCol").hasClass('btn-outline-secondary');
	}

	return {
		isAp: isAp,
		isDst: isDst,
		isMgtColor: isMgtColor
	};
}




/*
function doTheAjaxOrderBy(url, order_by, dir){

	var data = {
		'order_by': order_by,
		'dir': dir,
		'isAp': document.getElementById('apView').classList.contains('is-primary'),
		// 'csrfmiddlewaretoken': '{{ csrf_token }}',
	};

	ajaxCall(url, data, doNothingSuccess);
}
*/

// ########################



// AJAX: Get initial data (on page load).
function getInitialData(url, pageNumToGet, orderBy, dir, isCsv){
	// console.log("here!");
	var theBools = getTheBoolsForDisp();
	var data = {
		'pageNumToGet': pageNumToGet,
		'orderBy': orderBy,
		'dir': dir,
		'isAp': theBools.isAp,
		'isDst': theBools.isDst,
		'isMgtColor': theBools.isMgtColor,
		'isCsv': isCsv,
	};

	if (isCsv == true){
		ajaxCall(url, data, downloadCsvSuccess);
	}
	else{
		ajaxCall(url, data, doVisChngSuccess);
	}

}

function getInitialProjData(url, projectId, pageNumToGet, orderBy, dir, isCsv){

	var theBools = getTheBoolsForDisp();
	var data = {
		'projectId': JSON.stringify(projectId),
		'pageNumToGet': pageNumToGet,
		'orderBy': orderBy,
		'dir': dir,
		'isAp': theBools.isAp,
		'isDst': theBools.isDst,
		'isMgtColor': theBools.isMgtColor,
		'isCsv': isCsv,
	};

	if (isCsv == true){
		ajaxCall (url, data, downloadCsvSuccess);
	}
	else{
		ajaxCall(url, data, doVisChngSuccess);
	}


}

// THE +++ AJAX SEARCH TABLE COMPONENT
function searchInProj(url, tblName, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln, projectId){

	var searchVals = sortTheElemsAndSend(tblName, isoInfo, apInfo, ccInfo, epiInfo, isoMLoc, isoMIsln);

	// add project_id to arr_iso
	if (!searchVals){
		return;
	}

	// searchVals.arr_iso.push({"project": projectId});

	// 3. pass to ajax function.
	sendProjSearchData(url, projectId, searchVals.arr_ap, searchVals.arr_cc, searchVals.arr_epi, searchVals.arr_iso, searchVals.arr_isln, searchVals.arr_loc, null, null, null, null);
}

function sendToIsolateList(url, arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc, pageNumToGet, orderBy, dir, isCsv){

	var theBools = getTheBoolsForDisp();
	var data= {
		'arrAp': JSON.stringify(arr_ap),
		'arrCc': JSON.stringify(arr_cc),
		'arrEpi': JSON.stringify(arr_epi),
		'arrIso': JSON.stringify(arr_iso),
		'arrIsln': JSON.stringify(arr_isln),
		'arrLoc': JSON.stringify(arr_loc),
		'isAp': theBools.isAp,
		'isDst': theBools.isDst,
		'isMgtColor': theBools.isMgtColor,
		'pageNumToGet': pageNumToGet,
		'orderBy': orderBy,
		'dir': dir,
		'isCsv':isCsv,
	};

	if (isCsv == true){
		ajaxCall(url, data, downloadCsvSuccess);
	}
	else{
		ajaxCall(url, data, doVisChngSuccess);
	}

}




function sendProjSearchData(url, projectId, arr_ap, arr_cc, arr_epi, arr_iso, arr_isln, arr_loc, pageNumToGet, orderBy, dir, isCsv){

	var theBools = getTheBoolsForDisp();
	var data= {
		'arrAp': JSON.stringify(arr_ap),
		'arrCc': JSON.stringify(arr_cc),
		'arrEpi': JSON.stringify(arr_epi),
		'arrIso': JSON.stringify(arr_iso),
		'arrIsln': JSON.stringify(arr_isln),
		'arrLoc': JSON.stringify(arr_loc),
		'projectId': JSON.stringify(projectId),
		'isAp': theBools.isAp,
		'isDst': theBools.isDst,
		'isMgtColor': theBools.isMgtColor,
		'pageNumToGet': pageNumToGet,
		'orderBy': orderBy,
		'dir': dir,
		'isCsv': isCsv,
	};

	if (isCsv == true){
		ajaxCall(url, data, downloadCsvSuccess);
	}
	else{
		ajaxCall(url, data, doVisChngSuccess);
	}

}
