function passToServer(details, location){
	var xhr = new XMLHttpRequest();
	var url = "http://127.0.0.1:5000/user/stackoverflow" + location;
	//var url = "https://saumya-cse591.herokuapp.com/user/stackoverflow" + location;
	console.log(url);
	xhr.open("POST", url, true);
	console.log(details);
	xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.onreadystatechange = function() {//Call a function when the state changes.
			if(xhr.readyState == 4 && xhr.status == 200) {
    		console.log(xhr.responseText);
		}
	}
	xhr.send(details);
}

function getDate(){
	var x = new Date;
	var timestamp = x.getFullYear() + "-"  + (x.getMonth() - 1) + "-" + x.getDate() + " " + x.getHours() + ":" + x.getMinutes() + ":" + x.getSeconds();
	return timestamp;
}

function addClickEvent(domElement){
	domElement.addEventListener("click", function(event){
		var timestamp = encodeURIComponent(getDate());
		var clickDetails = "url=" + encodeURIComponent(document.URL)+"&action=click&targetClass=" + event.target.className + "&timeStamp=" + timestamp;
		console.log(clickDetails);
		passToServer(clickDetails, "/clicks");
	});
}

function addScrollEvent(domElement){
	var timer = null;
	domElement.addEventListener("scroll", function(){
		if (timer != null){
			clearTimeout(timer);
		}
		timer = setTimeout(function(){
			console.log(domElement.scrollingElement.scrollTop);
			var timestamp = encodeURIComponent(getDate());
			var ratio = domElement.scrollingElement.scrollTop/(domElement.documentElement.scrollHeight - domElement.documentElement.clientHeight);
			var scrollDetails = "url=" + encodeURIComponent(document.URL) + "&action=scroll&scrollRatio=" + ratio + "&timeStamp=" + timestamp;
			console.log(scrollDetails);
			passToServer(scrollDetails, "/scroll");
		}, 500)
	})
}

function idleTimer(){
	var t;
	document.onmousemove = resetTimer;
	document.onkeypress = resetTimer;
	function resetTimer(){
		console.log("Reset Timer");
		clearTimeout(t);
		t = setTimeout(function(){
			var timestamp = encodeURIComponent(getDate());
			var docURL = encodeURIComponent(document.URL);
			var idleTimeDetails = "url=" + docURL + "&action=idle&timeStamp=" + timestamp;
			console.log(idleTimeDetails);
			passToServer(idleTimeDetails, "/idleTime");
		}, 20000)
	}
}

function getTags(domElement){
	var timestamp = encodeURIComponent(getDate());
	var tagList = domElement.getElementsByClassName('post-tag js-gps-track');
	var tagString = "";
	for(var i = 0; i < tagList.length; i++){
		tagString = tagString + tagList[i].text;
		if (i < tagList.length - 1){
			tagString = tagString + "+";
		}
	}
	var docURL = encodeURIComponent(document.URL);
	tagString = encodeURIComponent(tagString)
	tagsDetails = "url=" + docURL + "&tags=" + tagString + "&timeStamp=" + timestamp;
	passToServer(tagsDetails, "/tags");
}


function searchField(){
	var timestamp = encodeURIComponent(getDate());
	var searchBox = document.getElementsByClassName('f-input js-search-field');
	searchBox[0].onclick = function(){
		docURL = encodeURIComponent(document.URL);
		var searchBoxDetails = "url=" + docURL + "&action=search&timeStamp=" + timestamp;  
		passToServer(searchBoxDetails, "/searchBox");
	}
}

function addCopyEvent(domElement){
	domElement.addEventListener('copy', function(e){
		var timestamp = encodeURIComponent(getDate());
		var docURL = encodeURIComponent(document.URL);
		var elementClass = encodeURIComponent(e.srcElement.className);
		var elementText = encodeURIComponent(e.srcElement.textContent);
		var copiedElementDetails = "url=" + docURL + "&action=copy&elementClass=" + elementClass + "&elementText=" + elementText + "&timeStamp=" + timestamp;
		console.log(copiedElementDetails);
		passToServer(copiedElementDetails, "/copiedElement");
	})

}

function addPostEvent(domElement){
	submitButton = domElement.getElementById('submit-button');
	submitButton.onclick = function(){
		var timestamp = encodeURIComponent(getDate());
		inputText = domElement.getElementsById('wmd-input');
		if (inputText.value != ''){
			var docURL = encodeURIComponent(document.URL);
			var submitElementDetails = "url=" + docURL + "&action=submit&timeStamp=" + timestamp;
			passToServer(submitElementDetails, "/submitButton");
		}
	}
}

chrome.runtime.sendMessage({todo:"showPageAction"});


console.log("Here!");
var anchorElements = document.getElementsByTagName('a');
for(var i = 0; i < anchorElements.length; i++){
	addClickEvent(anchorElements[i]);
}
addScrollEvent(document);
addCopyEvent(document);
addPostEvent(document);
idleTimer();
getTags(document);
searchField();