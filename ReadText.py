'''Sonia Moreno, 9/20/2017
 Reads and parses a text file containing course schedule information.
 '''

from bs4 import BeautifulSoup
import requests
html = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=18WI&subject=CS').text
soup = BeautifulSoup(html, 'html5lib')
def main():

	a_schedule = {'1a': '8:30', '2a': '9:50', '3a': '11:10', '4a': '12:30', '5a':'1:50', '6a': '3:10'}


	letters = soup.find_all("div", class_="course")

	print letters[0]


	lobbying = {}
	for element in letters:
	
		course_num = element.find(class_="coursenum").get_text()
		title = element.find(class_ = "title").get_text()
		for item in title:
			course_name = element.find(class_="coursenum").next_sibling
			
		lobbying[course_num] = course_name


	print lobbying





if __name__ == '__main__':
	main()



