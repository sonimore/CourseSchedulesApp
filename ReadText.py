''' Sonia Moreno, 9/2017
 Scrapes data from Carleton Enroll containing course schedule information.
 '''
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import re


''' Returns list of academic terms that user can choose from. Item in list
will be passed to function that returns html link with term info provided.
Example: 'term=18WI' in 'https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=18WI&subject=CS'
'''
def Academic_Term():
	html_enroll = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/').text
	soup2 = BeautifulSoup(html_enroll, 'html5lib')

	# Tag object containing list of academic terms 
	term_summary = soup2.find("select", id = "termElement")


	# Each term name such as "Winter 2018" has tag "option"
	terms = term_summary.find_all("option")

	# We want the value attribute; example: <option value="18WI">
	# Create list with all value attributes; this will be list of terms available to choose from
	term_list = []
	for option in terms:
		term_list.append(option['value'])

	return term_list


''' Returns list of course subjects. Each will be passed to function that returns
appropriate html link which contains specific course information for the subject
Example: 'subject=CS' in 'https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=18WI&subject=CS'
'''
def Subject(): 
	# Homepage showing listings of academic terms and course subjects
	html_enroll = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/').text
	soup2 = BeautifulSoup(html_enroll, 'html5lib')


	# Tag object containing list of subjects
	subject_summary = soup2.find("select", id = "subjectElement")

	# Each subject within summary has tag "option"
	# Create a list with subjects, excluding 'Selected' tag (1st item)
	subjects = subject_summary.find_all("option")[1:]

	# Only get the associated text, excluding the tag itself and add them to list
	subj_list = []
	for item in subjects:
		subj_list.append(item.get_text())

	# Each item in subj_list is currently in the form: 'Computer Science (CS)'
	# We only want the abbrevation in the parentheses so that we can use this in the html link
	# We use regular expressions to achieve this.
	subj_abbrev = []
	for i in subj_list:
		subj_abbrev.append(re.search(r"\s*\(.+?\)", i).group())
		
	return subj_abbrev


''' Returns dict object with course number, course name, and start/end times for each course
Finds course info based on the academic term and subject chosen (in this case, Winter 2018)
'''
def Specific_Course_Info():
	# Course listings for computer science during winter term of 2018
	html = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=18WI&subject=CS').text
	soup = BeautifulSoup(html, 'html5lib')

	# Creates list of all items with course as class attribute
	course_summary = soup.find_all("div", class_="course")

	# Creates dict object with course number as key and list containing name and times for course as values
	course_info = defaultdict(list)
	for course in course_summary:
		course_num = course.find(class_= "coursenum").get_text()

		# Finds title attribute within each course
		title = course.find(class_ = "title").get_text()

		# Only takes the actual name of the course
		# which is next to the coursenum attribute but not within its own tag
		for item in title:
			course_name = course.find(class_= "coursenum").next_sibling	

		# Start and end times for course
		start_time = course.find(class_ = "start").get_text()
		end_time = course.find(class_ = "end").get_text()

		# Add info to list associated with key
		course_info[course_num].append(course_name)
		course_info[course_num].append(start_time)
		course_info[course_num].append(end_time)

	return course_info


def main():
	Academic_Term()
	Subject()
	Specific_Course_Info()

main()



