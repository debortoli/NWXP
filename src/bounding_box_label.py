import sys
import os
import random
import flask
import numpy as np
from PIL import Image
import pdb

app = flask.Flask(__name__)
last_filename = None

@app.route('/<path:filename>')
def app_route_static_file(filename):
	return app.send_static_file(filename)

@app.route('/')
def main_page():
	return app.send_static_file('index.html')

@app.route('/frame.jpg')
def next_frame():
	global list_of_images,counter,filename,imagename,top_directory,numRepeated

	return flask.Response(open(filename).read(), mimetype='image/jpeg')

@app.route('/box')
def box():
	global filename
	x0 = flask.request.values.get('x0')
	x1 = flask.request.values.get('x1')
	y0 = flask.request.values.get('y0')
	y1 = flask.request.values.get('y1')
	x0, x1 = min(x0,x1), max(x0, x1)
	y0, y1 = min(y0,y1), max(y0, y1)
	line = "{},{},{},{},{}".format(filename[11:-4], x0, x1, y0, y1)
	open('transmissionlines.csv', 'a').write(line + '\n')#change this depending on the file you're labeling
	return 'OK'

def runApp():
	global list_of_images,counter,top_directory,numRepeated,filename
	filename='../images/level3_label.png'	

	app.run('0.0.0.0', port=8002)

if __name__ == '__main__':
	runApp()
