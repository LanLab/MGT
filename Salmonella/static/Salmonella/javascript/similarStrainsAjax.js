

function isolateDetailSearch(jsonIsoHgtInfo, url){
	$('#ajaxSearching').show();
	document.getElementById("searchSimStrains").disabled = true;

	var apSearchMap = {};
	var ccEpiSearchMap = {};
	var locMap = {};
	var islnMap = {};
	var projMap = {};

	// Aps
	if (document.getElementById(rowApId)){
		var tds = document.getElementById(rowApId).getElementsByTagName("td");
		apSearchMap = addStValsToMap(tds, apSearchMap, jsonIsoHgtInfo, document.getElementById("isPerfectSt").checked);
		console.log(apSearchMap);
		console.log("That twas the ap search map");
	}

	// Ccs
	if (document.getElementById(rowCcId)){
		var tds = document.getElementById(rowCcId).getElementsByTagName("td");
		ccEpiSearchMap = addCcValsToMap(tds, ccEpiSearchMap, jsonIsoHgtInfo);
	}

	// Epis
	if (document.getElementById(rowEpiId)){
		var tds = document.getElementById(rowEpiId).getElementsByTagName("td");
		ccEpiSearchMap = addCcValsToMap(tds, ccEpiSearchMap, jsonIsoHgtInfo);
	}

	// Location
	if (document.getElementById(table_loc)){
		var tds = document.getElementById(table_loc).getElementsByClassName("theSel");
		locMap = addMdValsToMap(tds, locMap);
	}


	console.log(locMap);
	if(document.getElementById(table_isln)){
		var tds = document.getElementById(table_isln).getElementsByClassName("theSel");
		islnMap = addMdValsToMap(tds, islnMap);
	}

	if(document.getElementById(table_proj)){
		var tds = document.getElementById(table_proj).getElementsByClassName("theSel");
		projMap = addMdValsToMap(tds, projMap);
	}

	//console.log(tds);
	// Isoln

	/*
	if (tds.length == 0){
		console.log("nothing here!");
		return;
	}*/

	//console.log(allSearchMap);


	if (Object.keys(apSearchMap).length == 0 && Object.keys(ccEpiSearchMap).length == 0 && Object.keys(locMap).length == 0 && Object.keys(islnMap).length == 0 && Object.keys(projMap).length == 0){
		console.log("nothing to search");
		$('#ajaxSearching').hide();
		document.getElementById("searchSimStrains").removeAttribute("disabled");
		return;
	}

	sendToIsolateDetail(url, apSearchMap, ccEpiSearchMap, locMap, islnMap, projMap, null, null, null, null);

}

function addMdValsToMap(tds, locMap){

	for (var i=0; i<tds.length; i++){
		// console.log(tds[i].id);
		// console.log("yolo! " + tds[i].innerText);
		locMap[tds[i].id] = tds[i].innerText;
	}

	return locMap;
}


function addStValsToMap(tds, allSearchMap, jsonIsoHgtInfo, isPerfectSt){

	for (var i = 0; i < tds.length; i++){
		if (tds[i].classList.contains(selTdClassName)){
			console.log(tds[i].id + "_st");

			var tn = tds[i].id + "_st";

			allSearchMap[tn] = jsonIsoHgtInfo[0].fields[tn];

			if (isPerfectSt == true){

				tn = tds[i].id + "_dst";

				allSearchMap[tn] = 0;

			}

		}
	}
	return (allSearchMap);
}

function addCcValsToMap(tds, allSearchMap, jsonIsoHgtInfo){

	for (var i = 0; i < tds.length; i++){
		if (tds[i].classList.contains(selTdClassName)){
			allSearchMap[tds[i].id] = jsonIsoHgtInfo[0].fields[tds[i].id];
		}
	}
	return (allSearchMap);
}


function sendToIsolateDetail(url, apSearchMap, ccEpiSearchMap, locMap, islnMap, projMap, pageNumToGet, orderBy, dir, isCsv){

	var theBools = getTheBoolsForDisp();
	var data = {
		'json_apSearchTerms': JSON.stringify(apSearchMap),
		'json_ccEpiSearchTerms': JSON.stringify(ccEpiSearchMap),
		'json_location': JSON.stringify(locMap),
		'json_isolation': JSON.stringify(islnMap),
		'json_project': JSON.stringify(projMap),
		'isAp': theBools.isAp,
		'isDst': theBools.isDst,
		'isMgtColor': theBools.isMgtColor,
		'pageNumToGet': pageNumToGet,
		'csrfmiddlewaretoken': '{{ csrf_token }}',
		'orderBy': orderBy,
		'dir': dir,
		'isCsv':isCsv,
	};

	if(isCsv == true){
		ajaxCall(url, data, downloadCsvSuccess);
	}
	else{
		ajaxCall(url, data, isolateDetailSuccess);
	}

}
