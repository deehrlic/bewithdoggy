#https://thinkinfi.com/yolo-object-detection-using-python-opencv/

# opencv object tracking
# object detection and tracking opencv
import cv2
import numpy as np
import pyautogui
from paramiko import SSHClient
from scp import SCPClient
from time import sleep

def handle_result(label, x, y, w, h):
    print(label, x, y, w, h)
    f = open("direction.txt", "w")
    if(label == 'dog' or label == 'person'):
        if(x>150 and x<200):
            print("go")
            f.write("straight")
        elif(x<200):
            print("right")
            f.write("right")
        else:
            print("left")
            f.write("left")
    if(label != 'dog' and label != 'person'):
        print("left")
        f.write("left")
    f.close()

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname='10.0.0.128', port=22, username='pi', password='pi')
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('direction.txt', 'Desktop/controller.py/direction.txt') 

def yolo(image):
    # Loading image
    img = cv2.imread(image)
    
    # Load Yolo
    yolo_weight = "data/model/yolov3.weights"
    yolo_config = "data/model/yolov3.cfg"
    coco_labels = "data/model/coco.names"
    net = cv2.dnn.readNet(yolo_weight, yolo_config)
    
    classes = []
    with open(coco_labels, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    
    # print(classes)
    
    # # Defining desired shape
    fWidth = 320
    fHeight = 320
    
    # Resize image in opencv
    img = cv2.resize(img, (fWidth, fHeight))
    
    height, width, channels = img.shape
    
    # Convert image to Blob
    blob = cv2.dnn.blobFromImage(img, 1/255, (fWidth, fHeight), (0, 0, 0), True, crop=False)
    # Set input for YOLO object detection
    net.setInput(blob)
    
    # Find names of all layers
    layer_names = net.getLayerNames()
    #print(layer_names)
    # Find names of three output layers
    output_layers = [layer_names[net.getUnconnectedOutLayers()[0] - 1], layer_names[net.getUnconnectedOutLayers()[1] - 1], layer_names[net.getUnconnectedOutLayers()[2] - 1]]
    
    # Send blob data to forward pass
    outs = net.forward(output_layers)
    
    # Generating random color for all 80 classes
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    
    # Extract information on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            # Extract score value
            scores = detection[5:]
            # Object id
            class_id = np.argmax(scores)
            # Confidence score for each object ID
            confidence = scores[class_id]
            # if confidence > 0.5 and class_id == 0:
            if confidence > 0.5:
                # Extract values to draw bounding box
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # Draw bounding box with text for each object
    font = cv2.FONT_HERSHEY_DUPLEX
    if(len(boxes) > 0):
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                print(label)
                confidence_label = int(confidences[i] * 100)
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, f'{label, confidence_label}', (x-25, y + 75), font, 1, color, 2)

                print(label, x, y, w, h)
                handle_result(label, x, y, w, h)
        
        #cv2.imshow("Image", img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    else:
        print("NOTHING FOUND")
        handle_result("none",0,0,0,0)



while True:
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save('cap.png')
    yolo('cap.png')
    sleep(1)
    