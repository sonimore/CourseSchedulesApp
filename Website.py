'''Sonia Moreno, September2017
Displays main page of website.
'''
import sys
import flask
import json
import config
import psycopg2

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/') 
def get_main_page():
    ''' This is the only route intended for human users '''
    return flask.render_template('index.html')



if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
    #     exit()

    # host = sys.argv[1]
    # port = sys.argv[2]
    app.run(debug = True)