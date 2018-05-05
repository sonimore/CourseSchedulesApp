/*
    homepage.js
    Sonia Moreno 

    Search box and buttons for index.html
 */

 function onBrowseButton(){
    /*
    Called when Browse button is clicked
    Resets screan of messages and tables
    Makes new request to api
    Calls function coursesCallback()
    */
    document.getElementById("browsed").innerHTML = 'You want to see all of the things. It will take a few seconds. Please wait.';
    var tableBody = "";
    var resultsTableElement = document.getElementById('results_table');
    resultsTableElement.innerHTML = tableBody;
    input.innerHTML = "";
    var url = api_base_url + 'courses/';
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);

    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
                coursesCallback(xmlHttpRequest.responseText);
            } 
        }; 
    xmlHttpRequest.send(null);
}

function coursesCallback(responseText) {
    /*
    @param responseText: The JSON string from the api
    Called when browse button is clicked from BrowseButton()
    Parses Json and creates table listing names and years of all neos
    */
    console.log("one");

    var course_list = JSON.parse(responseText);
        console.log("two");
    //document.getElementById("input").innerHTML = course_list;
    var tableBody = '';
    tableBody += '<thead><tr>';
    tableBody += '<td>' + 'Course </td>';
    tableBody += '<td> Course Name </td>';
    tableBody += '<td> Start Time </td>';
    tableBody += '<td> End Time </td>';
    tableBody += '<td> Professor </td>';
    tableBody += '<td> Professor Rating </td></thead><tbody>';

    for (var k = 0; k < course_list.length; k++) {
        var id = course_list[k].course_id;
        var name = course_list[k].course_name;
        var time = course_list[k].start_time;
        var end_time = course_list[k].end_time;
        var faculty = course_list[k].faculty;
        var rating = course_list[k].prof_rating;
        tableBody += '<tr>';
        // tableBody += '<td><a onclick="getNeos(' + obj + ")>" + '<a href='+ 'info/' + objString + '>' + obj + '</a></td>';
        tableBody += '<td>' + id;
        tableBody += '<td><b onclick = "on()">' + name + '</b>';
        if (time != 'n/a'){
            tableBody += '<td>' + time;
        }
        else{
            tableBody += '<td>'
        }
        if (end_time != 'n/a'){
            tableBody += '<td>' + end_time;
        }
        else{
            tableBody += '<td>'
        }
        tableBody += '<td>' + faculty;
        if(rating != null){
        tableBody += '<td>' + rating};
        tableBody += '</tr>';

    }
    //     // var objString = replaceAll(obj, " ", "%20")
    //     // tableBody += '<td><a onclick="getCourses(' + obj + ")>" + '<a href='+ 'info/' + objString + '>' + obj + '</a></td>';
    //     // var date = course_list[k].split(" ")[0];
    //     tableBody += '<td><a onclick="getCourses()"</td>'
    tableBody += '</tbody>'
    console.log("Here we are");
    // var tableBody = "Hello";
    var resultsTableElement = document.getElementById('results_table');
    resultsTableElement.innerHTML = tableBody;
}

function onBrowseByButton(){
    var url = api_base_url + 'courses/department/';
    var tableBody = "";
    browseBy = document.getElementById('browseBy');
    var resultsTableElement = document.getElementById('results_table');
    resultsTableElement.innerHTML = tableBody;
    input.innerHTML = "";
    var url = url + browseBy.value;
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);

    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
                coursesCallback(xmlHttpRequest.responseText);
            } 
        }; 
    xmlHttpRequest.send(null);

    // Close the dropdown menu if user clicks outside of it
    // window.onclick = function(event){
    //     if(!event.target.matches('.dropbtn')){
    //         var dropdowns = document.getElementsByClassName("dropdown-content")
    //     }
    // }
}

// Functions to turn overlay on/off, respectively
function on(){
    document.getElementById("overlay").style.display = "block";
}
function off(){
    document.getElementById("overlay").style.display = 'none';
}



// function getDepartments(){
//     var url = api_base_url + '/courses/departments';
//     xmlHttpRequest = new XMLHttpRequest();
//     xmlHttpRequest.open('get', url);

//     xmlHttpRequest.onreadystatechange = function() {
//             if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
//                 getCoursesCallback(xmlHttpRequest.responseText);
//             } 
//         }; 

//     xmlHttpRequest.send(null);    
// }

// function getCourses() {
//     var url = api_base_url + '/courses';
//     xmlHttpRequest = new XMLHttpRequest();
//     xmlHttpRequest.open('get', url);

//     xmlHttpRequest.onreadystatechange = function() {
//             if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
//                 getCoursesCallback(xmlHttpRequest.responseText);
//             } 
//         }; 

//     xmlHttpRequest.send(null);

// function getCoursesCallback (responseText) {
//     /*
//     @param searchValue: The string entered by the user to be searched
//     @param responseText: The JSON string from the api
//     Called when search button is clicked from SearchButton()
//     parses Json and creates table listing courses and 
//     */
//     var course_list = JSON.parse(responseText);
//     var tableBody = '';

//     for (var k = 0; k < course_list.length; k++){
//         var course_dict = course_list[k];
//         var obj = course_list[k].object;
//         tableBody += '<td><a onclick="getCourses()"/td>';
//         var date = course_dict.closeapproachdate.split(" ")[0];
//         tableBody += '<td>' + date.split(["-"[0]])[0] + '</td>';
//         tableBody += '</tr>';
            
//     }
   
//     var resultsTableElement = document.getElementById('results_table');
//     resultsTableElement.innerHTML = tableBody;
// }






//  function onSearchButton() {
//     var url = api_base_url + 'courses/';
//     xmlHttpRequest = new XMLHttpRequest();
//     xmlHttpRequest.open('get', url);

//     xmlHttpRequest.onreadystatechange = function() {
//             if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
//                 authorsCallback(xmlHttpRequest.responseText);
//             } 
//         }; 

//     xmlHttpRequest.send(null);
// }


// function SearchButton() {
//     /*
//     Called when search button is clicked
//     Resets screan of messages and tables
//     Makes new request to api
//     Calls function getCoursesCallback()
//     */
//     var search = document.getElementById('search');
//     var searchedBy = document.getElementById('searchBy'); //default is name
//     //reset table body
//     var tableBody = "";
//     var resultsTableElement = document.getElementById('results_table');
//     resultsTableElement.innerHTML = tableBody;
//     browsed.innerHTML = "";
//     var url = api_base_url + 'courses/';

//     if(search.value!='') {
//         url = url + searchBy.value +'/' + search.value;
//         input.innerHTML = 'You searched for ' + search.value + '. Please wait while the data loads.';
//     } else { //default is browse all
//         url = api_base_url + 'courses/';
//         input.innerHTML = 'You searched for all courses. Please wait while the data loads.';
//     }
//     xmlHttpRequest = new XMLHttpRequest();
//     xmlHttpRequest.open('get', url);
//     xmlHttpRequest.onreadystatechange = function() {
//             if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
//                 getNeoCallback(search.value, xmlHttpRequest.responseText);
//             } 
//         }; 
//     xmlHttpRequest.send(null);
// }


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