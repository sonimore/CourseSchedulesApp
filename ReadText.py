'''Sonia Moreno, 9/20/2017
 Reads and parses a text file containing course schedule information.
 '''
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import re


'''Returns list of course subjects. Each will be passed to function that returns
appropriate html link which contains specific course information for the subject
'''
def Subject():
	html2 = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/').text
	soup2 = BeautifulSoup(html2, 'html5lib')
	print(soup2)

	# List of subjects
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

# Returns dict object with course number, course name, and start/end times for each course
# Finds course info based on the academic term and subject chosen (in this case, Winter 2018)
def Specific_Course_Info():

	html = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=18WI&subject=CS').text
	soup = BeautifulSoup(html, 'html5lib')
	summary = soup.find_all("div", class_="course")


	course_info = defaultdict(list)
	for element in summary:
	
		course_num = element.find(class_="coursenum").get_text()
		title = element.find(class_ = "title").get_text()
		for item in title:
			course_name = element.find(class_="coursenum").next_sibling	

		start_time = element.find(class_ = "start").get_text()
		end_time = element.find(class_ = "end").get_text()
		course_info[course_num].append(course_name)
		course_info[course_num].append(start_time)
		course_info[course_num].append(end_time)

	return course_info


def main():

	Subject()
	Specific_Course_Info()










if __name__ == '__main__':
	main()



