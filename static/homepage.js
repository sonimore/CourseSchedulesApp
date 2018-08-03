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
    Parses Json and creates table with course titles and course information snapshot
    */

    var course_list = JSON.parse(responseText);

    var tableBody = '';
    tableBody += '<thead><tr>';
    tableBody += '<td> Course </td>';
    tableBody += '<td> Course Name </td>';
    tableBody += '<td> Start Time </td>';
    tableBody += '<td> End Time </td>';
    tableBody += '<td> Professor </td>';
    tableBody += '<td> Professor Rating </td></thead><tbody>';

    for (var k = 0; k < course_list.length; k++) {
        var id = course_list[k].course_id;
        var name = course_list[k].course_name;
        var name_formatted = String(name.split(" ").join(""))
        var time = course_list[k].start_time;
        var end_time = course_list[k].end_time;
        var faculty = course_list[k].faculty;
        var rating = course_list[k].prof_rating;
        var ind = course_list[k].index;
        var index = ind.toString();
        tableBody += '<tr>';
        // tableBody += '<td><a onclick="getNeos(' + obj + ")>" + '<a href='+ 'info/' + objString + '>' + obj + '</a></td>';
        tableBody += '<td>' + id;
        tableBody += '<td><b onclick = "getCourses(' + index + ')">' + name + '</b>';
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
function on(ind, responseText){
    var specific_course_list = JSON.parse(responseText);
    document.getElementById("overlay").style.display = "block";
    var overlay_text = document.getElementById("text");
    var requirements_arr = [specific_course_list[0].requirements_met0, specific_course_list[0].requirements_met1, specific_course_list[0].requirements_met2];
    var requirements = ""

    for (var i = 0; i < requirements_arr.length; i++){
        if(requirements_arr[i] != null){
            requirements = requirements + requirements_arr[i];
            if (requirements_arr[i+1] != null){
                requirements += ", ";
            }
        }
    }
    
    var info_table = '';
    info_table += '<table width = "750"><tr valign = "top">';
    info_table += '<td> Start Time: </td>';
    info_table += '<td>' + specific_course_list[0].start_time + '</td></tr>';
    info_table += '<td> End Time: </td>';
    info_table += '<td>' + specific_course_list[0].end_time + '</td></tr>';

    info_table += '<tr valign = "top"><td> Description: </td>';
    info_table += '<td>' + specific_course_list[0].description + '</td></tr>';

    info_table += '<tr valign = "top"><td> Requirements Met: </td>';
    info_table += '<td>' + requirements;

    overlay_text.innerHTML = info_table;
}
function off(){
    document.getElementById("overlay").style.display = 'none';
}

function getCourses(ind) {
    var url = api_base_url + 'courses/id/' + parseInt(ind);
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);

    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
                on(ind, xmlHttpRequest.responseText);
            } 
        }; 

    xmlHttpRequest.send(null);
}

// function getCourseInfoCallback (responseText) {
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


// function getCourseInfo(course_name) {
//     /*
//     Called when search button is clicked
//     Resets screan of messages and tables
//     Makes new request to api
//     Calls function getCoursesCallback()
//     */

//     var url = api_base_url + 'name/' + course_name;

//     xmlHttpRequest = new XMLHttpRequest();
//     xmlHttpRequest.open('get', url);
//     xmlHttpRequest.onreadystatechange = function() {
//             if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) { 
//                 on(course_name, xmlHttpRequest.responseText);
//             } 
//         }; 
//     xmlHttpRequest.send(null);
// }
