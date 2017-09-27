# facerec

Code to setup a simple alexa powered, face recognizing system.

## Files 
- alexa_server.py
Runs a server that listens to commands from lambda server

- lambda.py 
Code for a lambda function that talks to alexa_server

- add-face.sh
Shell script to add a face for detection later

- detect-faces.sh
Shell script to detect a face in an image

- match-faces.sh
Shell script to match a face to previously uploaded faces

- ssh_tunnel.sh
Sets up an ssh tunnel from a local alexa server so that amazon's lambda function can call it


