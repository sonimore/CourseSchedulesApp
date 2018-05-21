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
    		main = json.load(main_ratings)
		for i in os.listdir('/Users/sonimore/Documents/Projects/CourseSchedulesApp/Data'):
		    if i.endswith('.json'):
		        # files.append(i)
				# print(i)
				# print(type(main))
				# print(main.keys())
				path = 'Data/' + i
				# print(path)
				with open(path) as ratings:
			    		d = json.load(ratings)
		    			# print(d)

		    for prof in main:
		    		# print(prof)
		    		for dprof in d:
		    			if prof== dprof:
		    				print(d[dprof]['prof_proportion'])
			    			main[prof]['prof_proportion'].extend(d[dprof]['prof_proportion'][:])
			    			main[prof]['size'].extend(d[dprof]['size'][:])
			    			main[prof]['registered'].extend(d[dprof]['registered'][:])

		json.dump(main, main_ratings)


def main():
	Merge()

main()
