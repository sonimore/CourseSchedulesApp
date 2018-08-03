import json as simplejson

import csv

courses_parsed = simplejson.loads('course_data_18WI.json')

course_data = courses_parsed['course_info']

# open a file for writing

data = open('course_data_18WI.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(data)

count = 0

for course in course_data:

      if count == 0:

             header = course.keys()

             csvwriter.writerow(header)

             count += 1

      csvwriter.writerow(course.values())

data.close()