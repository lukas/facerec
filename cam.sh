killall darknet
(cd ../darknet && ./darknet detector demo cfg/coco.data cfg/yolo.cfg yolo.weights http://$1/cam.jpg)
