import cv2
import numpy as np

#loading yolo, reading the network
# from cv2.dnn import NMSBoxes
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

#put each item in coco.names into an array
file = open("coco.names", "r")
classes = file.readlines() #makes array of each line in coco.names
file.close()
for i in range(0, len(classes)):
    classes[i] = classes[i].replace("\n", '')

colours = np.random.uniform(0, 255, size=(len(classes), 3))
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]

#loading image
img = cv2.imread("room_ser.jpg")
#resizing since it's too large for screen
img = cv2.resize(img, None, fx=0.2, fy=0.2)
height, width, channels = img.shape

#detecting objects
#true value inverts blue with red (we are using BGR not RGB)
blob = cv2.dnn.blobFromImage(img, 0.00392, (700, 700), (0, 0, 0), True, crop=False)
net.setInput(blob)
#forward to output layers
outs = net.forward(output_layers)

#showing info on screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            #object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            #rectangle coordinates
            x = int(center_x - w/2) #bottom left x
            y = int(center_y - h/2) #bottom left y

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

#only important, indexes of first time classification
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

num_of_objects_detected = len(boxes)
font = cv2.FONT_HERSHEY_COMPLEX
for i in range(num_of_objects_detected):
    if i in indexes:
        colour = colours[i]
        x, y, w, h = boxes[i]
        #printing class ids of detected objects
        label = str(classes[class_ids[i]])
        cv2.rectangle(img, (x, y), (x + w, y + h), colour, 2)
        cv2.putText(img, label, (x, y + 25), font, 0.8, colour, 3)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
