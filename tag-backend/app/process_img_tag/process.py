import cv2
from fastapi import UploadFile
import numpy as np
import json


async def process_image(imagefile: UploadFile):


    labelsPath = "./cfg/coco.names"

    Labels = open(labelsPath).read().strip().split("\n")
    imagefile.seek(0)
    byte_img = await imagefile.read()

    img = cv2.imdecode(np.frombuffer(byte_img, np.uint8), cv2.COLOR_BGR2RGB)

    # Loads the Yolo algorithm
    net_obj = cv2.dnn.readNet(
        './cfg/yolov3-tiny.weights', './cfg/yolov3-tiny.cfg')

    # Object detection block
    class_ids = []
    accuracy = []

    lnames = net_obj.getLayerNames()
    layers = [lnames[i - 1] for i in net_obj.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(
        img, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

    net_obj.setInput(blob)

    result_det = net_obj.forward(layers)

    for each_result in result_det:
        for each in each_result:
            scores = each[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                accuracy.append(float(confidence))
                class_ids.append(class_id)

    # Convert the object list to set to get unique object values
    objects = set()
    length = len(class_ids)
    for i in range(length):
        objects.add(str(Labels[class_ids[i]]))

    # Put the detected objects to the DynamoDB
    return objects
