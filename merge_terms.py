from __future__ import division
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import re
import csv
import sys
import json
import os
def Merge():
	with open('prof_data_13FA.json', 'r+') as main_ratings:
		try:
    			main = json.load(main_ratings)
    			print(main)
			for i in os.listdir('/Users/sonimore/Documents/Projects/CourseSchedulesApp/Data'):
			    if i.endswith('.json'):
			        # files.append(i)
					# print(i)
					# print(type(i))
					path = 'Data/' + i
					# print(path)
					with open(path) as ratings:
						try:
				    			d = json.load(ratings)
				    		# print(d)
							for prof in main:
					    			for dprof in d:
						    			if prof== dprof:
							    			prof['prof_proportion'].append(dprof['prof_proportion'])
							    			prof['size'].append(dprof['size'])
							    			prof['enrollment'].append(dprof['enrollment'])
						except:
							sys.stderr.write('Could not parse JSON file: {0}'.format(path))

			json.dump(main, main_ratings)

		except:
			sys.stderr.write('Could not parse JSON file')


	# Creates dict object with course number as key and list containing name and times for course as values
	
	# prof_info = defaultdict(list)

	# subjects = Subject()
	# index = 1
	# for subject in subjects:

	# 	html_string = 'https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=' + term + '&subject=' + subject

	# 	# Course listings for subject during term provided
	# 	html = requests.get(html_string).text
	# 	soup = BeautifulSoup(html, 'lxml')

	# 	# Creates list of all items with course as class attribute, excluding related courses
	# 	course_summary = soup.find_all("div", class_="course")
	# 	for course in course_summary:
	# 		course_num = course.find(class_= "coursenum").get_text()
	# 		course_num = format_course(course_num)
	# 		if course_num.find(subject) > -1:
	# 			if course.find(class_ = "faculty") != None:
	# 				faculty = course.find(class_ = "faculty").get_text().strip()					
	# 				# Add ratemyprofessor.com rating to dictionary
	# 				for prof in d:
	# 					if prof['teacherfirstname_t'] in faculty and prof['teacherlastname_t'] in faculty or (prof['teacherlastname_t'] in faculty):
	# 						specific_info = {}
	# 						specific_info['faculty'] = faculty

	# 						specific_info['prof_rating'] = prof['averageratingscore_rf']

	# 						# print(type(registered))

	# 						if course_num.find(subject) > -1:
	# 							if course.find(class_ = "status") != None:
	# 								enrollment = course.find(class_ = "status").get_text()
	# 								# specific_info['enrollment'] = enrollment
	# 								registered = re.findall(r'(?<=Registered: ).*?(?=\,)', enrollment)[0]
	# 								size = re.findall(r'(?<=Size: ).*?(?=\,)', enrollment)[0]
	# 								# print registered
	# 								specific_info['registered'] = [registered]
	# 								specific_info['size'] = [size]
	# 								# print enrollment
	# 							else:
	# 								specific_info['registered'] = 0
	# 								specific_info['size'] = 0
	# 							registered = int(registered)
	# 							size = int(size)
	# 							# print(size)
	# 						if size != 0:
	# 							proportion = registered/size
	# 							# print(proportion)
	# 							specific_info['prof_proportion'] = [proportion]

	# 						prof_info['prof_info'].append(specific_info)
	# 							# specific_info['proportion'] = proportion
	# # Creates csv file with course info
	# # with open('course_info7.csv', 'w') as f: 
	# # 	w = csv.DictWriter(f, course_info.keys())
	# # 	w.writeheader()
	# # 	w.writerow(course_info)

	# # output_file = open('courses_table.csv', 'w')
	# # writer = csv.writer(output_file)
	# # for course in course_info['course_info']:
	# # 	course_row = [course['course_num'].encode("utf-8"), course['title'].encode("utf-8"), course['start_time'].encode("utf-8"), course['end_time'].encode("utf-8")]
	# # 	writer.writerow(course_row)
	# # output_file.close()
	# # print course_info


	# # print(course_info)
	# filename = 'prof_data_' + term + '.json'
	# with open(filename, 'w') as fp:
	# 	json.dump(prof_info, fp)
	# return prof_info

def main():
	# Academic_Term()
	# Subject()
	# Generate_HTML()
	Merge()

main()
