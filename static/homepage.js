/*
    homepage.js
    Sonia Moreno 

    Search box and buttons for homepage.html
 */

function SearchButton() {
    /*
    Called when search button is clicked
    Resets screan of messages and tables
    Makes new request to api
    Calls function getCoursesCallback()
    */
    var search = document.getElementById('search');
    var searchedBy = document.getElementById('searchBy'); //default is name
    //reset table body
    var tableBody = "";
    var resultsTableElement = document.getElementById('results_table');
    resultsTableElement.innerHTML = tableBody;
    browsed.innerHTML = "";
    var url = api_base_url + 'courses/';

    if(search.value!='') {
        url = url + searchBy.value +'/' + search.value;
        input.innerHTML = 'You searched for ' + search.value + '. Please wait while the data loads.';
    } else { //default is browse all
        url = api_base_url + 'courses/';
        input.innerHTML = 'You searched for all courses. Please wait while the data loads.';
    }
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);
    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
                getNeoCallback(search.value, xmlHttpRequest.responseText);
            } 
        }; 
    xmlHttpRequest.send(null);
}

function getCoursesCallback (searchValue, responseText) {
    /*
    @param searchValue: The string entered by the user to be searched
    @param responseText: The JSON string from the api
    Called when search button is clicked from SearchButton()
    parses Json and creates table listing courses and 
    */
    var course_list = JSON.parse(responseText);
    var tableBody = '';
    if (responseText[0] == '['){ //search by date
        if (course_list.length == 0){
        tableBody += '<td>' + 'No courses found for your search.' + '</td>';
        } else {
            var tableBody = '';
            tableBody += '<thead><tr>';
            tableBody += '<td>' + 'Course Title' + '</td>';
            tableBody += '<td>' + 'Start Time' + '</td>';
            tableBody += '<td>' + 'End Time' + '</td>';
            tableBody += '</tr></thead><tbody>';
            for (var k = 0; k < course_list.length; k++){
                var course_dict = course_list[k];
                var obj = course_list[k].object;
                tableBody += '<td><a onclick="getCourses(' + obj + ")>" + '<a href='+ 'info/' + objString + '>' + obj + '</a></td>';
                var date = neoDict.closeapproachdate.split(" ")[0];
                tableBody += '<td>' + date.split(["-"[0]])[0] + '</td>';
                tableBody += '</tr>';
            }
        }
    } else if (responseText[0] == '{' && responseText.length>2) { //This is a search by name
        var tableBody = '';
        tableBody += '<thead><tr>';
        tableBody += '<td>' + 'Object Name' + '</td>';
        tableBody += '<td>' + 'Closest Approach Year' + '</td>';
        tableBody += '</tr></thead><tbody>';
        var neoDict = neoList; 
        var obj = neoDict.object;
        var objString = replaceAll(obj," ", "%20");
        tableBody += '<td>' + '<a href='+ 'info/' + objString + '>' + obj + '</a></td>';
        var date = neoDict.closeapproachdate.split(" ")[0];
        tableBody += '<td>' + date.split(["-"[0]])[0] + '</td>';
        tableBody += '</tr>';
    } else {
        tableBody += '<td>' + 'No objects found for your search.' + '</td>';
    }
    var resultsTableElement = document.getElementById('results_table');
    resultsTableElement.innerHTML = tableBody;
}

function neosCallback(responseText) {
    /*
    @param responseText: The JSON string from the api
    Called when browse button is clicked from BrowseButton()
    Parses Json and creates table listing names and years of all neos
    */
    var neosList = JSON.parse(responseText);
    var tableBody = '';
    tableBody += '<thead><tr>';
    tableBody += '<td>' + 'Object Name' + '</td>';
    tableBody += '<td>' + 'Closest Approach Year' + '</td></thead><tbody>';
    for (var k = 0; k < neosList.length; k++) {
        tableBody += '<tr>';
        var obj = neosList[k].object;
        var objString = replaceAll(obj, " ", "%20")
        tableBody += '<td><a onclick="getNeos(' + obj + ")>" + '<a href='+ 'info/' + objString + '>' + obj + '</a></td>';
        var date = neosList[k].closeapproachdate.split(" ")[0];
        tableBody += '<td>' + date.split(["-"[0]])[0] + '</td>';
        tableBody += '</tr>';
    }
    tableBody += '</tbody>'
    var resultsTableElement = document.getElementById('results_table');
    resultsTableElement.innerHTML = tableBody;
}

function BrowseButton() {
    /*
    Called when Browse button is clicked
    Resets screan of messages and tables
    Makes new request to api
    Calls function neosCallback()
    */
    browsed.innerHTML = 'You want to see all of the things. It will take a few seconds. Please wait.';
    var tableBody = "";
    var resultsTableElement = document.getElementById('results_table');
    resultsTableElement.innerHTML = tableBody;
    input.innerHTML = "";
    var url = api_base_url + 'neos/';
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);

    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
                neosCallback(xmlHttpRequest.responseText);
            } 
        }; 
    xmlHttpRequest.send(null);
}

function replaceAll(str, find, replace) {
	/*
	@param str: string to be modified
	@param find: string to replace
	@param replace: string to replace find with
	@return A string 
    Replaces all instances of find with replace in the string
    */
  return str.replace(new RegExp(find, 'g'), replace);
}