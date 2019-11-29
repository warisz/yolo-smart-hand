import cv2
import numpy as np
import time
import serial

#arduino interfacing
ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout= 0.25)

#loading camera
cap = cv2.VideoCapture(2)
starting_time = time.time()
frame_id = 0
font = cv2.FONT_HERSHEY_PLAIN

width  = cap.get(3) # float
def isCentered(arr):
    if arr[1] > width/2-100 and arr[1] < width/2+100:
        return True
    return False

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


#claw capability
capableObjects = ['bottle', 'cup', 'toothbrush']
closeClaw = False

while True:
    #reading ultrasonic through serial port from arduino
    try:
        ultrasonicValue = int(ser.readline())
    except:
        ultrasonicValue = 0

    _, frame = cap.read()
    frame_id += 1

    height, width, channels = frame.shape

    #detecting objects
    #true value inverts blue with red (we are using BGR not RGB)
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (220, 220), (0, 0, 0), True, crop=False)
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
            if confidence > 0.1:
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
    currentObjects = []

    for i in range(num_of_objects_detected):
        if i in indexes:
            confidence = confidences[i]
            colour = colours[class_ids[i]]
            x, y, w, h = boxes[i]
            #printing class ids of detected objects
            label = str(classes[class_ids[i]])

            cv2.rectangle(frame, (x, y), (x + w, y + h), colour, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 25), font, 0.8, colour, 3)
            currentObjects.append([label, center_x, center_y])


    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 30), font, 1, (0, 0, 0), 1)
    cv2.imshow("Image", frame)

    #claw capability
    print(ultrasonicValue)
    for arr in currentObjects:
        if arr[0] in capableObjects and isCentered(arr) and ultrasonicValue <= 13:
            closeClaw = True
            print("CLOSE CLAW")
            ser.write("a".encode())
            time.sleep(10)
            ser.write("b".encode())
            time.sleep(2)
            ser.write("c".encode())


    #0 keeps img on hold, 1 keeps changing it every millisecond
    key = cv2.waitKey(1)
    #27 is s key on keyboard
    if key == 27:
        break

#make sure camera is closed
cap.release()
cv2.destroyAllWindows()

