''' Sonia Moreno, 9/20/2017
 Reads and parses a text file containing course schedule information.
 '''
def main():
	f = open('SampleText', 'r')
	courses = f.readlines()
	for line in courses:
		print(line)
		if "CS" in line:
			tempCourse = line
		if "Lecture/Discussion" in line:
			tempTime = line
			break




	data = {
    "Course Number":tempCourse,
    # "Course Title":courses[2],
    "Time":tempTime
	}
	print(data)


if __name__ == '__main__':
	main()


