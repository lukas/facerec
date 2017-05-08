
from __future__ import print_function
from urllib2 import Request, urlopen, URLError
import socket
socket.setdefaulttimeout(15)

# This is code for an amazon lambda function
# replce $TUNNELNAME with the name of your tunnel in the code

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Ok I'm talking to the optics lab "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please give me a message to pass along"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def show(intent, session):
    card_title = "Show Camera"
    if 'camera' in intent['slots']:
        camera = intent['slots']['camera']['value']
        if camera == 'behind me':
            camera = 'dennis'
        try:
            response = urlopen('http://$TUNNELNAME.localtunnel.me/show?camera=%s' % camera)
            if (camera == 'outside'):
                speech_output = "Ok, I'm Showing You What's Going On %s" % camera 
            elif camera == 'dennis':
                speech_output = "Ok, I'm showing you what's going on behind you" 
            else:
                speech_output = "Ok, I'm showing you what %s is seeing" % camera
        except URLError as e:
            speech_output = "Strange, I couldn't show %s" % camera
        except socket.timeout, e:
            speech_output = "The Optics Lab Timed out"
    else:
        speech_output = "I don't understand"
        
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



def face_camera(intent, session):
    card_title = "Face Camera"
    if 'camera' in intent['slots']:
        robot = intent['slots']['camera']['value']
        try:
            response = urlopen('http://$TUNNELNAME.localtunnel.me/faces/%s' % robot)
            data = response.read()
            if (data== "Not Found"):
                speech_output = "%s didn't see a face" % robot 
            else:
                person, gender, emotion = data.split(",")
                if person == "" or person is None:
                    speech_output = "%s didn't recognize the person, but " % robot
                else:
                    speech_output = "%s recognized %s and " % (robot, person)
                if gender == "Male":
                    speech_output += "he "
                else:
                    speech_output += "she "
                
                speech_output += "seems %s" % emotion.lower()
                

                
        except URLError as e:
            speech_output = "Strange, I couldn't wake up %s" % robot
        except socket.timeout, e:
            speech_output = "The Optics Lab Timed out"

    else:
        speech_output = "I don't know what robot you're talking about"
        
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



def tell_camera(intent, session):
    card_title = "Tell Camera"
    if 'camera' in intent['slots']:
        robot = intent['slots']['camera']['value']
        try:
            response = urlopen('http://$TUNNELNAME.localtunnel.me/labels/%s' % robot)
            speech_output = "%s is seeing %s " % (robot, response.read()) 
        except URLError as e:
            speech_output = "Strange, I couldn't wake up %s" % robot
        except socket.timeout, e:
            speech_output = "The Optics Lab Timed out"

    else:
        speech_output = "I don't know what robot you're talking about"
        
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def wake_up_robot(intent, session):
    card_title = "Wake Up"
    if 'robot' in intent['slots']:
        robot = intent['slots']['robot']['value']
        try:
            response = urlopen('http://$TUNNELNAME.localtunnel.me/wake?robot=%s' % robot)
            speech_output = "Ok, %s is awake " % robot 
        except URLError as e:
            speech_output = "Strange, I couldn't wake up %s" % robot
        except socket.timeout, e:
            speech_output = "The Optics Lab Timed out"

    else:
        speech_output = "I don't know what robot you're talking about"
        
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def drive_robot(intent, session):
    card_title = "Drive"
    if 'robot' in intent['slots']:
        robot = intent['slots']['robot']['value']
        try:
            response = urlopen('http://$TUNNELNAME.localtunnel.me/drive/%s' % robot)
            speech_output = "Ok, I told %s to look around " % robot 
        except URLError as e:
            speech_output = "Strange, I couldn't wake up %s" % robot
        except socket.timeout, e:
            speech_output = "The Optics Lab Timed out"

    else:
        speech_output = "I don't know what robot you're talking about"
        
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def wake_up():
    card_title = "Wake Up"
    try:
        response = urlopen('http://$TUNNELNAME.localtunnel.me/hi')
        speech_output = "Ok, the optics lab is awake " 
    except URLError as e:
        speech_output = "Strange, I couldn't wake up the optics lab"
        
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for talking to the optics lab. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))







# --------------- Events ------------------

def on_session_starreturn wake_up()
    elif intent_name == "ShowCameraIntent":
        return show(intent, session)
    elif intent_name == "WakeUpRobotIntent":
        return wake_up_robot(intent, session)
    elif intent_name == "DriveRobotIntent":
        return drive_robot(intent, session)
    elif intent_name == "TellCameraIntent":
        return tell_camera(intent, session)
    elif intent_name == "FakeTestIntent":
        return fake_face_camera(intent, session)
    elif intent_name == "PersonCameraIntent":
        return face_camera(intent, sessionot called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.)Id': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEnded
