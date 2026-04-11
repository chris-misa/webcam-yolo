"""
First set the following variable, then run the script. Press `q` to exit.

Assumes the model detects a single class...
"""

import math
import cv2
from ultralytics import YOLO
from pythonosc.udp_client import SimpleUDPClient

# List of (IP address, UDP port) pairs to send OSC messages to
ENDPOINTS = [
    ("127.0.0.1", 8000),
]

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Which trained yolo model to load
#model = YOLO("brust-test1-best.pt")
model = YOLO("yolo26n.pt")

capture = cv2.VideoCapture(0) # use 0 for builtin camera, 2 for extern USB camerea
capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

def get_most_confident(res):
    """
    Return the box over all results with highest confidence
    """
    out = None
    for r in res:
        for box in r.boxes:
            if out is None:
                out = box
            elif box.conf[0] > out.conf[0]:
                out = box
    return out

def send_osc(clients, box):
    """
    Sends the extracted x, y coordinates as an osc message on the given client
    """
    x1, y1, x2, y2 = box.xyxy[0]

    cx = float(0.5 * x1 + 0.5 * x2) / float(FRAME_WIDTH)
    cy = float(0.5 * y1 + 0.5 * y2) / float(FRAME_HEIGHT)
    for client in clients:
        client.send_message("/yolo", (cx, cy))

def draw_res(img, box):
    """
    Draws the given box on the given image
    """
    x1, y1, x2, y2 = box.xyxy[0]
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

    # put box in cam
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

osc_clients = [SimpleUDPClient(addr, port) for addr, port in ENDPOINTS]

while True:
    rv, image = capture.read()

    if not rv or image is None:
        continue
    
    image = cv2.flip(image, 33)
    
    res = model(image, stream = True)
    most_conf = get_most_confident(res)
    if not most_conf is None:
        send_osc(osc_clients, most_conf)
        draw_res(image, most_conf)

    cv2.imshow("Webcam", image)
    if cv2.waitKey(1) == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()

def draw_res_OLD(img, res):
    """
    Draw results of object detection over the given image.
    Copied from https://dipankarmedh1.medium.com/real-time-object-detection-with-yolo-and-webcam-enhancing-your-computer-vision-skills-861b97c78993
    """
    for r in res:
        boxes = r.boxes

        mostConfident = boxes[0] if len(boxes) > 0 else None
        
        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            if box.conf[0] > mostConfident.conf[0]:
                mostConfident = box
            # print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            # print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            # cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
            cv2.putText(img, str(confidence), org, font, fontScale, color, thickness)
