'''Sonia Moreno, 9/20/2017
 Reads and parses a text file containing course schedule information.
 '''

from bs4 import BeautifulSoup
import requests
html = requests.get('https://apps.carleton.edu/campus/registrar/schedule/enroll/?term=18WI&subject=CS').text
soup = BeautifulSoup(html, 'html5lib')
def main():
	# print(html)
	a_schedule = {'1a': '8:30', '2a': '9:50', '3a': '11:10', '4a': '12:30', '5a':'1:50', '6a': '3:10'}

	# first_course = soup.find('h3')
	# first_course_text = soup.div.text
	# fi = soup.div['id']
	first_course = soup('div', "course")
	print(first_course)
	print(len(first_course))
	# print(first_course_text)





if __name__ == '__main__':
	main()



