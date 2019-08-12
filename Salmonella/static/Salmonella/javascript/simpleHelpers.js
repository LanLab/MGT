function deactivateTheModal(modalId){
	var modalObj = document.getElementById(modalId);

	modalObj.classList.remove("is-active");
}

function activateTheModal(modalId){
	var modalObj = document.getElementById(modalId);

	modalObj.classList.add("is-active");
}

function isOkDate(val){
	if (val && val.match(/^[0-9]{4}-[0-9]{2}-[0-9{2}]+$/)){
		return true;
	}
	return false;
}

function isOkNum(val){

	if (val && val.match(/^[0-9]+$/)){
		return true;
	}
	return false;
}

function isOkValBasicCheck(val){

	if (val && val.match(/^[a-zA-Z0-9\.\s]+$/)){
		return true;
	}

	return false;
}


function isEmpOrOnlyWD(txtBoxId){
	var val = document.getElementById(txtBoxId).value;

	if (!val || !val.match(/^[a-zA-Z0-9\.]+$/)){
		makeIncorrect(txtBoxId);
		return true;
	}
	else{
		makeCorrect(txtBoxId);
		return false;
	}
}



function isEmpOrNotNumAndMakeInc(txtBoxId){
	var val = document.getElementById(txtBoxId).value;

	if (!val || !val.match(/^\d+$/)){
		makeIncorrect(txtBoxId);
		return true;
	}
	else{
		makeCorrect(txtBoxId);
		return false;
	}
}


function isPresAndNotNumMakeInc(txtBoxId){
	var val = document.getElementById(txtBoxId).value;

	if (val && !val.match(/^\d+$/)){
		makeIncorrect(txtBoxId);
		return true;
	}
	else if (val && val.match(/^\d+$/)){
		makeCorrect(txtBoxId);
		return false;
	}
	else if (!val){
		makeCorrect(txtBoxId);
		return false;
	}
}

function makeIncorrect(elementId){
	document.getElementById(elementId).className = document.getElementById(elementId).className + " incorrect";
}

function makeCorrect(elementId){
	document.getElementById(elementId).className = document.getElementById(elementId).className.replace(" incorrect", "");
}

function addClassToBtn(btnId, className){
	document.getElementById(btnId).classList.add(className);
}

function removeClassFromBtn(btnId, className){
	document.getElementById(btnId).classList.remove(className);
}

function hideDiv(divName, viewName){
	document.getElementById(divName).style.display='none';
	document.getElementById(viewName).classList.remove("active");
}

function showDiv(divName, viewName){
		document.getElementById(divName).style.display='';
		document.getElementById(viewName).classList.add("active");
}
