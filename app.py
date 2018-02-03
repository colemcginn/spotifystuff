from flask import Flask
from flask import render_template
from flask import request
import songfunc
import threading
import os
from datetime import datetime
from threading import Timer
from shutil import copyfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
	if request.method == 'POST':
		username = request.form['text']
		t = threading.Thread(target=songfunc.allSongs, args=(username,))
		t.start()
		return render_template('new.html')
	elif request.method == 'GET':
		return redirect(url_for(''))

@app.route('/latest/<username>')
def latest(username):
	template = username + 'latest.html'
	return render_template(template)

@app.route('/all')
def all():
	return render_template('all.html')

@app.route('/last', methods=['GET', 'POST'])
def last():
	if request.method == 'POST':
		copyToLast()
		return render_template('last.html')
	elif request.method == 'GET':
		return render_template('last.html')

@app.route('/shutdown')
def shutdown():
	shutdown_server()
	return

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def copyToLast():
	src = 'templates/all.html'
	dst = 'templates/last.html'
	copyfile(src,dst)
	return

def updateLatest():
	print 'updating..............'
	t = threading.Thread(target=songfunc.allSongs, args=('fillerbil',))
	t.start()
	# startTimer()

def startTimer():
	x=datetime.today()
	y=x.replace(day=x.day+1, hour=3, minute=0, second=0, microsecond=0)
	delta_t=y-x
	secs=delta_t.seconds+1
	# secs = 5
	t = Timer(secs, updateLatest)
	t.start()

def checkLatest():
	if os.stat('templates/all.html').st_size < 100:
		t = threading.Thread(target=songfunc.allSongs, args=('fillerbil',))
		t.start()
	else:
		copyToLast()
	startTimerBackup()

def startTimerBackup():
	x=datetime.today()
	y=x.replace(day=x.day+1, hour=4, minute=0, second=0, microsecond=0)
	delta_t=y-x
	secs=delta_t.seconds+1
	t = Timer(secs, checkLatest)
	t.start()


if __name__ == "__main__":
	startTimer()
	# startTimerBackup()
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0')