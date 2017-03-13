import urllib
from subprocess import call, Popen, PIPE
import shutil
import threading
from PIL import Image 
import json
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

camera_list = [
    'charlie',
    'wonkus',
    'wallace',
    'willy',
    'wilma',
    'dennis',
    'willa'
]


image_files =[]

def describe_face_image(image_filename):
    cmd = Popen(["bash", "detect-faces.sh", image_filename], stdout=PIPE)
    
    output = ""
    for line in cmd.stdout:
        output += line

    data = json.loads(output)
    if len(data["FaceDetails"]) == 0:
        return []
    else:
        gender = data["FaceDetails"][0]["Gender"]["Value"] # Male or Female
        emotion = data["FaceDetails"][0]["Emotions"][0]["Type"] # CALM, etc.
        return [gender, emotion]
        
def identify_face_image(image_filename):
    cmd = Popen(["bash", "match-faces.sh", image_filename], stdout=PIPE)
    
    output = ""
    for line in cmd.stdout:
        output += line

# Typical Return Value
#{
#    "SearchedFaceBoundingBox": {
#        "Width": 0.2554086446762085, 
#        "Top": 0.1308760643005371, 
#        "Left": 0.3861177861690521, 
#        "Height": 0.4540598392486572
#    }, 
#    "SearchedFaceConfidence": 99.9906005859375, 
#    "FaceMatches": [
#        {
#            "Face": {
#                "BoundingBox": {
#                    "Width": 0.4717549979686737, 
#                    "Top": 0.16526399552822113, 
#                    "Left": 0.234375, 
#                    "Height": 0.4717549979686737
#                }, 
#                "FaceId": "b1e93a17-05c7-5b54-b41a-552b5c50c146", 
#                "ExternalImageId": "lukas.png", 
#                "Confidence": 99.99960327148438, 
#                "ImageId": "b440ba40-6664-5448-86c6-52a905843b42"
#            }, 
#            "Similarity": 86.0721206665039
#        }
#    ]
#}

    try:
        data = json.loads(output)
    except ValueError as e:
        return None
    
    if len(data["FaceMatches"]) == 0:
        return None
    else:
        return data["FaceMatches"][0]["Face"]["ExternalImageId"].split(".")[0]
    
    
def upload_image(image_filename):
    conn = boto.connect_s3()
    b = conn.get_bucket('doorcamera')
    k = Key(b)
    k.key = image_filename
    k.set_contents_from_filename(image_filename)

def label_image(image_filename):
    cmd = Popen("bash detect-labels.sh %s" % image_filename, shell=True, stdout=PIPE)
    
    output = ""
    for line in cmd.stdout:
        output += line

    #print(output)
    data = json.loads(output)

    # Sample output
# {
#    "Labels": [
#        {
#            "Confidence": 99.107177734375, 
#            "Name": "People"
#        }, 
#        {
#            "Confidence": 99.10718536376953, 
#            "Name": "Person"
#        }, 
#        {
#            "Confidence": 99.08333587646484, 
#            "Name": "Human"
#        },
#    ], 
#    "OrientationCorrection": "ROTATE_180"
#}


    if not ('Labels' in data):
        print("Error in output: %s", output)
        return []
    
    labels= [label['Name'] for label in data['Labels']]
    
    return labels
    
def save_camera(camera):
    url = '%s.local/cam.jpg' % camera
    file = '%s.jpg' % camera
    print "Getting %s" % url
    cmd = ["wget", url, '-O', file]
    p = call(cmd, stdout=PIPE)
###    print("%s: %i" % (camera, p))
    if (p == 0):
        print "Success!!"
        image_files.append(file)


def show_all_cameras():
    save_all_cameras()
    print image_files
    images = map(Image.open, image_files)
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)  
    
    new_im = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.show()
    #new_im.save('test.jpg')


def label_camera(camera):
    file = '%s.jpg' % camera
    save_camera(camera)
    im = Image.open(file)
    im.show()
    return label_image(file)

def face_camera(camera):
    file = '%s.jpg' % camera

    save_camera(camera)
    im = Image.open(file)
    im.show()
    person = identify_face_image(file)
    data = describe_face_image(file)
    if data:
            
        return [person, data[0], data[1]]
    else:
        return None


    
def save_all_cameras():
    threads = []
    for camera in camera_list:
        thread = threading.Thread(target=save_camera, args=(camera,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        print thread.getName()
        thread.join()
    
if __name__ == "__main__":
    #show_all_cameras()
    #label_camera("willa")
    print face_camera("willa")
