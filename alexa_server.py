from subprocess import call, Popen, PIPE
from urllib2 import Request, urlopen, URLError, quote
import socket
socket.setdefaulttimeout(10)
import cameras as c

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Ok'

@app.route('/hi')
def hi():
    call(["espeak", "hi everyone"])
    return 'Ok'

@app.route('/drive/<path:robot>')
def drive(robot):
    host = '%s.local' % robot
    command=  'http://%s.local/say?text=%s' %(robot, quote('ok I\'ll take a look around'))
    print(command)
    call(["wget", command])
    cmd = ["bash", "cam.sh", host]
    p = Popen(cmd, stdout=PIPE)

    command = 'http://%s.local/drive?time=20' % robot
    call(["wget", command])
    
    return "Ok"

@app.route('/wake')
def wake():
    robot = request.args.get('robot').lower()
    call(["espeak", "ok, I'm waking up %s" % robot])

    if robot == 'willy':
        response = urlopen('http://willy.local/shake')
    if robot == 'wilma':
        response = urlopen('http://wilma.local/demo')
    if robot == 'wallace':
        response = urlopen('http://wallace.local/say?text=%s' % quote('hello this is wallace'))
        response = urlopen('http://wallace.local/shake')
    if robot == 'wonkus':
        response = urlopen('http://wonkus.local/say?text=%s' % quote('hello this is wonkus'))
        response = urlopen('http://wonkus.local/shake')

    
    return "Ok"


@app.route('/show_all_cameras')
def show_all_cameras():
    c.show_all_cameras()
    return "Ok"

def say_labels_camera(camera):
    Popen(['wget', 'http://%s.local/say?text=%s' % (camera, quote("I think I would describe what I'm seeing as"))])
    labels = c.label_camera(camera)[0:3]
    response = urlopen('http://%s.local/say?text=%s' % (camera, quote("%s or maybe %s" % (labels[0], labels[1]))))
    return labels

@app.route('/labels/<path:camera>')
def labels_camera(camera):
    print("Getting labels for %s" % camera)
    if (camera == 'wonkus' or camera == "wallace"):
        return ",".join(say_labels_camera(camera))
    else:
        labels = c.label_camera(camera)[0:3]
        return ",".join(labels)

@app.route('/faces/<path:camera>')
def face_camera(camera):
    data = c.face_camera(camera)
    print(data)
    if data:
        if data != "":
            if data[0] is None:
                data[0]=""
            return ",".join(data)
        else:
            return "Not Found"
    else:
        return "Not Found"


@app.route('/show')
def show():
    camera = request.args.get('camera').lower()

    print("Showing %s" % camera)
    
    host ='charlie.local'
    if camera == "wallace":
        host = "wallace.local"
    elif camera == 'willy':
        host = "willy.local"
    elif camera == "wilma":
        host = "wilma.local"
    elif camera == "wonkus":
        host = "wonkus.local"
    elif camera == "front" or camera == 'infront' or camera == "willa":
        host = "willa.local"
    elif camera == "dennis":
        host = "dennis.local"
        
    
    cmd = ["bash", "cam.sh", host]
    p = Popen(cmd, stdout=PIPE)
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    
