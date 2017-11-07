#!/usr/bin/env python3
'''
    courses_api.py
    Sonia

    Simple Flask API used in the sample web app for
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

def _fetch_all_rows_for_query(query):
    '''
    Returns a list of rows obtained from the courses database by the specified SQL
    query. If the query fails for any reason, an empty list is returned.
    '''
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print('Connection error:', e, file=sys.stderr)
        return []

    rows = []
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall() # This can be trouble if your query results are really big.
    except Exception as e:
        print('Error querying database:', e, file=sys.stderr)

    connection.close()
    return rows

@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/courses/') 
def get_courses():
    '''
    Returns a list of all the courses in our database, in alphabetical
    order by course_title.
    '''
    
    query = '''SELECT course_num, course_title, start_time, end_time
               FROM courses ORDER BY '''
               
    sort_argument = flask.request.args.get('sort')
    if sort_argument == 'start_time':
        query += 'start_time'
    else:
        query += 'course_title'

    courses_list = []
    for row in _fetch_all_rows_for_query(query):
        url = flask.url_for('get_courses_by_course_num', course_num=row[0], _external=True)
        course = {'course_num':row[0], 'course_title':row[1], 'start_time':row[2],
                  'end_time':row[3], 'url':url}
        courses_list.append(course)

    return json.dumps(courses_list)

@app.route('/courses/<course_title>')
def get_courses_by_course_title(course_title:
    '''
    Returns a list of all the courses with course titles equal to
    (case-insensitive) the specified course title.  See get_course_by_course_num
    below for description of the courses resource representation.
    '''
    query = '''SELECT course_num, course_title, start_time, end_time
               FROM courses
               WHERE UPPER(course_title) LIKE UPPER('%{0}%')
               ORDER BY course_title'''.format(course_title)

    courses_list = []
    for row in _fetch_all_rows_for_query(query):
        url = flask.url_for('get_courses_by_course_num', course_num=row[0], _external=True)
        course = {'course_num':row[0], 'course_title':row[1], 'start_time':row[2],
                  'end_time':row[3], 'url':url}
        courses_list.append(course)

    return json.dumps(courses_list)

@app.route('/author/<author_id>')
def get_author_by_id(author_id):
    '''
    Returns the course resource that has the specified course_num.
    A course resource will be represented as a JSON dictionary
    with keys 'course_title' (string value), 'start_time' (string),
    'end_time' (string), 'course_num' (string),
    and 'url' (string). The value associated with 'url' is a URL
    you can use to retrieve this same course in the future.
    '''
    query = '''SELECT course_num, course_title, start_time, end_time
               FROM courses WHERE course_num = {0}'''.format(course_num)

    rows = _fetch_all_rows_for_query(query)
    if len(rows) > 0:
        row = rows[0]
        url = flask.url_for('get_course_by_course_num', course_num=row[0], _external=True)
        course = {'course_num':row[0], 'course_title':row[1], 'start_time':row[2],
                  'end_time':row[3], 'url':url}
        return json.dumps(course)

    return json.dumps({})


@app.route('/help')
def help():
    rule_list = []
    for rule in app.url_map.iter_rules():
        rule_text = rule.rule.replace('<', '&lt;').replace('>', '&gt;')
        rule_list.append(rule_text)
    return json.dumps(rule_list)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=int(port), debug=True)