#!/usr/bin/env python3
'''
    courses_api.py
    Sonia

    Simple Fla sk API used in the sample web app for
    courses web app. This is the Flask app for the
    "courses" API only. There's a separate Flask app
    for the courses website.
'''
import sys
import flask
import json
import config
import psycopg2

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
course_id2 = ''
def _fetch_all_rows_for_query(query):
    '''
    Returns a list of rows obtained from the courses database by the specified SQL
    query. If the query fails for any reason, an empty list is returned.
    '''
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print("connection error")
        #print('Connection error:', e, file=sys.stderr)
        return []

    rows = []
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall() # This can be trouble if your query results are really big.
    except Exception as e:
        #print('Error querying database:', e, file=sys.stderr)
        return []

    connection.close()
    return rows

@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# def format_course(text):
#     course = ''
#     course_parser = text.split('%20')
#     for word in course_parser:
#         course += word
#         if course_parser.index(word) != len(course_parser)-1 and word != '':
#             course += ' '
#     return course

@app.route('/courses/') 
def get_courses():
    '''
    Returns a list of all the courses in our database, in alphabetical
    order by course_name.
    '''
    query = '''SELECT index, course_id, course_name, start_time, end_time, faculty, department, prof_rating
               FROM courses ORDER BY '''
    sort_argument = flask.request.args.get('sort')

    if sort_argument == 'start_time':
        query += 'start_time'
    else:
        query += 'course_id'

    # course_id2 = format_course(course_id)
    courses_list = []
    for row in _fetch_all_rows_for_query(query):
        url = flask.url_for('get_courses_by_course_id', index = row[0], _external=True)
        course = {'index': row[0], 'course_id':row[1].replace("+", " "), 'course_name':row[2].replace("+", " "), 'start_time':row[3],
                  'end_time':row[4], 'faculty':row[5], 'department':row[6], 'prof_rating':row[7], 'url':url.strip('%25')}
        courses_list.append(course)
        print(row[0])

    return json.dumps(courses_list)

@app.route('/courses/name/<course_name>')
def get_courses_by_course_name(course_name):
    '''
    Returns a list of all the courses with course titles equal to
    (case-insensitive) the specified course title.  See get_course_by_course_id
    below for description of the courses resource representation.
    '''
    query = '''SELECT course_id, course_name, start_time, end_time, faculty, department
               FROM courses
               WHERE UPPER(course_name) =  UPPER('{0}')
               ORDER BY course_name'''.format(course_name)
    courses_list = []
    for row in _fetch_all_rows_for_query(query):
        url = "http://localhost:5234/courses/name/" + row[1]
        course = {'course_id':row[0].replace("+", " "), 'course_name':row[1].replace("+", " "), 'start_time':row[2],
                  'end_time':row[3], 'faculty':row[4], 'department':row[5], 'url':url}
        # course_partition = course['course_name'].split(" ")
        # course_name2 = ''
        # for word in course_partition:
        #     course_name2 += word
        # if course_name == course_name2:
            # courses_list.append(course)
        courses_list.append(course)

    return json.dumps(courses_list)

# @app.route('/courses/<course_id>')
# def course_id(course_id):
#     course_id2 = flask.url_for(course_id)
#     print(course_id2)


@app.route('/courses/id/')
def get_course_id():
    query = ''' SELECT index, course_id, course_name, start_time, end_time, faculty, department
               FROM courses ORDER BY index'''
    rows = _fetch_all_rows_for_query(query)
    courses_list = []
    for row in rows:
        url = flask.url_for('get_courses_by_course_id', index = row[0], _external=True)
        course = {'index':row[0], 'course_name':row[1].replace("+", " ")}
        if course not in courses_list:
            courses_list.append(course)
    return json.dumps(courses_list)

@app.route('/courses/id/<index>')
def get_courses_by_course_id(index):
    '''
    Returns the course resource that has the specified course_id.
    A course resource will be represented as a JSON dictionary
    with keys 'course_name' (string value), 'start_time' (string),
    'end_time' (string), 'course_id' (string),
    and 'url' (string). The value associated with 'url' is a URL
    you can use to retrieve this same course in the future.
    '''
    # print(index)
    query = '''SELECT index, course_id, course_name, start_time, end_time, faculty, department, prof_rating
               FROM courses WHERE index = {0}'''.format(index)
    courses_list = []
    # print("here")
    # print(query)
    rows = _fetch_all_rows_for_query(query)
    # print("rows1:")
    # print(rows)
    for row in rows:
        # print("ROWS:")
        # print(row[0])
        url = flask.url_for('get_courses_by_course_id', index = row[0], _external=True)
        course = {'course_index': row[0], 'course_id':row[1].replace("+", " "), 'course_name':row[2].replace("+", " "), 'start_time':row[3],
                  'end_time':row[4], 'faculty':row[5], 'department':row[6], 'prof_rating':row[7], 'url':url}
        courses_list.append(course)

    return json.dumps(courses_list)

@app.route('/courses/departments/')
def get_course_departments():
    query = ''' SELECT index, course_id, course_name, start_time, end_time, faculty, department
               FROM courses ORDER BY department'''
    rows = _fetch_all_rows_for_query(query)
    courses_list = []
    for row in rows:
        url = "http://localhost:5234/courses/" + row[0]
        course = {'department':row[6]}
        if course not in courses_list:
            courses_list.append(course)
    return json.dumps(courses_list)


@app.route('/courses/department/<department>')
def get_courses_by_department(department):
    '''
    Returns the course resource that has the specified department.
    A course resource will be represented as a JSON dictionary
    with keys 'course_name' (string value), 'start_time' (string),
    'end_time' (string), 'course_id' (string),
    and 'url' (string). The value associated with 'url' is a URL
    you can use to retrieve this same course in the future.
    '''
    query = '''SELECT index, course_id, course_name, start_time, end_time, faculty, department, prof_rating
               FROM courses WHERE UPPER(department) LIKE UPPER('{0}') ORDER BY department'''.format(department)
    courses_list = []
    rows = _fetch_all_rows_for_query(query)
    for row in rows:
        url = flask.url_for('get_courses_by_course_id', index = row[0], _external=True)
        course = {'course_index': row[0], 'course_id':row[1].replace("+", " "), 'course_name':row[2].replace("+", " "), 'start_time':row[3],
                  'end_time':row[4], 'faculty':row[5], 'department':row[6], 'prof_rating':row[7], 'url':url}
        courses_list.append(course)

    return json.dumps(courses_list)




@app.route('/help')
def help():
    rule_list = []
    for rule in app.url_map.iter_rules():
        rule_text = rule.rule.replace('<', '&lt;').replace('>', '&gt;')
        rule_list.append(rule_text)
    return json.dumps(rule_list)

if __name__ == '__main__':
    # format_course_id('amst 123')
    if len(sys.argv) != 3:
        #print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=int(port), debug=True)
