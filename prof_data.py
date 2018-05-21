''' Sonia Moreno, 5/2018
 Scrapes data from Carleton Enroll website containing course schedule information.
 '''
from __future__ import division
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import re
import csv
import sys
import json



''' Returns list of academic terms that user can choose from. Item in list
will be passed to function that returns html link with term info provided.
Example: 'term=18WI' in 'https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=18WI&subject=CS'
'''
def Academic_Term():
	# Homepage showing listings of academic terms and course subjects
	html_enroll = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/').text
	soup2 = BeautifulSoup(html_enroll, 'lxml')

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
	html_enroll = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/').text
	soup2 = BeautifulSoup(html_enroll, 'lxml')


	# Tag object containing list of subjects
	subject_summary = soup2.find("select", id = "subjectElement")

	# Each subject within summary has tag "option"
	# Create a list with subjects, excluding 'Selected' tag (1st item)
	subjects = subject_summary.find_all("option")[1:]

	# Only get the associated text, excluding the tag itself and add them to list
	subj_list = []
	for item in subjects:
		subj_list.append(item.get_text())

	# print subj_list

	# Each item in subj_list is currently in the form: 'Computer Science (CS)'
	# We only want the abbrevation in the parentheses so that we can use this in the html link
	# We use regular expressions to achieve this.
	subj_abbrev = []
	for i in subj_list:
		subj_abbrev.append(re.search('\((.*?)\)', i).group(1))

	# print subj_abbrev
		
	return subj_abbrev

# Formats strings with spaces to replace spaces with %20
# Makes it so courses are searchable by names in the API
def format_course(text):
    course = ''
    course_parser = text.split(' ')
    for word in course_parser:
        course += word
        if course_parser.index(word) != len(course_parser)-1 and word != '':
            course += '%20'
    return course

''' Returns dict object with course number, course name, and start/end times for each course
Finds course info based on the academic term and subject chosen (in this case, Winter 2018)
'''

def Specific_Course_Info(term):
	
	with open('prof_ratings.json') as ratings:
    		d = json.load(ratings)
    		# print(d)

	# Creates dict object with course number as key and list containing name and times for course as values
	
	prof_info = {}
	# print(prof_info)
	subjects = Subject()
	index = 1
	for subject in subjects:

		html_string = 'https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=' + term + '&subject=' + subject

		# Course listings for subject during term provided
		html = requests.get(html_string).text

		soup = BeautifulSoup(html, 'lxml')

		# Creates list of all items with course as class attribute, excluding related courses
		course_summary = soup.find_all("div", class_="course")
		for course in course_summary:
			course_num = course.find(class_= "coursenum").get_text()
			course_num = format_course(course_num)
			# Add info to list associated with key
			
			# # Ensures that no related courses are added
			if course_num.find(subject) > -1:
			# 	if course.find(class_ = "status") != None:
			# 		enrollment = course.find(class_ = "status").get_text()
			# 		# specific_info['enrollment'] = enrollment
			# 		registered = re.findall(r'(?<=Registered: ).*?(?=\,)', enrollment)[0]
			# 		size = re.findall(r'(?<=Size: ).*?(?=\,)', enrollment)[0]
			# 		# print registered
			# 		# specific_info['registered'] = registered
			# 		# specific_info['size'] = size
			# 		# print enrollment
			# 	else:
			# 		specific_info['registered'] = "n/a"
			# 		specific_info['size'] = "n/a"

				if course.find(class_ = "faculty") != None:
					faculty = course.find(class_ = "faculty").get_text().strip()					
					# Add ratemyprofessor.com rating to dictionary
					for prof in d:
						if prof['FIELD4'] in faculty[0:10] and prof['FIELD5'] in faculty[3:14] and len(faculty) < 20 and  faculty not in prof_info.keys():

						# if prof['FIELD4']==faculty.split()[0] and prof['FIELD5']==faculty.split()[1] and faculty not in prof_info.keys():

						# if prof['FIELD4'] in faculty and prof['FIELD5'] in faculty or (prof['FIELD5'] in faculty) and not specific_info['faculty'] and ',' not in faculty and '\\xe1n' not in faculty:
							specific_info = {}
							specific_info['faculty'] = faculty
							specific_info['department'] = prof['FIELD7']
							specific_info['status'] = prof['FIELD6']
							specific_info['number_of_ratings'] = prof['FIELD3']
							specific_info['prof_rating'] = prof['FIELD1']

							# print(type(registered))

							if course_num.find(subject) > -1:
								if course.find(class_ = "status") != None:
									enrollment = course.find(class_ = "status").get_text()
									# specific_info['enrollment'] = enrollment
									registered = re.findall(r'(?<=Registered: ).*?(?=\,)', enrollment)[0]
									size = re.findall(r'(?<=Size: ).*?(?=\,)', enrollment)[0]
									# print registered
									specific_info['registered'] = [registered]
									specific_info['size'] = [size]
									# print enrollment
								else:
									specific_info['registered'] = 0
									specific_info['size'] = 0
								registered = int(registered)
								size = int(size)
								# print(size)

							if size != 0:
								proportion = registered/size
								# print(proportion)
								specific_info['prof_proportion'] = [proportion]
							else:
								specific_info['prof_proportion'] = []
							# print(prof_info['prof_info'])
							prof_info[faculty] = specific_info
						elif prof['FIELD4'] in faculty[0:10] and prof['FIELD5'] in faculty[3:14] and len(faculty) < 20:
							# registered = prof_info['prof_info'][0][faculty]['prof_proportion']['registered']
							# size = prof_info['prof_info'][0][faculty]['prof_proportion']['size']
							if course_num.find(subject) > -1:
								if course.find(class_ = "status") != None:
									enrollment = course.find(class_ = "status").get_text()
									# specific_info['enrollment'] = enrollment
									registered = re.findall(r'(?<=Registered: ).*?(?=\,)', enrollment)[0]
									size = re.findall(r'(?<=Size: ).*?(?=\,)', enrollment)[0]
									# print registered
									prof_info[faculty]['registered'].append(registered)
									prof_info[faculty]['size'].append(size)
									# print enrollment
								registered = int(registered)
								size = int(size)
								# print(size)
								# print(prof_info[faculty]['registered'])
							if size != 0:
								proportion = registered/size
								# print(proportion)
								prof_info[faculty]['prof_proportion'].append(proportion)
								# prof_info['prof_info'][0][faculty]['prof_proportion'].append(registered/size)
								# specific_info['proportion'] = proportion
	# Creates csv file with course info
	# with open('course_info7.csv', 'w') as f: 
	# 	w = csv.DictWriter(f, course_info.keys())
	# 	w.writeheader()
	# 	w.writerow(course_info)

	# output_file = open('courses_table.csv', 'w')
	# writer = csv.writer(output_file)
	# for course in course_info['course_info']:
	# 	course_row = [course['course_num'].encode("utf-8"), course['title'].encode("utf-8"), course['start_time'].encode("utf-8"), course['end_time'].encode("utf-8")]
	# 	writer.writerow(course_row)
	# output_file.close()
	# print course_info


	# print(course_info)
	# print(prof_info)
	filename = 'prof_data_' + term + '.json'
	with open(filename, 'w') as fp:
		json.dump(prof_info, fp)
	return prof_info



# ''' Adds lists together from Specific_Course_Info so that each csv file will contain info 
# for ALL subjects in one term
# ''' 
# def Append_Dicts(a_dict, b_dict):
# 	return


''' Returns HTML string that Specific Course Info will use to provide information
for every term and subject combination.
'''
def Generate_HTML():
	terms = Academic_Term()[1:3]
	subjects = Subject()[1:3]
	html = []
	for term in terms:
		for subject in subjects:
			print term
			print subject
		Specific_Course_Info(term, subject)

def main():
	# Academic_Term()
	# Subject()
	# Generate_HTML()
	Specific_Course_Info('13FA')
	# Specific_Course_Info('14FA')
	# Specific_Course_Info('15FA')
	# Specific_Course_Info('16FA')
	# Specific_Course_Info('17FA')
	# Specific_Course_Info('14WI')
	# Specific_Course_Info('15WI')
	# Specific_Course_Info('16WI')
	# Specific_Course_Info('17WI')
	# Specific_Course_Info('18WI')
	# Specific_Course_Info('14SP')
	# Specific_Course_Info('15SP')
	# Specific_Course_Info('16SP')
	# Specific_Course_Info('17SP')
	# Specific_Course_Info('18SP')




main()



