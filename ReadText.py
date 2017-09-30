'''Sonia Moreno, 9/20/2017
 Reads and parses a text file containing course schedule information.
 '''
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
html = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=18WI&subject=CS').text

soup = BeautifulSoup(html, 'html5lib')


'''Returns list of course subjects. Each will be passed to function that returns
appropriate html link which contains specific course information for the subject
'''
def subject():
	html2 = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/').text
	soup2 = BeautifulSoup(html2, 'html5lib')
	print(soup2)

	# List of subjects
	subject_summary = soup2.find("select", id = "subjectElement")

	print subject_summary

	# Each subject within summary has tag "option"
	# Create a list with subjects, excluding 'Selected' tag (1st item)
	subjects = subject_summary.find_all("option")[1:]
	print subjects	
	return subjects

def main():




	# a_schedule = {'1a': '8:30', '2a': '9:50', '3a': '11:10', '4a': '12:30', '5a':'1:50', '6a': '3:10'}


	summary = soup.find_all("div", class_="course")

	# print summary[0]


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

	# print course_info







if __name__ == '__main__':
	main()



